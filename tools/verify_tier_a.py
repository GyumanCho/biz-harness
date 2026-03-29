#!/usr/bin/env python3
"""
BizHarness Tier A Assertion Verifier

Deterministically validates agent output YAML against Tier A assertions.
No LLM judgment — pure structural checks.

Usage:
    python verify_tier_a.py output.yaml assertions.yaml
    python verify_tier_a.py output.yaml assertions.yaml --json

Assertion file format (YAML):
    assertions:
      - type: field_exists
        path: "classification.category"
      - type: one_of
        path: "classification.category"
        values: ["bug", "feature_request", "how_to", "billing", "account", "other"]
      - type: range
        path: "classification.confidence"
        min: 0.0
        max: 1.0
      - type: max_length
        path: "response.body"
        value: 200  # words
        unit: words
      - type: is_type
        path: "classification.confidence"
        expected: float
      - type: not_empty
        path: "classification.keywords"
      - type: yaml_valid
"""

import json
import sys
from pathlib import Path

import yaml


def load_yaml(path: str) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def resolve_path(data: dict, path: str):
    """Navigate dotted path like 'classification.category' into nested dict."""
    keys = path.split(".")
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return None, False
    return current, True


def count_words(text: str) -> int:
    return len(str(text).split())


def check_assertion(data: dict, assertion: dict) -> dict:
    atype = assertion["type"]
    path = assertion.get("path", "")
    result = {"assertion": assertion, "passed": False, "evidence": ""}

    if atype == "yaml_valid":
        result["passed"] = isinstance(data, dict) and len(data) > 0
        result["evidence"] = "Valid YAML dict" if result["passed"] else "Not a valid YAML dict"
        return result

    value, found = resolve_path(data, path)

    if atype == "field_exists":
        result["passed"] = found
        result["evidence"] = f"{'Found' if found else 'Missing'}: {path}"

    elif atype == "not_empty":
        result["passed"] = found and value is not None and value != "" and value != []
        result["evidence"] = f"{path} = {repr(value)}" if found else f"Missing: {path}"

    elif atype == "one_of":
        valid = assertion["values"]
        result["passed"] = found and value in valid
        result["evidence"] = (
            f"{path} = {repr(value)}, valid: {valid}"
            if found
            else f"Missing: {path}"
        )

    elif atype == "range":
        lo, hi = assertion.get("min"), assertion.get("max")
        if found and isinstance(value, (int, float)):
            in_range = (lo is None or value >= lo) and (hi is None or value <= hi)
            result["passed"] = in_range
            result["evidence"] = f"{path} = {value}, range [{lo}, {hi}]"
        else:
            result["evidence"] = f"{path} = {repr(value)}, expected numeric"

    elif atype == "max_length":
        limit = assertion["value"]
        unit = assertion.get("unit", "chars")
        if found and value is not None:
            length = count_words(str(value)) if unit == "words" else len(str(value))
            result["passed"] = length <= limit
            result["evidence"] = f"{path}: {length} {unit} (max {limit})"
        else:
            result["evidence"] = f"Missing: {path}"

    elif atype == "min_length":
        limit = assertion["value"]
        unit = assertion.get("unit", "chars")
        if found and value is not None:
            length = count_words(str(value)) if unit == "words" else len(str(value))
            result["passed"] = length >= limit
            result["evidence"] = f"{path}: {length} {unit} (min {limit})"
        else:
            result["evidence"] = f"Missing: {path}"

    elif atype == "is_type":
        expected = assertion["expected"]
        type_map = {
            "str": str, "string": str,
            "int": int, "integer": int,
            "float": (int, float), "number": (int, float),
            "list": list, "array": list,
            "dict": dict, "object": dict,
            "bool": bool, "boolean": bool,
        }
        expected_type = type_map.get(expected)
        if found and expected_type:
            result["passed"] = isinstance(value, expected_type)
            result["evidence"] = f"{path}: type={type(value).__name__}, expected={expected}"
        else:
            result["evidence"] = f"Missing: {path}" if not found else f"Unknown type: {expected}"

    elif atype == "equals":
        expected_val = assertion["value"]
        result["passed"] = found and value == expected_val
        result["evidence"] = f"{path} = {repr(value)}, expected {repr(expected_val)}"

    elif atype == "min_count":
        limit = assertion["value"]
        if found and isinstance(value, list):
            result["passed"] = len(value) >= limit
            result["evidence"] = f"{path}: {len(value)} items (min {limit})"
        else:
            result["evidence"] = f"{path} is not a list or missing"

    elif atype == "max_count":
        limit = assertion["value"]
        if found and isinstance(value, list):
            result["passed"] = len(value) <= limit
            result["evidence"] = f"{path}: {len(value)} items (max {limit})"
        else:
            result["evidence"] = f"{path} is not a list or missing"

    else:
        result["evidence"] = f"Unknown assertion type: {atype}"

    return result


def run_verification(output_path: str, assertions_path: str) -> dict:
    try:
        data = load_yaml(output_path)
    except Exception as e:
        return {
            "status": "error",
            "error": f"Failed to parse output YAML: {e}",
            "passed": 0,
            "failed": 0,
            "total": 0,
            "results": [],
        }

    spec = load_yaml(assertions_path)
    assertions = spec.get("assertions", [])

    results = [check_assertion(data, a) for a in assertions]
    passed = sum(1 for r in results if r["passed"])
    failed = len(results) - passed

    return {
        "status": "complete",
        "passed": passed,
        "failed": failed,
        "total": len(results),
        "pass_rate": round(passed / len(results) * 100, 1) if results else 0,
        "results": results,
    }


def format_table(report: dict) -> str:
    lines = [
        f"\nTier A Verification: {report['passed']}/{report['total']} "
        f"({report['pass_rate']}%)\n",
        f"{'#':<4} {'Result':<8} {'Type':<14} {'Path':<35} Evidence",
        "-" * 90,
    ]
    for i, r in enumerate(report["results"], 1):
        a = r["assertion"]
        mark = "PASS" if r["passed"] else "FAIL"
        lines.append(
            f"{i:<4} {mark:<8} {a['type']:<14} {a.get('path', '-'):<35} {r['evidence']}"
        )
    if report["failed"] > 0:
        lines.append(f"\n{report['failed']} FAILED assertion(s):")
        for r in report["results"]:
            if not r["passed"]:
                a = r["assertion"]
                lines.append(f"  - [{a['type']}] {a.get('path', '-')}: {r['evidence']}")
    return "\n".join(lines)


def main():
    if len(sys.argv) < 3:
        print("Usage: verify_tier_a.py <output.yaml> <assertions.yaml> [--json]")
        sys.exit(1)

    output_path = sys.argv[1]
    assertions_path = sys.argv[2]
    json_mode = "--json" in sys.argv

    if not Path(output_path).exists():
        print(f"Error: {output_path} not found")
        sys.exit(1)
    if not Path(assertions_path).exists():
        print(f"Error: {assertions_path} not found")
        sys.exit(1)

    report = run_verification(output_path, assertions_path)

    if json_mode:
        print(json.dumps(report, indent=2, default=str))
    else:
        print(format_table(report))

    sys.exit(0 if report["failed"] == 0 else 1)


if __name__ == "__main__":
    main()
