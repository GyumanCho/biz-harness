# Execution Trace: UC-SAAS-03 Ticket Classifier

A real Phase 5 execution trace showing the actual Agent tool call, real response,
Tier A script verification, and Tier B evaluation. This is not hypothetical —
every output below was captured from a live run.

## Step 1: Agent Invocation

**Tool used:** Agent tool with `model: sonnet`

**Prompt sent to agent:**
```
You are a customer support ticket classifier. Classify the following ticket.

Input:
- subject: "Cannot export data to CSV"
- body: "I'm trying to export my project data to CSV from the dashboard but
  the export button shows a spinner for about 30 seconds and then nothing
  happens. No file is downloaded. I've tried Chrome and Firefox. This worked
  fine last week."
- customer_context: account_type=pro, tenure_months=14

Return YAML in exactly this format:
classification:
  category: "bug | feature_request | how_to | billing | account | other"
  urgency: "critical | high | medium | low"
  confidence: 0.0-1.0
  reasoning: "One sentence explaining the classification"
  keywords: ["extracted", "relevant", "terms"]
```

## Step 2: Actual Agent Response (verbatim)

```yaml
classification:
  category: "bug"
  urgency: "high"
  confidence: 0.95
  reasoning: "A previously working export feature is now silently failing across multiple browsers for a paying Pro user, blocking data access workflows."
  keywords: ["export", "CSV", "spinner", "no download", "dashboard", "Chrome", "Firefox", "regression"]
```

## Step 3: Tier A Verification (via verify_tier_a.py)

**Command:**
```bash
python3 tools/verify_tier_a.py trace-classifier-output.yaml sample-assertions.yaml
```

**Output (verbatim from script execution):**
```
Tier A Verification: 14/14 (100.0%)

#    Result   Type           Path                                Evidence
------------------------------------------------------------------------------------------
1    PASS     yaml_valid     -                                   Valid YAML dict
2    PASS     field_exists   classification                      Found: classification
3    PASS     field_exists   classification.category             Found: classification.category
4    PASS     field_exists   classification.urgency              Found: classification.urgency
5    PASS     field_exists   classification.confidence           Found: classification.confidence
6    PASS     field_exists   classification.reasoning            Found: classification.reasoning
7    PASS     field_exists   classification.keywords             Found: classification.keywords
8    PASS     one_of         classification.category             classification.category = 'bug', valid: ['bug', 'feature_request', 'how_to', 'billing', 'account', 'other']
9    PASS     one_of         classification.urgency              classification.urgency = 'high', valid: ['critical', 'high', 'medium', 'low']
10   PASS     range          classification.confidence           classification.confidence = 0.95, range [0.0, 1.0]
11   PASS     is_type        classification.confidence           classification.confidence: type=float, expected=float
12   PASS     is_type        classification.keywords             classification.keywords: type=list, expected=list
13   PASS     not_empty      classification.reasoning            classification.reasoning = 'A previously working export feature is now silently failing across multiple browsers for a paying Pro user, blocking data access workflows.'
14   PASS     not_empty      classification.keywords             classification.keywords = ['export', 'CSV', 'spinner', 'no download', 'dashboard', 'Chrome', 'Firefox', 'regression']
```

**Result:** 14/14 Tier A assertions PASS. Exit code 0.

This verification required ZERO LLM judgment. The Python script parsed the YAML,
checked field existence, validated types, confirmed value ranges, and verified
enum membership. Every check is deterministic and reproducible.

## Step 4: Tier B Evaluation (LLM-judged)

These assertions require understanding meaning, not just structure.

| Assertion | Result | Evidence | Reasoning |
|-----------|--------|----------|-----------|
| category_matches_expected: "bug" | PASS | category = "bug" | Correct — customer reports broken functionality that previously worked |
| urgency_matches_expected: "high" | PASS | urgency = "high" | Correct — major feature broken, blocking workflow |
| confidence_gte_0.8 | PASS | confidence = 0.95 | High confidence appropriate for clear bug report |
| keywords_include_export_term | PASS | "export" in keywords | Core issue term extracted |
| reasoning_addresses_regression | PASS | "previously working" in reasoning | Correctly identified this as a regression |

**Tier B: 5/5 PASS**

**Honesty note:** These 5 checks required me (the LLM) to judge whether the
classification is correct for this input. The expected values ("bug", "high")
come from the golden output `UC-SAAS-03-happy-path.yaml`, which was authored
in advance. For non-golden use cases, these expected values would be generated
at runtime, introducing circular evaluation risk.

## Step 5: Golden Output Comparison

Comparing against `references/golden-outputs/UC-SAAS-03-happy-path.yaml`:

| Golden Assertion | Real Output | Match |
|------------------|-------------|-------|
| category_must_be: "bug" | category: "bug" | YES |
| urgency_must_be_one_of: ["high", "critical"] | urgency: "high" | YES |
| confidence_range: [0.8, 1.0] | confidence: 0.95 | YES |
| keywords_must_include "export" | keywords includes "export" | YES |

**Structural match: 4/4 (100%)**

## Step 6: Score Calculation

**Completeness (Tier A only):**
- trigger_handler_exists: PASS
- classifier_agent_exists: PASS
- → 2/2 = 100

**Accuracy (Tier A + Tier B + Golden):**
- Tier A format checks: 14/14
- Tier B decision checks: 5/5
- Golden structural match: 4/4
- → 23/23 = 100

**Consistency (run twice):**
- Run 1 category: "bug" | Run 2 category: "bug" → MATCH
- Run 1 urgency: "high" | Run 2 urgency: "high" → MATCH
- Run 1 confidence: 0.95 | Run 2 confidence: 0.93 → MATCH (within 5%)
- → 3/3 = 100

**Performance (Tier A):**
- Agent invocations: 1 (single classifier) → PASS
- → 1/1 = 100

**Business Fit (Tier B):**
- Correctly identified as bug (not "how_to"): PASS
- Urgency appropriate for blocking issue: PASS
- → 2/2 = 100

**Base score: 100**
No adversarial review in this trace (Quick mode).

**Final: 100/100 EXCELLENT (single agent, Quick mode)**

## Key Takeaway

This trace demonstrates the separation between Tier A and Tier B:

- **Tier A (steps 3):** Python script, deterministic, reproducible, zero LLM involvement.
  If you run the same script on the same YAML file tomorrow, you get the same result.

- **Tier B (step 4):** LLM reads the output, judges correctness against golden output.
  The judgment is structured (binary assertions, not subjective scoring) but still
  requires model evaluation. Reported separately for transparency.

A user who only trusts machine-verified results can look at Tier A alone (14/14 = 100%).
A user who also values decision quality can include Tier B (5/5, but with the caveat
that these are LLM-judged). The Score Card always shows both.
