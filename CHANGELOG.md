# Changelog

## [1.5.0] - 2026-03-29

### Added
- **`tools/convert_golden.py`** — Golden output → verify_tier_a.py assertion
  format converter. Bridges the two-format gap. Supports `--agent` filter and
  `-o` file output. Extracts embedded `tier_a_assertions_file` sections.
- **`tools/requirements.txt`** — PyYAML dependency declaration.

### Fixed
- `verify_tier_a.py` now catches assertion file parse errors (was unhandled crash).
- `verify_tier_a.py` validates assertion file has `assertions` key.
- `execution-trace-example.md` Step 3 output replaced with verbatim script output
  (was paraphrased, misrepresenting provenance).
- README.md golden output count corrected: 5 → 7.
- team-examples.md headers updated from v1.3.0 to v1.4.0.

### Changed
- Full pipeline now works: golden output → `convert_golden.py` → assertion YAML
  → `verify_tier_a.py` → pass/fail report. No manual format translation needed.

## [1.4.0] - 2026-03-29

### Added
- **`tools/verify_tier_a.py`** — Executable Python script that deterministically
  validates agent output YAML against Tier A assertions. Supports 11 assertion types:
  yaml_valid, field_exists, not_empty, one_of, range, max_length, min_length,
  is_type, equals, min_count, max_count. Outputs table or JSON. Exit code 1 on failure.
- **`tools/sample-assertions.yaml`** — Sample assertion file for ticket-classifier.
- **`references/execution-trace-example.md`** — Real execution trace showing:
  actual Agent tool call → verbatim agent response → `verify_tier_a.py` output →
  Tier B evaluation → golden output comparison → score calculation. Every output
  captured from a live run, not hypothetical.
- **Edge case golden output:** `UC-SAAS-03-edge-multilingual.yaml` — Mixed
  Korean/English ticket to test language bias in classification.
- **Failure golden output:** `UC-ECOM-01-failure-missing-fields.yaml` — All
  required fields missing, tests graceful failure and pipeline halt.
- Golden output count: 5 happy path + 1 edge + 1 failure = 7 total.

### Changed
- SKILL.md Phase 5 Step 2 now references `tools/verify_tier_a.py` for Tier A
  verification and `execution-trace-example.md` for walkthrough.
- Tier A claim is now backed by executable code, not just documentation.

## [1.3.1] - 2026-03-29

### Fixed
- qa-adversary-guide.md deduction values synced to -10/-5/-2 (was -15/-8/-3)
- qa-adversary-guide.md "Method A/B" terminology replaced with Phase 5 step references
- team-examples.md: all 8 instances of "v1.1.0" updated to "v1.3.0"
- team-examples.md: Example 1 score corrected from 88 to 93 (matches assertion walkthrough)
- Adversary guide now references qa-scoring-engine.md as single source of truth for deductions

## [1.3.0] - 2026-03-29

### Changed
- **Honesty-first scoring:** Assertions split into Tier A (machine-verifiable: format,
  contract, structural) and Tier B (LLM-judged: decision, business quality). Score Card
  reports both tiers separately so users know exactly what's deterministic vs model-evaluated.
- **Adversary deductions recalibrated:** Critical -10 (max 3), Major -5 (max 5),
  Minor -2 (max 5), total cap -40. Rationale provided for each value.
- **QA modes added:** Quick (~6 invocations), Standard (~7), Full (~11). Users choose
  based on budget and validation stage.
- **team-examples.md fully rebuilt** with assertion-based scoring — every score point
  traceable to specific pass/fail assertions with evidence.
- **improvement-playbook.md report template updated** with Tier A/B columns,
  adversary findings status tracking, and assertion-level change tracking.
- **README.md and README_KO.md fully synchronized** with v1.3 features.
- Removed overclaims: no longer states "no subjective component." Honestly categorizes
  what is machine-verifiable vs what requires LLM judgment.

### Added
- **Baseline agent specification** for with/without comparison (sonnet model, generic
  prompt, standard tools — documented in qa-scoring-engine.md).
