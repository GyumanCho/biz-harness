# Agent Architecture Patterns

Guide for selecting the right architecture pattern based on business use case characteristics.

## Pattern Selection Decision Tree

```
Is the use case a sequential process with clear stages?
├─ YES → Does each stage need a different specialist?
│   ├─ YES → Pipeline
│   └─ NO  → Consider merging stages, then Pipeline
└─ NO  → Does the use case require parallel analysis of the same input?
    ├─ YES → Do parallel results need to be synthesized?
    │   ├─ YES → Fan-out/Fan-in
    │   └─ NO  → Expert Pool (pick best)
    └─ NO  → Does output need validation by a different perspective?
        ├─ YES → Producer-Reviewer
        └─ NO  → Is there a complex multi-step coordination need?
            ├─ YES → Supervisor
            └─ NO  → Hierarchical Delegation (nested teams)
```

---

## Pattern 1: Pipeline

**When to use:** Sequential business processes with clear stages.

```
[Agent A] → [Agent B] → [Agent C] → [Output]
```

**Characteristics:**
- Each agent completes its work before the next begins
- Output of one agent is input to the next
- Easy to debug — check each stage independently
- Natural fit for most business workflows

**Business use case fit:**
- Onboarding flows
- Order processing
- Content production
- Report generation
- CI/CD pipelines

**Agent design rules:**
- Each agent has a single responsibility
- Define clear input/output contracts between stages
- Include error handling: what happens if a stage fails?
- Consider timeout per stage

**Team mode suitability:** High — works well with `TaskCreate` sequential execution.

**Example orchestrator pattern:**
```
1. TaskCreate: Agent A processes input
2. Wait for completion
3. Pass output to Agent B via TaskCreate
4. Wait for completion
5. Pass output to Agent C via TaskCreate
6. Collect final output
```

---

## Pattern 2: Fan-out/Fan-in

**When to use:** Same input needs multiple parallel analyses, results synthesized.

```
              ┌─ [Agent A] ─┐
[Input] ──────┼─ [Agent B] ─┼──── [Synthesizer] → [Output]
              └─ [Agent C] ─┘
```

**Characteristics:**
- Parallel execution for speed
- Each agent analyzes from a different perspective
- Synthesizer resolves conflicts and merges insights
- Higher token cost but faster wall-clock time

**Business use case fit:**
- Multi-criteria evaluation (risk assessment)
- Content review from multiple angles
- Customer analysis (sentiment + intent + history)
- Incident triage (correlate multiple data sources)

**Agent design rules:**
- Fan-out agents must be independent (no shared state)
- Define the synthesizer's conflict resolution strategy
- Set timeout for slowest agent — don't block on stragglers
- Consider partial results if one agent fails

**Team mode suitability:** High — use parallel `Agent` tool calls.

---

## Pattern 3: Expert Pool

**When to use:** Input needs routing to the right specialist.

```
                 ┌─ [Expert A]
[Router] ────────┼─ [Expert B]
                 └─ [Expert C]
```

**Characteristics:**
- Router determines which expert(s) to engage
- Only relevant experts are activated (token efficient)
- Experts have deep, narrow domain knowledge
- Router needs broad classification ability

**Business use case fit:**
- Customer support routing by category
- Document processing by type
- Task assignment by skill requirement
- Advisory services by domain

**Agent design rules:**
- Router must have clear classification criteria
- Experts should have non-overlapping domains
- Define fallback when no expert matches
- Include confidence threshold for routing decisions

**Team mode suitability:** Medium — router uses conditional `Agent` dispatch.

---

## Pattern 4: Producer-Reviewer

**When to use:** Output quality requires validation from a different perspective.

```
[Producer] → [Reviewer] → [Accept/Revise] → [Output]
                  ↑              │
                  └──── Revise ──┘
```

**Characteristics:**
- Separation of generation and evaluation
- Built-in quality control loop
- Reviewer catches errors the producer is blind to
- Natural limit on revision rounds prevents infinite loops

**Business use case fit:**
- Content creation with editorial review
- Code generation with security review
- Financial reports with compliance check
- Legal document drafting with review

**Agent design rules:**
- Producer and reviewer must have different system prompts
- Reviewer must provide specific, actionable feedback
- Set maximum revision rounds (typically 2-3)
- Define "good enough" acceptance criteria

**Team mode suitability:** High — natural back-and-forth via `SendMessage`.

---

## Pattern 5: Supervisor

**When to use:** Complex coordination with dynamic task assignment.

```
            [Supervisor]
           /     |      \
    [Agent A] [Agent B] [Agent C]
```

**Characteristics:**
- Supervisor maintains overall state and progress
- Dynamically assigns tasks based on current state
- Can reassign work if an agent fails
- Highest coordination overhead

**Business use case fit:**
- Project management automation
- Multi-stage approval workflows
- Complex investigation processes
- Resource allocation and scheduling

**Agent design rules:**
- Supervisor must track state explicitly
- Define escalation criteria clearly
- Include deadlock detection (circular dependencies)
- Supervisor should be lightweight — coordinate, not execute

**Team mode suitability:** High — supervisor uses `TeamCreate` with `SendMessage`.

---

## Pattern 6: Hierarchical Delegation

**When to use:** Large-scale processes with nested sub-teams.

```
         [Top Coordinator]
          /            \
   [Sub-Team A]    [Sub-Team B]
    /    \           /    \
 [A1]   [A2]     [B1]   [B2]
```

**Characteristics:**
- Multiple levels of coordination
- Sub-teams can use different patterns internally
- Scales to complex organizational processes
- Highest complexity — use only when simpler patterns fail

**Business use case fit:**
- Enterprise workflow automation
- Multi-department processes
- Large-scale data processing pipelines
- Organization-wide reporting

**Agent design rules:**
- Each sub-team should be self-contained
- Define clear interfaces between sub-teams
- Limit to 2 levels of hierarchy (3 max)
- Each sub-team can use any of the above patterns

**Team mode suitability:** Medium — requires nested `TeamCreate` calls.

---

## Pattern-to-Use-Case Quick Reference

| Pattern | Best For | Agent Count | Complexity | Token Cost |
|---------|----------|-------------|------------|------------|
| Pipeline | Sequential processes | 3-5 | Low | Low |
| Fan-out/Fan-in | Parallel analysis | 3-6 | Medium | Medium-High |
| Expert Pool | Routing by type | 3-8 | Medium | Low-Medium |
| Producer-Reviewer | Quality-critical output | 2-3 | Low | Medium |
| Supervisor | Dynamic coordination | 3-6 | High | Medium |
| Hierarchical | Enterprise-scale | 5-8 | Very High | High |

## Combining Patterns

Most real-world harnesses combine patterns:

- **Pipeline + Producer-Reviewer:** Each pipeline stage has its own reviewer
- **Fan-out + Pipeline:** Parallel initial analysis, then sequential processing
- **Supervisor + Expert Pool:** Supervisor routes to expert sub-teams

When combining, keep total agent count under 8 to manage context costs.
