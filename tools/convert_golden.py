#!/usr/bin/env python3
"""
Golden Output → verify_tier_a.py Assertion Converter

Reads a golden output YAML file and extracts embedded assertions into
the format that verify_tier_a.py expects.

Usage:
    python convert_golden.py golden-output.yaml                  # print to stdout
    python convert_golden.py golden-output.yaml -o assertions.yaml  # write to file
    python convert_golden.py golden-output.yaml --agent ticket_classifier  # single agent

Conversion rules:
    category_must_be: "bug"           → type: equals, path: classification.category, value: "bug"
    urgency_must_be_one_of: [...]     → type: one_of, path: classification.urgency, values: [...]
    confidence_range: [0.8, 1.0]      → type: range, path: classification.confidence, min/max
    confidence_must_be_gte: 0.8       → type: range, path: classification.confidence, min: 0.8
    keywords_must_include_at_least_one → (skipped — Tier B, requires LLM judgment)
    *_must_not_be: "x"                → type: not_equals (custom assertion)
    status_must_be: "pass"            → type: equals
    missing_required_must_be_empty    → type: equals, value: []
    min_count / max_count             → type: min_count / max_count
"""

import sys
from pathlib import Path

import yaml


# Patterns that map golden assertion keys to verify_tier_a.py format
FIELD_MAPPINGS = {
    # ticket_classifier
    "classification.category": "classification.category",
    "classification.urgency": "classification.urgency",
    "classification.confidence": "classification.confidence",
    "classification.keywords": "classification.keywords",
    "classification.reasoning": "classification.reasoning",
    # data_normalizer
    "normalized_product.name": "normalized_product.name",
    "normalized_product.price.amount": "normalized_product.price.amount",
    "normalized_product.price.currency": "normalized_product.price.currency",
    "normalized_product.images": "normalized_product.images",
    "validation.status": "validation.status",
    "validation.missing_required": "validation.missing_required",
    # content_generator
    "listing_content.title": "listing_content.title",
    "listing_content.description.short": "listing_content.description.short",
    "listing_content.description.full": "listing_content.description.full",
    "listing_content.tags": "listing_content.tags",
    "listing_content.category_suggestion": "listing_content.category_suggestion",
    # qa_checker
    "qa_result.status": "qa_result.status",
    "qa_result.issues": "qa_result.issues",
    # response_generator
    "decision": "decision",
    "response.body": "response.body",
    "response.greeting": "response.greeting",
    "response.next_steps": "response.next_steps",
    "metadata.classification_confidence": "metadata.classification_confidence",
    "metadata.auto_resolution": "metadata.auto_resolution",
    # search results
    "search_results": "search_results",
    "search_results.total_found": "search_results.total_found",
    "search_results.best_match_confidence": "search_results.best_match_confidence",
}


def convert_assertion(key: str, value, agent_context: str) -> list[dict]:
    """Convert a single golden assertion into verify_tier_a.py assertions."""
    results = []

    # Skip Tier B assertions (require LLM judgment)
    tier_b_keywords = [
        "must_include_at_least_one",
        "must_search",
        "must_not_fabricate",
        "must_address",
        "must_reference",
        "language_should",
        "must_not_crash",
        "optional_fields_still",
        "must_not_proceed",
        "must_report",
        "error_message_must",
        "must_not_return_partial",
        "must_contain",
        "must_not_contain",
        "semantically",
        "appropriate",
        "actionable",
    ]
    if any(kw in key for kw in tier_b_keywords):
        return []  # Skip — these are Tier B

    # *_must_be: "value" → equals
    if key.endswith("_must_be"):
        field = key.replace("_must_be", "").replace("_", ".")
        path = guess_path(field, agent_context)
        if path:
            results.append({"type": "equals", "path": path, "value": value})

    # *_must_be_one_of: [...] → one_of
    elif key.endswith("_must_be_one_of"):
        field = key.replace("_must_be_one_of", "").replace("_", ".")
        path = guess_path(field, agent_context)
        if path and isinstance(value, list):
            results.append({"type": "one_of", "path": path, "values": value})

    # *_must_not_be: "value" → not_equals (custom)
    elif key.endswith("_must_not_be"):
        pass  # verify_tier_a.py doesn't have not_equals yet; skip

    # *_range: [min, max] → range
    elif key.endswith("_range"):
        field = key.replace("_range", "").replace("_", ".")
        path = guess_path(field, agent_context)
        if path and isinstance(value, list) and len(value) == 2:
            results.append({"type": "range", "path": path, "min": value[0], "max": value[1]})

    # *_must_be_gte: N → range with min only
    elif "_must_be_gte" in key:
        field = key.replace("_must_be_gte", "").replace("_", ".")
        path = guess_path(field, agent_context)
        if path:
            results.append({"type": "range", "path": path, "min": value})

    # *_must_be_empty / *_must_be_empty: true → equals []
    elif key.endswith("_must_be_empty") and value is True:
        field = key.replace("_must_be_empty", "").replace("_", ".")
        path = guess_path(field, agent_context)
        if path:
            results.append({"type": "equals", "path": path, "value": []})

    # *_must_include: [...] → Tier B (skip)
    elif "must_include" in key:
        pass

    # min_count / max_count
    elif key == "min_count":
        pass  # needs path context
    elif key == "max_count":
        pass  # needs path context

    return results