- **Golden outputs expanded** to 5 files (1 per domain): UC-SAAS-03, UC-ECOM-01,
  UC-FIN-01, UC-MEDIA-01, UC-DEV-02.
- **Tier promotion rule:** When golden output exists, Tier B decision assertions
  become Tier A (comparing against pre-verified baseline, not generated expectation).
- **Phase 5 execution trace walkthrough** in team-examples.md with real assertion
  results, adversary findings, and score calculation steps.
- **Cost guidance** with invocation estimates per QA mode per team size.

### Fixed
- plugin.json version now matches changelog (was 1.0.0, now 1.3.0).
- All files internally consistent — no v1.1 terminology remaining.
- Score Card template includes Tier A/B separation, adversary cap, QA mode indicator.

## [1.2.0] - 2026-03-29

### Changed
- **QA scoring engine completely rebuilt:** Replaced subjective 0-100 scoring with
  binary assertion framework. Every score point is now earned from pass/fail checks,
  not LLM judgment.
- Phase 5 now has 4 evidence sources: live execution, binary assertions, adversarial
  review, and with/without comparison.
- Phase 6 improvement loop now targets specific failing assertions (concrete action
  items) instead of vague axis-level improvements.
- Score calculation: `base_score - adversary_deductions` with transparent formula.

### Added
- `references/qa-adversary-guide.md` — Adversarial reviewer agent that attacks the
  generated team from 6 angles: contract violations, missing error paths, business
  logic gaps, adversarial inputs, cross-agent consistency, assertion verification.
  Runs with a completely different system prompt and does NOT see generation instructions.
- `references/golden-outputs/UC-SAAS-03-happy-path.yaml` — Pre-verified expected
  output with structural assertions for customer support ticket processing.
- `references/golden-outputs/UC-ECOM-01-happy-path.yaml` — Pre-verified expected
  output with structural assertions for product listing pipeline.
- Binary assertion categories: Format, Contract, Decision, Business Rule.
- Adversary severity deductions: Critical (-15), Major (-8), Minor (-3).

### Fixed
- Eliminated all subjective scoring. No axis score is assigned by LLM opinion.
- Score Card template now shows assertion pass rates, not subjective grades.
- Adversary review breaks the self-evaluation loop (different prompt, no generation context).

## [1.1.0] - 2026-03-29

### Changed
- Phase 5 redesigned: Replaced simulated dry-run with empirical validation
  using live agent execution (Method A) and with/without comparison (Method B)
- QA scoring engine updated to measure from real execution traces
- SKILL.md reduced, removed duplicate content
- UC-ECOM-04 pattern corrected from Expert Pool to Pipeline

### Added
- `references/agent-definition-spec.md` — Mandatory agent file format with
  model selection guide, tool access principles, data passing protocols,
  execution mode selection (subagent vs Agent Teams)
- `references/skill-writing-guide.md` — Why-first instructions, pushy
  descriptions, progressive disclosure, anti-patterns, quality checklist
- `references/team-examples.md` — 2 complete working examples with full
  agent files, orchestrators, skills, and score breakdowns
- Phase 1 conflict detection and user level assessment
- `_workspace/{uc-id}/` convention for intermediate artifacts

### Fixed
- Removed circular reasoning in improvement loop
- Eliminated content duplication between SKILL.md and reference files

## [1.0.0] - 2026-03-29

### Added
- 6-phase workflow: Domain Discovery → Use Case Mapping → Agent Team Design →
  QA Scenario Generation → Dry-Run & Scoring → Improvement Loop
- 5-axis QA scoring engine
- Automated improvement loop with max 3 rounds
- Use case catalog with 5 domains × 4 use cases (20 templates)
- 6 architecture pattern guides with decision tree
- QA scenario templates (happy path, edge case, failure)
- Improvement playbook with axis-specific strategies
- Orchestrator templates for all 6 patterns
- Bilingual README (English + Korean)
