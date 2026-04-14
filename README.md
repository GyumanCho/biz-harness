# BizHarness

Business use-case driven agent team generator for Claude Code with tiered QA validation.

## What It Does

BizHarness takes your business domain as input, guides you through selecting
standard use cases, generates a validated agent team, and tests it with a
transparent, tiered scoring system that separates machine-verifiable checks
from model-judged evaluations.

```
Domain → Use Cases → Agent Team → Tiered QA → Improvement Loop → Validated Output
```

## Key Differentiators

| Feature | Traditional Harness | BizHarness |
|---------|-------------------|------------|
| Starting point | Technical patterns | Business use cases |
| QA method | Manual / simulated | **Tier A (machine-verifiable) + Tier B (LLM-judged) + adversarial review** |
| Scoring transparency | Single score | **Tier A/B split reporting — you know what's verified vs judged** |
| Adversarial testing | None | **Independent attacker agent (6 attack patterns)** |
| Cost control | All-or-nothing | **Quick / Standard / Full QA modes** |
| Agent spec | Informal | **Mandatory format with model selection, I/O contracts** |
| Use case library | None | 5 domains × 4 use cases + golden outputs |

## Installation

```bash
# 1) Register the marketplace
claude plugin marketplace add GyumanCho/biz-harness

# 2) Install the plugin
claude plugin install biz-harness@biz-harness
```

For local development:
```bash
claude --plugin-dir /path/to/biz-harness
```

## Usage

```
> build a harness for this project
> create agent team for e-commerce
> /biz-harness
```

## 6-Phase Workflow

1. **Domain Discovery** — Identify domain, detect existing agents, assess context
2. **Use Case Mapping** — Select from 20 standard use cases or bring your own
3. **Agent Team Design** — Generate agents (with spec), skills (with guide), orchestrator
4. **QA Scenario Generation** — Create E2E scenarios (happy/edge/failure)
5. **Empirical Validation** — Choose QA mode, run tiered assertions + adversarial review
6. **Improvement Loop** — Fix failing assertions, re-test, repeat (max 3 rounds)

## QA Modes

| Mode | What Runs | Cost (3-agent team) |
|------|-----------|---------------------|
| Quick | Live execution + Tier A assertions | ~6 invocations |
| Standard | + Tier B assertions + golden output | ~7 invocations |
| Full | + adversarial review + with/without baseline | ~11 invocations |

## Assertion Tiers

| Tier | What It Checks | How It's Verified |
|------|---------------|-------------------|
| **Tier A** | YAML validity, field presence, types, ranges, contracts | Deterministic — no LLM judgment |
| **Tier B** | Decision correctness, business quality, domain fit | LLM-judged — reported separately |

Score Card always shows both tiers so you know exactly what's machine-verified.

## Reference Files (12)

| File | Purpose |
|------|---------|
| `usecase-catalog.md` | 20 use case templates across 5 domains |
| `agent-patterns.md` | 6 architecture patterns with decision tree |
| `agent-definition-spec.md` | Agent file format, model selection, data passing |
| `skill-writing-guide.md` | Why-first instructions, anti-patterns |
| `qa-scoring-engine.md` | Tier A/B assertion framework, cost guide, baseline spec |
| `qa-adversary-guide.md` | Adversarial reviewer with 6 attack patterns |
| `qa-scenario-templates.md` | Happy/edge/failure scenario templates |
| `improvement-playbook.md` | Axis-specific strategies, report template |
| `orchestrator-templates.md` | Templates for all 6 patterns |
| `team-examples.md` | 2 complete teams with assertion-based score breakdowns |
| `golden-outputs/` | 7 verified expected outputs (5 happy + 1 edge + 1 failure) |

## Requirements

- Claude Code
- `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` (only for Supervisor/Producer-Reviewer)

## License

Apache-2.0
