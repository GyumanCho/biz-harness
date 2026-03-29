# Improvement Playbook

Automated improvement strategies for agent teams that score below the 80-point
threshold. Organized by quality axis with specific, actionable interventions.

## Improvement Loop Rules

1. **Maximum 3 rounds** — prevents infinite optimization loops
2. **Target lowest 2 axes** — focus effort where impact is greatest
3. **Track score progression** — if score gains < 5 points, switch strategy
4. **Record all changes** — every modification is logged as a diff
5. **Delegate after round 3** — user gets full comparison report

## Loop Flow

```
Score < 80
│
├─ Identify 2 lowest-scoring axes
├─ Select improvement strategies for each axis
├─ Apply changes to agent/skill files
├─ Record changes as diff
│
├─ Re-run empirical validation & scoring
│   │
│   ├─ Score >= 80 → PASS: Finalize + report
│   │
│   ├─ Score improved by 5+ points → Continue to next round
│   │
│   ├─ Score improved by < 5 points → Switch strategy
│   │   ├─ Try next strategy in the axis playbook
│   │   └─ If all strategies exhausted → Target next-lowest axis
│   │
│   └─ Round > 3 → STOP: Delegate to user
│       └─ Generate full comparison report across all rounds
```

---

## Axis-Specific Strategies

### Completeness Strategies

**C1: Gap Fill — Add Missing Agent Coverage**
- Symptom: Use case steps with no agent mapping
- Action: Create new agent for uncovered step, or extend existing agent's scope
- Risk: May increase agent count (keep under 8)

**C2: Handoff Repair — Fix Agent-to-Agent Transitions**
- Symptom: Agent A's output doesn't connect to Agent B's input
- Action: Align output format of upstream agent with input contract of downstream
- Risk: May require changing both agents

**C3: Trigger & Outcome Anchoring**
- Symptom: Missing trigger handler or outcome verification
- Action: Add explicit trigger detection to first agent; add verification step to last
- Risk: Low — usually a missing instruction in system prompt

**C4: Error Path Addition**
- Symptom: No fallback when a step fails
- Action: Add error detection and fallback routing to orchestrator
- Risk: Low — orchestrator modification only

---

### Accuracy Strategies

**A1: Prompt Sharpening — Clarify Agent Instructions**
- Symptom: Agent produces vaguely correct but imprecise output
- Action: Add specific output format requirements, constraints, and examples
- Example: "Classify as exactly one of: [bug, feature, question, other]"

**A2: Few-Shot Injection — Add Examples to Agent Context**
- Symptom: Agent misinterprets the task despite clear instructions
- Action: Add 2-3 concrete input/output examples to the agent's system prompt
- Risk: Increases context consumption — keep examples minimal

**A3: Output Schema Enforcement**
- Symptom: Agent output is unstructured or inconsistent format
- Action: Define explicit output schema (JSON, YAML, or structured markdown)
- Example: "Output must be a YAML block with keys: category, confidence, reasoning"

**A4: Domain Vocabulary Injection**
- Symptom: Agent uses generic terms instead of domain-specific language
- Action: Add domain glossary to agent's context or skill reference
- Risk: Moderate context cost — keep glossary under 50 terms

---

### Consistency Strategies

**S1: Deterministic Branching — Replace Ambiguous Decisions**
- Symptom: Agent makes different routing/classification decisions across runs
- Action: Add explicit decision criteria with thresholds
- Example: "If confidence > 0.8 → auto-approve. If 0.5-0.8 → review. If < 0.5 → reject"

**S2: Input Normalization**
- Symptom: Variations in input format cause different behaviors
- Action: Add preprocessing step to normalize input before agent processing
- Risk: Low — usually a simple text normalization instruction

**S3: Output Anchoring**
- Symptom: Agent produces wildly different phrasings for same semantic output
- Action: Provide output templates or structured formats
- Risk: May reduce naturalness — use only for decision-critical outputs

---

### Performance Strategies

**P1: Agent Consolidation — Merge Redundant Agents**
- Symptom: Two agents doing overlapping work
- Action: Merge into single agent with combined responsibilities
- Constraint: Merged agent must still have clear single purpose

**P2: Context Tier Optimization**
- Symptom: Agent loads full reference when only partial is needed
- Action: Split reference into smaller, phase-specific files
- Risk: May require restructuring reference documents

**P3: Parallel Execution Identification**
- Symptom: Sequential execution of independent agents
- Action: Mark independent agents for parallel execution in orchestrator
- Risk: Must verify agents truly have no data dependency

