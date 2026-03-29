# QA Scenario Templates

Templates for generating E2E test scenarios from business use cases.
Each use case should produce 3-8 scenarios covering happy path, edge cases,
and failure modes.

## Scenario Generation Process

1. Read the use case definition (steps, actors, outcome)
2. Generate Happy Path scenario first
3. For each step, ask: "What could go wrong?" → Failure scenarios
4. For each input, ask: "What are the boundaries?" → Edge cases
5. Assign quality axis weights to each scenario

## Scenario Structure

```yaml
scenario_id: "{UC-ID}-S{number}"
name: "{Descriptive name}"
type: "happy_path | edge_case | failure"
use_case: "{UC-ID}"
description: "{What this scenario validates}"

preconditions:
  - "{State that must be true before execution}"

input:
  data: "{Concrete example input data}"
  context: "{Additional context the agents receive}"

steps:
  - agent: "{Agent role name}"
    action: "{What the agent should do}"
    expected_output: "{What the agent should produce}"
    success_criteria: "{How to judge if this step passed}"

expected_outcome: "{Final result of the complete scenario}"

quality_axes_tested:
  primary: "{Which axis this scenario tests most}"
  secondary: "{Second axis tested}"

severity: "critical | major | minor"
```

---

## Template: Happy Path

The normal, expected flow where everything works correctly.

**Generation rules:**
- Follow the use case steps exactly in order
- Use typical, valid input data
- All agents succeed on first attempt
- Expected outcome matches the use case's defined outcome

```yaml
scenario_id: "{UC-ID}-S01"
name: "Happy Path - {Use Case Name}"
type: happy_path
description: "Normal flow with valid inputs and all agents succeeding"

preconditions:
  - "System is in normal operating state"
  - "All required data sources are available"
  - "Input data meets all validation requirements"

input:
  data: "{Typical valid input for this use case}"
  context: "{Standard operating context}"

steps:
  - agent: "{First agent in the flow}"
    action: "{Process the trigger}"
    expected_output: "{Valid intermediate result}"
    success_criteria: "{Specific measurable check}"
  # ... one step per use case action

expected_outcome: "{Matches use case outcome definition}"

quality_axes_tested:
  primary: completeness
  secondary: accuracy

severity: critical
```

---

## Template: Edge Cases

Boundary conditions, unusual but valid inputs, optional paths.

### Edge Case Categories

**Input boundaries:**
- Minimum valid input (single item, shortest string, smallest number)
- Maximum valid input (bulk data, longest string, largest number)
- Unicode/special characters in text inputs
- Empty optional fields

**Timing boundaries:**
- Request at system boundary times (midnight, month-end)
- Concurrent requests for same resource
- Request immediately after system restart

**State boundaries:**
- First-time user (no history)
- Power user (extensive history)
- User at plan limits
- Partially completed previous run

```yaml
scenario_id: "{UC-ID}-S02"
name: "Edge - {Specific boundary being tested}"
type: edge_case
description: "Tests {boundary condition} to verify graceful handling"

preconditions:
  - "{Specific state that creates the edge condition}"

input:
  data: "{Boundary input data}"
  context: "{What makes this edge-case-y}"

steps:
  - agent: "{Agent that encounters the boundary}"
    action: "{How it should handle the boundary}"
    expected_output: "{Correct handling of edge case}"
    success_criteria: "{No errors, graceful degradation, or correct adaptation}"

expected_outcome: "{Acceptable result — may differ from happy path}"

quality_axes_tested:
  primary: accuracy
  secondary: consistency

severity: major
```

---

## Template: Failure Scenarios

What happens when things go wrong. Tests resilience and error handling.

### Failure Categories

**Agent failures:**
- Agent times out
- Agent returns malformed output
- Agent returns low-confidence result

**Data failures:**
- Required data source unavailable
- Input data fails validation
- Stale or outdated reference data

**Dependency failures:**
- External API timeout
- Authentication expired
- Rate limit exceeded

**Business rule violations:**
- Input violates business constraints
- Requested action conflicts with policies
- Insufficient permissions

```yaml
scenario_id: "{UC-ID}-S03"
name: "Failure - {What fails and how}"
type: failure
description: "Tests system behavior when {specific failure occurs}"

preconditions:
  - "{Normal preconditions}"
  - "{Condition that will cause the failure}"

input:
  data: "{Input that triggers or accompanies the failure}"
  context: "{Failure condition details}"

steps:
  - agent: "{Agent that encounters the failure}"
    action: "{Attempt normal processing}"
    expected_output: "{Error detection and handling}"
    success_criteria: "{Failure is caught, not silently ignored}"
  - agent: "{Fallback or escalation agent}"
    action: "{Handle the failure gracefully}"
    expected_output: "{Appropriate fallback response}"
    success_criteria: "{User/system is not left in broken state}"

expected_outcome: "{Graceful degradation or appropriate escalation}"

quality_axes_tested:
  primary: completeness
  secondary: business_fit

severity: major
```

---

## Scenario Coverage Matrix

After generating scenarios, verify coverage with this matrix:

```markdown
| Use Case Step | Happy Path | Edge Case | Failure | Covered? |
|---------------|:----------:|:---------:|:-------:|:--------:|
| {Step 1}      | S01        | S02       | S04     | YES      |
| {Step 2}      | S01        | S03       | -       | PARTIAL  |
| {Step 3}      | S01        | -         | S05     | YES      |
| {Step N}      | S01        | -         | -       | MINIMAL  |
```

**Coverage requirements:**
- Every step must appear in the Happy Path scenario
- Every step must be covered by at least one additional scenario (edge or failure)
- At least 1 failure scenario per use case
- Critical business steps must have both edge and failure coverage

## Scenario-to-Axis Mapping Guide

| Scenario Type | Primary Axis | Secondary Axis |
|---------------|-------------|----------------|
| Happy Path | Completeness | Accuracy |
| Input Boundary | Accuracy | Consistency |
| Timing Boundary | Consistency | Performance |
| State Boundary | Accuracy | Business Fit |
| Agent Failure | Completeness | Business Fit |
| Data Failure | Accuracy | Completeness |
| Dependency Failure | Completeness | Performance |
| Business Rule Violation | Business Fit | Accuracy |
