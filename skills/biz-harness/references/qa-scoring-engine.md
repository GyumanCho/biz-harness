# QA Scoring Engine

Quantitative quality assessment framework for evaluating generated agent teams.

## Scoring Philosophy

Scores are derived from **four evidence sources**, with honest categorization
of what is objectively verifiable vs. what requires LLM judgment.

```
Evidence Source              Objectivity    Purpose
─────────────────────────    ───────────    ─────────────────────
1. Tier A Assertions         Objective      Structural correctness
2. Tier B Assertions         LLM-judged     Decision & business quality
3. Golden Output Comparison  Objective      Structural match against verified baseline
4. Adversarial Review        Independent    Stress-test from outsider perspective
```

**Honesty principle:** We do NOT claim all assertions are objective. Tier A
assertions are machine-verifiable. Tier B assertions require LLM judgment and
are reported separately so users know exactly which parts of the score are
deterministic and which are model-evaluated.

---

## Assertion Tiers

### Tier A: Machine-Verifiable (no LLM judgment needed)

These assertions have deterministic answers. A script could evaluate them.

**Format Assertions:**
```yaml
- output_is_valid_yaml: true/false
- all_required_fields_present: true/false
- field_X_is_one_of: ["valid", "values"]  # enumerated set
- string_length_lte: 200
- numeric_value_positive: true/false
- word_count_within_range: [50, 300]
- image_count_gte: 1
```

**Contract Assertions:**
```yaml
- agent_A_output_has_field_X: true/false  # field existence
- orchestrator_passes_all_intermediate_outputs: true/false
- no_agent_receives_empty_input: true/false
- output_yaml_keys_match_schema: ["key1", "key2", "key3"]
```

**Structural Assertions:**
```yaml
- total_agents_lte: 8
- parallel_agents_have_no_data_dependency: true/false
- every_use_case_step_mapped_to_agent: true/false
- trigger_handler_exists: true/false
- error_path_exists_for_each_step: true/false
```

**How to verify Tier A:** Extract field → apply check → Pass/Fail.
No interpretation. No "close enough."

### Tier B: LLM-Judged (requires model evaluation)

These assertions require understanding meaning, not just structure. They are
valuable but inherently involve model judgment. Report them separately.

**Decision Assertions:**
```yaml
- classification_matches_expected: true/false
  # WHY Tier B: "expected" value was determined by LLM or human author.
  # For golden outputs, this becomes Tier A (pre-verified expected value).

- routing_decision_matches_expected: true/false
- escalation_triggered_appropriately: true/false
```

**Business Quality Assertions:**
```yaml
- response_addresses_specific_issue: true/false
  # WHY Tier B: Requires semantic understanding of "addresses."

- domain_terminology_used_correctly: true/false
- output_is_actionable_for_target_audience: true/false
- harness_output_more_structured_than_baseline: true/false
```

**How to verify Tier B:** LLM reads the output and makes a judgment call.
These checks are better than subjective 0-100 scoring because they force
explicit criteria, but they are NOT machine-verifiable. Users should weight
Tier A results more heavily when trust matters.

**Tier promotion:** When a golden output exists with a pre-verified expected
value, decision assertions become Tier A (comparing against a fixed baseline
instead of a generated expectation).

---

## Evidence Source: Golden Output Comparison

For use cases with golden outputs (`references/golden-outputs/`):

1. Run the agent team with the golden output's test input
2. Compare real output against golden expected output
3. Score by structural match:

```yaml
comparison_metrics:
  fields_present: "{matched}/{expected}"
  decisions_correct: "{matched}/{expected}"
  contracts_satisfied: "{matched}/{expected}"
  cross_agent_consistent: "{matched}/{expected}"
```

Match criteria is structural, not textual:
- Same YAML keys present? (not same prose)
- Same classification/routing decision? (not same explanation)
- Same numeric values within 5%? (not exact float match)

**Golden output coverage:** 5 domains covered (SaaS, E-Commerce, Fintech,
Content, DevTools). For custom domains, Tier B assertions are used until the
user authors a golden output (recommended).

---

## Evidence Source: Adversarial Review

Load `references/qa-adversary-guide.md` for the full spec.

### Deduction Calibration

Deduction values are based on impact severity:

| Severity | Deduction | Rationale | Cap |
|----------|-----------|-----------|-----|
| CRITICAL | -10 pts | Would cause harness to fail entirely (missing agent, broken contract) | Max 3 counted |
| MAJOR | -5 pts | Would cause incorrect results in some scenarios (wrong routing, missed edge case) | Max 5 counted |
| MINOR | -2 pts | Suboptimal but functional (verbose output, missed optimization) | Max 5 counted |

**Total deduction cap: -40 points maximum.**

Why capped: An uncapped adversary creates a perverse incentive to report fewer
issues. The cap ensures the adversary can be thorough without guaranteeing a
zero score. A base score of 90 with max deductions still yields 50 (POOR),
which correctly triggers improvement rounds.

**Why these specific values:** CRITICAL issues block the use case entirely
(10 pts = one axis loses 40%). MAJOR issues corrupt specific scenarios
(5 pts = noticeable but recoverable). MINOR issues are polish
(2 pts = worth fixing but not blocking).

Users may adjust these values in the orchestrator prompt if their domain
requires stricter or more lenient thresholds.

---

## Baseline Agent for With/Without Comparison

The "without harness" baseline uses this configuration:

```yaml
baseline_agent:
  model: sonnet
  prompt: |
    You are a general-purpose assistant. Complete the following task
    to the best of your ability. No specialized tools or domain knowledge
    are provided.

    Task: {the same task given to the harness}
  tools:
    - Read
    - Write
    - Grep
    - Glob
    - WebSearch
```

