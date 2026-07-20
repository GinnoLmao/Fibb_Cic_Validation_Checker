"""Reusable validation-rule primitives."""
from __future__ import annotations

import re
from datetime import datetime
from typing import Iterable

from cic_validator.core.models import FieldError, Record, severity_from_prefix
from cic_validator.core.domain_loader import DomainLoader
from cic_validator.core.rule_loader import RuleLoader


def _find_rule(rule_loader: RuleLoader, pattern: str, field_name: str | None) -> dict | None:
    return rule_loader.find_code(pattern, field_name)


def _prefix(code: str) -> str:
    return code.split("-")[0] if "-" in code else code


def _make_error(
    record: Record,
    field_name: str | None,
    error_code: str,
    description: str,
    fix: str,
    severity: str | None,
    offending_value: str | None = None,
) -> FieldError:
    prefix = _prefix(error_code)
    return FieldError(
        error_code=error_code,
        category_prefix=prefix,
        record_type=record.record_type,
        line_number=record.line_number,
        provider_subject_no=record.provider_subject_no,
        field_name=field_name,
        offending_value=offending_value,
        description=description,
        fix_suggestion=fix,
        severity=severity or severity_from_prefix(prefix),
    )


def required(record: Record, field: dict, rule_loader: RuleLoader) -> FieldError | None:
    name = field["name"]
    value = record.fields.get(name, "")
    if value != "":
        return None
    rule = _find_rule(rule_loader, "IS MANDATORY", name)
    code = rule["error_code"] if rule else "CUSTOM-REQ"
    desc = rule["description"] if rule else f"Field '{name}' is mandatory."
    fix = (
        rule.get("rephrased_fix") or rule.get("solution")
        if rule
        else f"Provide a value for {name}."
    )
    severity = severity_from_prefix(rule["category_prefix"]) if rule else "field"
    return _make_error(record, name, code, desc, fix, severity, offending_value=value)


def required_conditional(
    record: Record,
    field: dict,
    condition_field_name: str,
    condition_values: Iterable[str],
    rule_loader: RuleLoader,
) -> FieldError | None:
    name = field["name"]
    cond_value = record.fields.get(condition_field_name, "")
    if cond_value not in set(condition_values):
        return None
    value = record.fields.get(name, "")
    if value != "":
        return None
    # Try to find a rule specific to this conditional field.
    rule = _find_rule(rule_loader, "IS MANDATORY", name)
    code = rule["error_code"] if rule else "CUSTOM-REQ-COND"
    desc = (
        rule["description"]
        if rule
        else f"Field '{name}' is mandatory when {condition_field_name} is {cond_value}."
    )
    fix = (
        rule.get("rephrased_fix") or rule.get("solution")
        if rule
        else f"Provide a value for {name} because {condition_field_name} is {cond_value}."
    )
    severity = severity_from_prefix(rule["category_prefix"]) if rule else "business_rule"
    return _make_error(record, name, code, desc, fix, severity, offending_value=value)


def max_length(record: Record, field: dict, rule_loader: RuleLoader) -> FieldError | None:
    name = field["name"]
    max_len = field.get("max_length")
    if max_len is None:
        return None
    value = record.fields.get(name, "")
    if value == "" or len(value) <= max_len:
        return None
    rule = _find_rule(rule_loader, "LENGTH IS NOT CORRECT", name)
    code = rule["error_code"] if rule else "CUSTOM-LEN"
    desc = (
        rule["description"]
        if rule
        else f"Field '{name}' exceeds the maximum length of {max_len}."
    )
    fix = (
        rule.get("rephrased_fix") or rule.get("solution")
        if rule
        else f"Shorten {name} to no more than {max_len} characters."
    )
    severity = severity_from_prefix(rule["category_prefix"]) if rule else "field"
    return _make_error(record, name, code, desc, fix, severity, offending_value=value)


def numeric_and_length(record: Record, field: dict, rule_loader: RuleLoader) -> FieldError | None:
    name = field["name"]
    value = record.fields.get(name, "")
    if value == "":
        return None
    max_len = field.get("max_length")
    ok = value.isdigit() and (max_len is None or len(value) <= max_len)
    if ok:
        return None
    rule = _find_rule(rule_loader, "IS NOT NUMERIC OR LENGTH IS NOT CORRECT", name)
    code = rule["error_code"] if rule else "CUSTOM-NUM"
    desc = (
        rule["description"]
        if rule
        else f"Field '{name}' must be numeric and no longer than {max_len} digits."
    )
    fix = (
        rule.get("rephrased_fix") or rule.get("solution")
        if rule
        else f"Enter only digits for {name} (max {max_len})."
    )
    severity = severity_from_prefix(rule["category_prefix"]) if rule else "field"
    return _make_error(record, name, code, desc, fix, severity, offending_value=value)


def _valid_date(value: str) -> bool:
    if not re.fullmatch(r"\d{8}", value):
        return False
    try:
        datetime.strptime(value, "%d%m%Y")
        return True
    except ValueError:
        return False


