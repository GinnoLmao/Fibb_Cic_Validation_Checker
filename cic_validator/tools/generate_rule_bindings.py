"""One-time rule-binding pass over the CIC error rulebook.

Reads schema/record_type_field_schema.json (annotated) and schema/error_rules_consolidated.json,
attempts to bind each rule to a schema field + primitive, and writes:

- schema/rule_bindings.json      : confidently auto-bound rules
- schema/unmapped_rules.json     : rules that could not be bound automatically

Run from the project root:
    .venv\\Scripts\\python.exe -m cic_validator.tools.generate_rule_bindings
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "cic_validator" / "schema" / "record_type_field_schema.json"
RULES_PATH = ROOT / "cic_validator" / "schema" / "error_rules_consolidated.json"
BINDINGS_PATH = ROOT / "cic_validator" / "schema" / "rule_bindings.json"
UNMAPPED_PATH = ROOT / "cic_validator" / "schema" / "unmapped_rules.json"

FIELD_RE = re.compile(r"FIELD '([^']+)'")
FIELDS_RE = re.compile(r"FIELDS '([^']+)' (?:AND|OR) '([^']+)'")


def normalize(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", name.lower())


def load_schema() -> dict:
    with SCHEMA_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_rules() -> list[dict]:
    with RULES_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def build_field_index(schema: dict) -> dict[str, list[tuple[str, dict]]]:
    """Map normalized field name -> list of (record_type, field)."""
    index: dict[str, list[tuple[str, dict]]] = {}
    for rt, spec in schema.items():
        for field in spec["fields"]:
            index.setdefault(normalize(field["name"]), []).append((rt, field))
            # Allow matching by base name after block prefix
            base = field["name"].split(": ")[-1]
            if normalize(base) != normalize(field["name"]):
                index.setdefault(normalize(base), []).append((rt, field))
    return index


def lookup_field(field_name: str, record_type: str | None, index: dict) -> tuple[str, dict] | None:
    norm = normalize(field_name)
    candidates = index.get(norm, [])
    if record_type:
        candidates = [(rt, f) for rt, f in candidates if rt == record_type]
    if not candidates:
        return None
    return candidates[0]


def infer_primitive(rule: dict, field: dict | None) -> str | None:
    desc = rule["description"].upper()
    if "IS MANDATORY" in desc:
        return "required"
    if "LENGTH IS NOT CORRECT" in desc:
        return "max_length"
    if "IS NOT NUMERIC OR LENGTH IS NOT CORRECT" in desc:
        return "numeric_and_length"
    if "IS NOT CORRECT" in desc:
        if field and field.get("data_type") == "date":
            return "date_format"
        return "domain_lookup"
    if "CANNOT BE BOTH EMPTY OR FILLED IN" in desc:
        return "paired_fields"
    if "MUST BE GREATER THAN" in desc and field and field.get("data_type") == "date":
        return "date_min"
    if "CAN HAVE ONLY A >0 VALUE" in desc or "CAN ONLY HAVE A > 0 VALUE" in desc:
        return "numeric_min"
    if "CAN HAVE ONLY A VALUE >0 OR =0" in desc:
        return "numeric_min"
    if "AGE SHOULD BE BETWEEN" in desc:
        return "numeric_range"
    if desc.startswith("AT LEAST ONE") or "AT LEAST ONE BETWEEN" in desc:
        return "at_least_one_of"
    if "NUMBER OF FIELDS IS NOT VALID" in desc:
        return "field_count"
    if "RECORD TYPE IS NOT VALID" in desc:
        return "record_type_valid"
    if "FILENAME FORMAT IS NOT VALID" in desc:
        return "filename_format"
    if "PROVIDER CODE" in desc and ("FILENAME" in desc or "INSIDE THE FILE" in desc):
        return "provider_code_consistency"
    if "ALREADY ASSIGNED TO ANOTHER SUBJECT" in desc:
        return "cross_record_unique"
    return None


def generate_bindings() -> tuple[list[dict], list[dict]]:
    schema = load_schema()
    rules = load_rules()
    index = build_field_index(schema)

    bindings: list[dict] = []
    unmapped: list[dict] = []
    used_codes: set[str] = set()

    structural_prefixes = {"3", "30", "40"}

    for rule in rules:
        code = rule["error_code"]
        desc = rule["description"]
        prefix = rule["category_prefix"]

        # Structural / file-level rules: bind generically without a field.
        if prefix in structural_prefixes or code in {"1-105", "1-119", "1-120", "1-121", "1-128", "1-097"}:
            primitive = None
            if "NUMBER OF FIELDS IS NOT VALID" in desc:
                primitive = "field_count"
            elif "RECORD TYPE IS NOT VALID" in desc:
                primitive = "record_type_valid"
            elif "FILENAME FORMAT" in desc or "TIMESTAMP" in desc:
                primitive = "filename_format"
            elif "PROVIDER CODE" in desc and ("FILENAME" in desc or "INSIDE THE FILE" in desc):
                primitive = "provider_code_consistency"
            elif "HEADER IS NOT PRESENT" in desc or "MORE THAN ONE HEADER" in desc:
                primitive = "header_footer"
            elif "FOOTER IS NOT PRESENT" in desc:
                primitive = "header_footer"
            elif "CHARACTER SET" in desc or "UTF-8" in desc:
                primitive = "encoding"
            elif "SERVICE CODE" in desc:
                primitive = "domain_lookup"
            elif "VERSION" in desc:
                primitive = "version"

            if primitive:
                bindings.append(
                    {
                        "error_code": code,
                        "record_types": ["*"],
                        "field_name": None,
                        "field_names": None,
                        "primitive": primitive,
                        "params": {},
                        "description": desc,
                        "fix": rule.get("rephrased_fix") or rule.get("solution") or "",
                    }
                )
                used_codes.add(code)
                continue

        # Extract quoted field names
        quoted = FIELD_RE.findall(desc)
        if not quoted:
            unmapped.append(
                {
                    "error_code": code,
                    "description": desc,
                    "reason_unmapped": "No FIELD '...' name found in description",
                }
            )
            continue

        # Single-field rules
        if len(quoted) == 1:
            field_name = quoted[0]
            match = lookup_field(field_name, None, index)
            if not match:
                unmapped.append(
                    {
                        "error_code": code,
                        "description": desc,
                        "reason_unmapped": f"Field '{field_name}' not found in schema",
                    }
                )
                continue
            rt, field = match
            primitive = infer_primitive(rule, field)
            if not primitive:
                unmapped.append(
                    {
                        "error_code": code,
                        "description": desc,
                        "reason_unmapped": "Could not infer primitive from description",
                    }
                )
                continue
            binding = {
                "error_code": code,
                "record_types": [rt],
                "field_name": field["name"],
                "field_names": None,
                "primitive": primitive,
                "params": {},
                "description": desc,
                "fix": rule.get("rephrased_fix") or rule.get("solution") or "",
            }
            if primitive in ("domain_lookup", "date_format"):
                binding["params"]["domain"] = field.get("domain")
            if primitive == "max_length":
                binding["params"]["max_length"] = field.get("max_length")
            if primitive == "numeric_and_length":
                binding["params"]["max_length"] = field.get("max_length")
            bindings.append(binding)
            used_codes.add(code)
            continue

        # Multi-field rules (e.g. paired fields)
        matches = [lookup_field(fn, None, index) for fn in quoted]
        if any(m is None for m in matches):
            missing = [q for q, m in zip(quoted, matches) if m is None]
            unmapped.append(
                {
                    "error_code": code,
                    "description": desc,
                    "reason_unmapped": f"One or more fields not found in schema: {missing}",
                }
            )
            continue
        record_types = {m[0] for m in matches}
        primitive = infer_primitive(rule, None)
        if not primitive or primitive not in {"paired_fields", "at_least_one_of", "cross_record_unique"}:
            unmapped.append(
                {
                    "error_code": code,
                    "description": desc,
                    "reason_unmapped": "Could not infer multi-field primitive",
                }
            )
            continue
        bindings.append(
            {
                "error_code": code,
                "record_types": sorted(record_types),
                "field_name": None,
                "field_names": [m[1]["name"] for m in matches],
                "primitive": primitive,
                "params": {},
                "description": desc,
                "fix": rule.get("rephrased_fix") or rule.get("solution") or "",
            }
        )
        used_codes.add(code)

    return bindings, unmapped


def main() -> None:
    bindings, unmapped = generate_bindings()
    with BINDINGS_PATH.open("w", encoding="utf-8") as f:
        json.dump(bindings, f, indent=2, ensure_ascii=False)
    with UNMAPPED_PATH.open("w", encoding="utf-8") as f:
        json.dump(unmapped, f, indent=2, ensure_ascii=False)
    print(f"Bindings: {len(bindings)}; unmapped: {len(unmapped)}")
    print(f"Written to {BINDINGS_PATH} and {UNMAPPED_PATH}")


if __name__ == "__main__":
    main()
