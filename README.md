# BizHarness

> Business use-case driven Claude Code agent team generator with tiered QA validation

[![Claude Code Plugin](https://img.shields.io/badge/Claude%20Code-Plugin-blueviolet)](https://github.com/GyumanCho/biz-harness)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](./LICENSE)
[![Version](https://img.shields.io/badge/version-1.5.0-green)]()

**English** | [한국어](./README_KO.md)

---

## TL;DR

**"Build a Claude Code agent team for your actual business work — and prove it works"** — from domain selection to empirical validation in under 30 minutes.

```
Domain → Use Cases → Agent Team → Tiered QA → Improvement Loop → Validated Output
```

---

## 🎯 Key Features

### 1. **Starts from Business Use Cases, Not Tech Patterns**
Library of 20 standard use cases (5 domains × 4) — or bring your own.
- **Domains**: SaaS / E-commerce / Finance / Media / Development
- **Examples**: *ticket classification*, *product listing generation*, *risk scoring*, *content moderation*, *code review*

### 2. **Three-Layer QA Validation** (breaks self-eval loop)
| Layer | What It Checks | How | Confidence |
|-------|----------------|-----|------------|
| **Tier A** | YAML validity, field presence, types, ranges, contracts | Deterministic Python script | 100% reproducible |
| **Tier B** | Decision correctness, business quality | LLM-judged (reported separately) | Transparently split |
| **Adversarial** | 6 attack patterns exposing weaknesses | Independent agent (no generation context) | Blocks self-bias |

**Key differentiator**: not a single opaque score — **tier-separated reporting** so you know exactly what is machine-verified vs model-judged.

### 3. **Cost-Controlled QA Modes**
| Mode | What Runs | Est. invocations (3-agent team) |
|------|-----------|---------------------------------|
| **Quick** | Execution + Tier A only | ~6 |
| **Standard** | + Tier B + Golden Output comparison | ~7 |
| **Full** | + Adversarial review + With/Without baseline | ~11 |

Choose by budget and stage (Quick during dev, Full before release).

### 4. **Mandatory Agent Specification Format**
Not free-form prompts — **structured specs** enforcing:
- Model selection rationale (Haiku / Sonnet / Opus)
- I/O contracts (input YAML schema → output YAML schema)
- Data-passing protocol between agents
- Execution mode (subagent vs Agent Teams)

### 5. **Built-in Golden Outputs**
7 pre-verified expected outputs (5 happy + 1 edge + 1 failure) — solves the "no comparison baseline" problem in LLM evaluation.

### 6. **Reusable Artifacts**
- **Agent files** (`.claude/agents/*.md`) — ready for Claude Code
- **Skill guides** (`.claude/skills/*/SKILL.md`) — documented domain knowledge
- **Orchestrators** — 6 architecture templates (Pipeline, Supervisor, Expert Pool, Producer-Reviewer, Hierarchical, Peer)
- **QA scenarios** — Happy/Edge/Failure YAML
- **Score Card** — reproducible validation report

---

## 🚀 Installation

### From marketplace (recommended)
```bash
# 1) Register the marketplace (one-time)
claude plugin marketplace add GyumanCho/biz-harness

# 2) Install the plugin
claude plugin install biz-harness@biz-harness
```

### For local development
```bash
claude --plugin-dir /path/to/biz-harness
```

### Update
```bash
claude plugin marketplace update biz-harness
claude plugin update biz-harness@biz-harness
```

---

## 💡 Usage

### Quickest start
Open Claude Code in your project directory, then:
```
> /biz-harness
```
Or in natural language:
```
> build an agent team for this project
> create a team for e-commerce listing automation
> make a harness for customer support ticket classification
```

### Example session
```
You    > /biz-harness
Claude > [Phase 1] Analyzing project...
         Domain: E-commerce (detected Shopify API in package.json)
         Existing agents: none
         User level: Intermediate

You    > proceed
Claude > [Phase 2] Recommended use cases:
         1. UC-ECOM-01 — Product listing pipeline ⭐ (recommended)
         2. UC-ECOM-02 — Inventory sync
         3. UC-ECOM-03 — Order status notifications
         4. Custom
         Choose:

You    > 1
Claude > [Phase 3] Designing agent team...
         - listing-writer (Sonnet, SEO copy)
         - image-tagger (Haiku, attribute extraction)
         - qa-reviewer (Sonnet, brand tone check)
         Architecture: Pipeline
         orchestrator.md generated.

You    > Standard QA mode
Claude > [Phase 5] Empirical validation (Standard)...
         ✅ Tier A: 12/12 passed
         ⚠️  Tier B: 8/10 (2 brand tone misses)
         Golden Output match: 87%
         → [Phase 6] proceed to improvement loop?
```

### Standalone tools
Usable without the plugin:
```bash
# Verify Tier A assertions
python tools/verify_tier_a.py output.yaml assertions.yaml

# Convert golden output → assertion file
python tools/convert_golden.py golden.yaml -o assertions.yaml
```

---

## 📋 6-Phase Workflow

| Phase | Name | Key Activities | Artifacts |
|-------|------|----------------|-----------|
| 1 | Domain Discovery | Project analysis, existing agent detection, conflict check | Domain report |
| 2 | Use Case Mapping | Present 20 standard UCs or custom definition | Selected UC-ID |
| 3 | Agent Team Design | Generate agents (spec), skills, orchestrator | `.claude/agents/*`, `.claude/skills/*`, orchestrator |
| 4 | QA Scenario Generation | Derive Happy/Edge/Failure scenarios | YAML scenario files |
| 5 | Empirical Validation | Pick QA mode, Tier A/B assertions + adversarial review | Score Card |
| 6 | Improvement Loop | Fix failing assertions, re-test (max 3 rounds) | Improved team + changelog |

---

## 📚 Reference Files (12)

| File | Purpose |
|------|---------|
| `usecase-catalog.md` | 20 use case templates across 5 domains |
| `agent-patterns.md` | 6 architecture patterns + decision tree |
| `agent-definition-spec.md` | Mandatory agent file format |
| `skill-writing-guide.md` | Why-first instructions, anti-patterns |
| `qa-scoring-engine.md` | Tier A/B framework, cost guide |
| `qa-adversary-guide.md` | 6 adversarial attack patterns |
| `qa-scenario-templates.md` | Happy/Edge/Failure templates |
| `improvement-playbook.md` | Axis-specific strategies, report template |
| `orchestrator-templates.md` | Orchestrators for all 6 patterns |
| `team-examples.md` | 2 complete teams with score breakdowns |
| `execution-trace-example.md` | Real execution trace walkthrough |
| `golden-outputs/` | 7 pre-verified expected outputs |

---

## 🛠 Requirements

- **Claude Code** (plugin-supported version)
- **Env var** (optional): `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` — only for Supervisor/Producer-Reviewer patterns
- **Python 3.8+** (for standalone tools): `pip install -r tools/requirements.txt`

---

## 🐛 Troubleshooting

**"Plugin not found"**
```bash
claude plugin marketplace update biz-harness
claude plugin marketplace list   # verify registration
```

**"Tier A assertion parse failure"**
→ Check YAML syntax. Run `python tools/verify_tier_a.py <output> <assertions>` for specific errors.

**"Adversarial review cost higher than expected"**
→ Switch to `Quick` mode. Full is recommended only right before release.

---

## 🗺 Roadmap

- [ ] Custom domain template builder
- [ ] MCP server integration use cases
- [ ] Multilingual golden outputs
- [ ] Cost dashboard (token/invocation tracking)

---

## 🤝 Contributing

Issues and PRs welcome — especially:
- New use case catalog entries
- Additional golden outputs
- New adversarial attack patterns

---

## 📄 License

Apache-2.0 — see [LICENSE](./LICENSE)