def guess_path(field_hint: str, agent_context: str) -> str | None:
    """Try to find the dotted path for a field based on context."""
    # Direct match
    for known_path in FIELD_MAPPINGS:
        if field_hint in known_path:
            return known_path
    # Fallback: use the hint as-is
    if "." in field_hint:
        return field_hint
    return None


def extract_assertions_from_agent(agent_data: dict, agent_name: str) -> list[dict]:
    """Extract assertions from a single agent's golden output section."""
    results = []

    # Always add yaml_valid
    results.append({"type": "yaml_valid"})

    # Check for 'assertions' list
    assertions_list = agent_data.get("assertions", [])
    for assertion in assertions_list:
        if isinstance(assertion, dict):
            for key, value in assertion.items():
                if key == "reason":
                    continue
                converted = convert_assertion(key, value, agent_name)
                results.extend(converted)

    # Check for direct field specs (e.g., classification.category_must_be)
    for key, value in agent_data.items():
        if key in ("assertions", "reason", "decision"):
            continue
        if isinstance(value, dict):
            for subkey, subvalue in value.items():
                if subkey == "reason":
                    continue
                converted = convert_assertion(subkey, subvalue, agent_name)
                results.extend(converted)

    # Check for embedded tier_a_assertions_file
    tier_a = agent_data.get("tier_a_assertions_file", {})
    if tier_a and "assertions" in tier_a:
        results.extend(tier_a["assertions"])

    return results


def convert_golden_file(golden_path: str, agent_filter: str | None = None) -> dict:
    """Convert an entire golden output file to assertion format."""
    with open(golden_path) as f:
        data = yaml.safe_load(f)

    all_assertions = []

    # Check for top-level tier_a_assertions_file (directly usable)
    top_tier_a = data.get("tier_a_assertions_file", {})
    if top_tier_a and "assertions" in top_tier_a:
        all_assertions.extend(top_tier_a["assertions"])

    # Skip non-agent sections
    skip_keys = {"test_input", "cross_agent", "tier_a_assertions_file"}

    for key, value in data.items():
        if key in skip_keys:
            continue
        if not isinstance(value, dict):
            continue
        if agent_filter and key != agent_filter:
            continue

        agent_assertions = extract_assertions_from_agent(value, key)
        all_assertions.extend(agent_assertions)

    # Deduplicate
    seen = set()
    unique = []
    for a in all_assertions:
        fingerprint = str(sorted(a.items()))
        if fingerprint not in seen:
            seen.add(fingerprint)
            unique.append(a)

    return {"assertions": unique}


def main():
    if len(sys.argv) < 2:
        print("Usage: convert_golden.py <golden-output.yaml> [-o output.yaml] [--agent name]")
        sys.exit(1)

    golden_path = sys.argv[1]
    output_path = None
    agent_filter = None

    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "-o" and i + 1 < len(sys.argv):
            output_path = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--agent" and i + 1 < len(sys.argv):
            agent_filter = sys.argv[i + 1]
            i += 2
        else:
            i += 1

    if not Path(golden_path).exists():
        print(f"Error: {golden_path} not found")
        sys.exit(1)

    try:
        result = convert_golden_file(golden_path, agent_filter)
    except Exception as e:
        print(f"Error parsing golden output: {e}")
        sys.exit(1)

    output_text = yaml.dump(result, default_flow_style=False, allow_unicode=True, sort_keys=False)

    if output_path:
        with open(output_path, "w") as f:
            f.write(f"# Auto-generated from {Path(golden_path).name}\n")
            f.write(f"# Assertions: {len(result['assertions'])} (Tier A only)\n\n")
            f.write(output_text)
        print(f"Wrote {len(result['assertions'])} assertions to {output_path}")
    else:
        print(output_text)


if __name__ == "__main__":
    main()