**P4: Early Termination**
- Symptom: Pipeline continues even when early result is sufficient
- Action: Add conditional exit points in orchestrator
- Example: "If classification confidence > 0.95, skip validation agent"

---

### Business Fit Strategies

**B1: Goal Alignment Audit**
- Symptom: Agent outputs are technically correct but don't serve the business goal
- Action: Add business goal as explicit context to each agent
- Example: Prepend "Business goal: Reduce MTTR by 50%" to agent prompts

**B2: Stakeholder Language Adaptation**
- Symptom: Output is too technical for target audience
- Action: Add audience profile to output-generating agents
- Example: "Write for: Product managers with no engineering background"

**B3: Business Rule Injection**
- Symptom: Agent ignores domain-specific business rules
- Action: Add business rules as explicit constraints in agent prompt
- Risk: Must verify rules are current and complete

**B4: Outcome Measurement Addition**
- Symptom: Cannot verify if the business goal was actually served
- Action: Add measurement/tracking step to the workflow
- Example: Add a metrics-collection agent at the end of the pipeline

---

## Strategy Selection Priority

When an axis scores low, try strategies in order:

| Axis | Try First | Then | Last Resort |
|------|-----------|------|-------------|
| Completeness | C1 (Gap Fill) | C2 (Handoff) | C3, C4 |
| Accuracy | A1 (Sharpen) | A3 (Schema) | A2, A4 |
| Consistency | S1 (Deterministic) | S3 (Anchor) | S2 |
| Performance | P3 (Parallel) | P1 (Consolidate) | P2, P4 |
| Business Fit | B1 (Align) | B3 (Rules) | B2, B4 |

---

## Round Comparison Report Template

Generated after all rounds complete (pass or max rounds reached):

```markdown
# BizHarness QA Report

## Summary
- Domain: {domain}
- Use Cases: {count} evaluated
- QA Mode: {Quick | Standard | Full}
- Final Score: {score}/100 {grade}
- Improvement Rounds: {rounds_completed}/{max_rounds}

## Assertion Progression
| Metric | Round 1 | Round 2 | Round 3 | Final |
|--------|---------|---------|---------|-------|
| Tier A Pass Rate | {%} | {%} | {%} | {%} |
| Tier B Pass Rate | {%} | {%} | {%} | {%} |
| Adversary Deductions | -{pts} | -{pts} | -{pts} | -{pts} |
| **Final Score** | **{n}** | **{n}** | **{n}** | **{n}** |

## Axis Scores (Final)
| Axis | Tier A | Tier B | Combined | Weight |
|------|--------|--------|----------|--------|
| Completeness | {n}/{n} | — | {score} | 25% |
| Accuracy | {n}/{n} | {n}/{n} | {score} | 25% |
| Consistency | {n}/{n} | {n}/{n} | {score} | 15% |
| Performance | {n}/{n} | — | {score} | 15% |
| Business Fit | {n}/{n} | {n}/{n} | {score} | 20% |

## Changes Applied Per Round

### Round {N}
- Failed assertions targeted: {list of assertion names}
- Strategy applied: {strategy_id}: {strategy_name}
- Files modified: {list}
- Assertions fixed: {count} of {count} targeted
- Score impact: {before} → {after} ({delta})

## Adversary Findings (Full mode)
| # | Severity | Attack Pattern | Issue | Status |
|---|----------|---------------|-------|--------|
| 1 | {level} | {pattern} | {desc} | Fixed / Open / Accepted |

## Per Use Case Results
### {UC-ID}: {name}
- Tier A: {n}/{n} ({%})
- Tier B: {n}/{n} ({%})
- Final Score: {score}/100 {grade}
- Open Issues: {remaining}

## Generated Files
| File | Purpose | Use Case |
|------|---------|----------|
| {path} | {description} | {UC-ID} |

## Recommendations
- {Tier A fixes remaining — machine-verifiable, should be addressed}
- {Tier B improvements — involve judgment, may need human review}
- {Adversary findings still open — prioritize by severity}
```

---

## When to Recommend Architecture Pattern Change

If after 2 rounds the score is still below 60, consider recommending a different
architecture pattern:

| Current Pattern | Common Issues | Consider Switching To |
|----------------|---------------|----------------------|
| Pipeline | Steps need parallel analysis | Fan-out/Fan-in |
| Fan-out/Fan-in | Synthesis is losing information | Pipeline with richer handoff |
| Expert Pool | Router accuracy is low | Supervisor with dynamic routing |
| Producer-Reviewer | Revision loop not converging | Fan-out/Fan-in with multiple producers |
| Supervisor | Coordination overhead too high | Pipeline with simpler flow |