**Why sonnet:** Matches the most common harness agent model. Using opus for
baseline would unfairly disadvantage the harness; using haiku would unfairly
advantage it.

**Comparison criteria** (Tier B assertions):
- `harness_output_more_structured_than_baseline` — Does the harness use
  consistent YAML/schema while baseline produces free text?
- `harness_output_more_domain_specific_than_baseline` — Does the harness
  use correct domain terminology that the baseline misses?
- `harness_covers_more_steps_than_baseline` — Does the harness address
  more use case steps?

---

## Score Calculation

### Per-Axis Scores

Each axis has Tier A and Tier B assertions mapped to it. Both contribute to
the axis score, but are reported separately for transparency.

| Axis | Tier A Assertions | Tier B Assertions | Weight |
|------|-------------------|-------------------|--------|
| Completeness (25%) | Coverage matrix, contract checks, trigger/outcome existence | — | 25% |
| Accuracy (25%) | Format validity, field presence, golden output structural match | Decision correctness, routing appropriateness | 25% |
| Consistency (15%) | Tier A assertions identical across 2 runs | Tier B assertions identical across 2 runs | 15% |
| Performance (15%) | Agent count, invocation count, redundancy checks | — | 15% |
| Business Fit (20%) | Prohibited words, word count, structural format | Domain terminology, actionability, with/without comparison | 20% |

```
axis_score = (tier_a_passed + tier_b_passed) / (tier_a_total + tier_b_total) × 100

base_score = (completeness × 0.25) + (accuracy × 0.25) +
             (consistency × 0.15) + (performance × 0.15) +
             (business_fit × 0.20)

adversary_deductions = min(40,
  (critical_count × 10, max 3 counted) +
  (major_count × 5, max 5 counted) +
  (minor_count × 2, max 5 counted))

final_score = max(0, base_score - adversary_deductions)
```

---

## QA Cost Guide

### Invocation Estimates by QA Mode

| Mode | What Runs | Agent Invocations | When to Use |
|------|-----------|-------------------|-------------|
| **Quick** | Live execution + Tier A assertions only | ~N×2 (N = agent count, run twice) | Budget-constrained, iterating fast |
| **Standard** | Quick + Tier B assertions + golden output comparison | ~N×2 + 1 (comparison) | Default for most teams |
| **Full** | Standard + adversarial review + with/without baseline | ~N×3 + 2 (adversary + baseline) | Final validation before deployment |

For a typical 3-agent team:
- Quick: ~6 invocations
- Standard: ~7 invocations
- Full: ~11 invocations

Per improvement round, only failing scenarios re-run (~3-5 invocations).

**Recommendation:** Use Quick during design iteration, Standard for first
validation, Full for final sign-off.

---

## Grade Assignment

| Score | Grade | Symbol | Action |
|-------|-------|--------|--------|
| 90-100 | EXCELLENT | ★★★★★ | Finalize. Optional optimization. |
| 80-89 | GOOD | ★★★★ | Finalize. Note Tier B improvements. |
| 60-79 | FAIR | ★★★ | Fix failing Tier A assertions first. |
| 40-59 | POOR | ★★ | Architecture pattern change recommended. |
| 0-39 | FAIL | ★ | Restart from use case definition. |

---

## Score Card Template

```markdown
## Score Card: {UC-ID} {Use Case Name}
### QA Mode: {Quick | Standard | Full}

### Tier A Assertions (Machine-Verifiable)
| Category | Passed | Total | Rate |
|----------|--------|-------|------|
| Format | {n} | {n} | {%} |
| Contract | {n} | {n} | {%} |
| Structural | {n} | {n} | {%} |
| **Tier A Total** | **{n}** | **{n}** | **{%}** |

### Tier B Assertions (LLM-Judged)
| Category | Passed | Total | Rate |
|----------|--------|-------|------|
| Decision | {n} | {n} | {%} |
| Business Quality | {n} | {n} | {%} |
| **Tier B Total** | **{n}** | **{n}** | **{%}** |

### Axis Scores
| Axis | Tier A | Tier B | Combined | Weight |
|------|--------|--------|----------|--------|
| Completeness | {n}/{n} | — | {score} | 25% |
| Accuracy | {n}/{n} | {n}/{n} | {score} | 25% |
| Consistency | {n}/{n} | {n}/{n} | {score} | 15% |
| Performance | {n}/{n} | — | {score} | 15% |
| Business Fit | {n}/{n} | {n}/{n} | {score} | 20% |

### Adversarial Review (Full mode only)
| Severity | Found | Counted (cap) | Deduction |
|----------|-------|---------------|-----------|
| Critical | {n} | {min(n,3)} | -{pts} |
| Major | {n} | {min(n,5)} | -{pts} |
| Minor | {n} | {min(n,5)} | -{pts} |
| **Total** | | | **-{sum} (cap: -40)** |

### Final Score
- Base Score: {base}/100
- Tier A Confidence: {tier_a_rate}% (machine-verified)
- Tier B Confidence: {tier_b_rate}% (LLM-judged)
- Adversary Deduction: -{deduction}
- **Final Score: {final}/100 {grade}**

### Failed Assertions
| # | Tier | Assertion | Agent | Evidence |
|---|------|-----------|-------|----------|
| 1 | A/B | {text} | {agent} | {evidence} |

### Adversary Issues
| # | Severity | Attack | Issue | Fix |
|---|----------|--------|-------|-----|
| 1 | {level} | {pattern} | {desc} | {fix} |
```