def date_format(record: Record, field: dict, rule_loader: RuleLoader) -> FieldError | None:
    name = field["name"]
    value = record.fields.get(name, "")
    if value == "" or _valid_date(value):
        return None
    rule = _find_rule(rule_loader, "IS NOT CORRECT", name)
    code = rule["error_code"] if rule else "CUSTOM-DATE"
    desc = (
        rule["description"]
        if rule
        else f"Field '{name}' must be a valid date in DDMMYYYY format."
    )
    fix = (
        rule.get("rephrased_fix") or rule.get("solution")
        if rule
        else f"Use DDMMYYYY format for {name}."
    )
    severity = severity_from_prefix(rule["category_prefix"]) if rule else "field"
    return _make_error(record, name, code, desc, fix, severity, offending_value=value)


def domain_lookup(
    record: Record, field: dict, domain_loader: DomainLoader, rule_loader: RuleLoader
) -> FieldError | None:
    name = field["name"]
    value = record.fields.get(name, "")
    if value == "":
        return None
    domain_key = field.get("domain")
    if not domain_key:
        return None
    if domain_loader.is_valid(domain_key, value):
        return None
    rule = _find_rule(rule_loader, "IS NOT CORRECT", name)
    code = rule["error_code"] if rule else "CUSTOM-DOMAIN"
    desc = (
        rule["description"]
        if rule
        else f"Field '{name}' value '{value}' is not in the allowed domain."
    )
    fix = (
        rule.get("rephrased_fix") or rule.get("solution")
        if rule
        else f"Replace '{value}' with a valid value from the {domain_key} domain."
    )
    severity = severity_from_prefix(rule["category_prefix"]) if rule else "field"
    return _make_error(record, name, code, desc, fix, severity, offending_value=value)


def paired_fields(
    record: Record,
    field_a: str,
    field_b: str,
    error_code: str,
    description: str,
    fix: str,
    severity: str = "business_rule",
) -> FieldError | None:
    a = record.fields.get(field_a, "")
    b = record.fields.get(field_b, "")
    a_empty = a == ""
    b_empty = b == ""
    if a_empty == b_empty:
        return None
    offending = f"{field_a}={a!r}, {field_b}={b!r}"
    return _make_error(
        record,
        None,
        error_code,
        description,
        fix,
        severity,
        offending_value=offending,
    )


def at_least_one_of(
    record: Record,
    fields: list[str],
    error_code: str,
    description: str,
    fix: str,
    severity: str = "business_rule",
) -> FieldError | None:
    if any(record.fields.get(f, "") != "" for f in fields):
        return None
    return _make_error(
        record,
        None,
        error_code,
        description,
        fix,
        severity,
        offending_value="all empty",
    )


def at_least_one_of_values(
    record: Record,
    fields: list[str],
    allowed_values: list[str],
    error_code: str,
    description: str,
    fix: str,
    severity: str = "business_rule",
) -> FieldError | None:
    allowed = {str(v).strip() for v in allowed_values}
    for f in fields:
        if record.fields.get(f, "").strip() in allowed:
            return None
    return _make_error(
        record,
        None,
        error_code,
        description,
        fix,
        severity,
        offending_value=str([record.fields.get(f, "") for f in fields]),
    )


def at_least_one_group_of(
    record: Record,
    alternatives: list[list[str]],
    error_code: str,
    description: str,
    fix: str,
    severity: str = "business_rule",
) -> FieldError | None:
    for group in alternatives:
        if all(record.fields.get(f, "") != "" for f in group):
            return None
    return _make_error(
        record,
        None,
        error_code,
        description,
        fix,
        severity,
        offending_value="address incomplete",
    )


def address_type_if_any(
    record: Record,
    address_fields: list[str],
    type_field: str,
    error_code: str,
    description: str,
    fix: str,
    severity: str = "business_rule",
) -> FieldError | None:
    any_filled = any(record.fields.get(f, "") != "" for f in address_fields if f != type_field)
    type_filled = record.fields.get(type_field, "") != ""
    if not any_filled or type_filled:
        return None
    return _make_error(
        record,
        type_field,
        error_code,
        description,
        fix,
        severity,
        offending_value="",
    )


def numeric_range_from_fields(
    record: Record,
    value: int,
    min_val: int,
    max_val: int,
    field_name: str,
    error_code: str,
    description: str,
    fix: str,
    severity: str = "business_rule",
) -> FieldError | None:
    if min_val <= value <= max_val:
        return None
    return _make_error(
        record,
        field_name,
        error_code,
        description,
        fix,
        severity,
        offending_value=str(value),
    )


def cross_record_unique(
    records: list[Record],
    field_name: str,
    error_code: str,
    description: str,
    fix: str,
) -> list[FieldError]:
    seen: dict[str, Record] = {}
    errors: list[FieldError] = []
    for rec in records:
        value = rec.fields.get(field_name, "")
        if value == "":
            continue
        if value in seen:
            # Error on the duplicate only.
            errors.append(
                _make_error(
                    rec,
                    field_name,
                    error_code,
                    description,
                    fix,
                    "business_rule",
                    offending_value=value,
                )
            )
        else:
            seen[value] = rec
    return errors
