"""Stage 3 — cross-field / business-rule validation."""
from __future__ import annotations

import re
from datetime import datetime

from cic_validator.core.models import FieldError, Record
from cic_validator.core.rule_loader import RuleLoader
from cic_validator.core.schema_loader import SchemaLoader
from cic_validator.core import rule_primitives as primitives


def _rule_or_default(
    rule_loader: RuleLoader,
    code: str,
    default_desc: str,
    default_fix: str,
) -> tuple[str, str, str]:
    rule = rule_loader.get_rule(code)
    if rule:
        return (
            code,
            rule.get("description") or default_desc,
            rule.get("rephrased_fix") or rule.get("solution") or default_fix,
        )
    return code, default_desc, default_fix


def _group_address_fields(fields: list[dict], address_group: str) -> list[str]:
    return [f["name"] for f in fields if f.get("address_group") == address_group]


def _is_address_provided(record: Record, address_fields: list[str], type_field: str | None = None) -> bool:
    """An address is considered provided if at least one sub-field (other than Type) is filled."""
    exclude = {type_field} if type_field else set()
    return any(record.fields.get(f, "") != "" for f in address_fields if f not in exclude)


def validate_business_rules(
    records: list[Record],
    schema: SchemaLoader,
    rule_loader: RuleLoader,
) -> list[FieldError]:
    errors: list[FieldError] = []

    for rec in records:
        if rec.record_type not in schema.record_types():
            continue
        fields = schema.get_fields(rec.record_type)
        group_rules = schema.get_group_rules(rec.record_type)

        for rule in group_rules:
            rt = rule.get("rule_type")
            if rt == "address_completeness":
                ag = rule.get("address_group")
                address_fields = _group_address_fields(fields, ag)
                type_field_name = None
                for f in address_fields:
                    if "Address Type" in f:
                        type_field_name = f
                        break
                if not _is_address_provided(rec, address_fields, type_field_name):
                    continue
                err = primitives.at_least_one_group_of(
                    rec,
                    rule.get("alternatives", []),
                    rule.get("error_code", "CUSTOM-ADDR"),
                    rule.get("message", "Address incomplete"),
                    "Provide the full address or the required address sub-fields.",
                )
                if err:
                    errors.append(err)
            elif rt == "address_type_if_any":
                for ag in rule.get("address_groups", []):
                    address_fields = _group_address_fields(fields, ag)
                    type_field = None
                    for f in address_fields:
                        if "Address Type" in f:
                            type_field = f
                            break
                    if not address_fields or not type_field:
                        continue
                    if not _is_address_provided(rec, address_fields, type_field):
                        continue
                    err = primitives.address_type_if_any(
                        rec,
                        address_fields,
                        type_field,
                        rule.get("error_code", "CUSTOM-ADDRTYPE"),
                        rule.get("message", "Address Type is required when address fields are supplied"),
                        "Provide the Address Type when any address sub-field is filled.",
                    )
                    if err:
                        errors.append(err)
            elif rt == "paired_fields":
                for pair in rule.get("pairs", []):
                    err = primitives.paired_fields(
                        rec,
                        pair[0],
                        pair[1],
                        rule.get("error_code", "CUSTOM-PAIR"),
                        rule.get("message", "Fields must be both empty or both filled"),
                        "Fill both fields or leave both empty.",
                    )
                    if err:
                        errors.append(err)
            elif rt == "at_least_one_of":
                err = primitives.at_least_one_of(
                    rec,
                    rule.get("fields", []),
                    rule.get("error_code", "CUSTOM-ALO"),
                    rule.get("message", "At least one field must be filled"),
                    "Provide at least one of the required fields.",
                )
                if err:
                    errors.append(err)
            elif rt == "at_least_one_of_values":
                err = primitives.at_least_one_of_values(
                    rec,
                    rule.get("fields", []),
                    rule.get("allowed_values", []),
                    rule.get("error_code", "CUSTOM-ALOVAL"),
                    rule.get("message", "At least one field must have an allowed value"),
                    "Provide at least one of the allowed values.",
                )
                if err:
                    errors.append(err)

        # Age range for ID records
        if rec.record_type == "ID":
            age_err = _validate_age(rec, rule_loader)
            if age_err:
                errors.append(age_err)

    # Cross-record uniqueness of Provider Subject No within subject records only.
    subject_records = [r for r in records if r.record_type in {"ID", "BD"}]
    errors.extend(
        primitives.cross_record_unique(
            subject_records,
            "Provider Subject No",
            "10-090",
            "Provider Subject No already assigned to another subject",
            "Ensure each subject has a unique Provider Subject No.",
        )
    )

    # Compound outstanding-balance / outstanding-payments rules for CI.
    errors.extend(_validate_ci_outstanding_fields(records, rule_loader))

    return errors


def _validate_age(record: Record, rule_loader: RuleLoader) -> FieldError | None:
    dob = record.fields.get("Date of Birth", "")
    ref = record.fields.get("Subject Reference Date", "")
    if not dob or not ref:
        return None
    try:
        dob_dt = datetime.strptime(dob, "%d%m%Y")
        ref_dt = datetime.strptime(ref, "%d%m%Y")
    except ValueError:
        return None
    age = ref_dt.year - dob_dt.year - ((ref_dt.month, ref_dt.day) < (dob_dt.month, dob_dt.day))
    code, desc, fix = _rule_or_default(
        rule_loader,
        "20-137",
        "Individual age should be between 18 and 100 years",
        "Verify Date of Birth and Subject Reference Date.",
    )
    return primitives.numeric_range_from_fields(
        record,
        age,
        18,
        100,
        "Date of Birth",
        code,
        desc,
        fix,
        "business_rule",
    )


def _validate_ci_outstanding_fields(
    records: list[Record],
    rule_loader: RuleLoader,
) -> list[FieldError]:
    """Enforce 10-270/10-272/10-274 compound rules for CI records.

    10-270: Contract Phase = AC AND Outstanding Payments Number is empty AND
            Contract Reference Date < Contract End Planned Date.
    10-272: Contract Phase = AC AND Outstanding Balance is empty AND
            Contract Reference Date < Contract End Planned Date.
    10-274: Contract Phase = AC AND (
                (Outstanding Payments Number = 0 or empty AND Outstanding Balance > 0) OR
                (Outstanding Payments Number > 0 AND Outstanding Balance = 0 or empty)
            ).
    """
    errors: list[FieldError] = []
    for rec in records:
        if rec.record_type != "CI":
            continue
        phase = rec.fields.get("Contract Phase", "")
        if phase != "AC":
            continue

        ref_date_str = rec.fields.get("Contract Reference Date", "")
        end_planned_str = rec.fields.get("Contract End Planned Date", "")
        ref_date = _parse_date(ref_date_str)
        end_planned = _parse_date(end_planned_str)
        before_end = ref_date is not None and end_planned is not None and ref_date < end_planned

        outstanding_num_str = rec.fields.get("Outstanding Payments Number", "")
        outstanding_bal_str = rec.fields.get("Outstanding Balance", "")
        outstanding_num = _parse_int(outstanding_num_str)
        outstanding_bal = _parse_int(outstanding_bal_str)

        # 10-270
        if before_end and outstanding_num_str == "":
            code, desc, fix = _rule_or_default(
                rule_loader,
                "10-270",
                "Outstanding Payments Number is required when Contract Phase is AC and Contract Reference Date is before Contract End Planned Date",
                "Provide Outstanding Payments Number for active contracts before the planned end date.",
            )
            errors.append(
                FieldError(
                    error_code=code,
                    category_prefix="10",
                    record_type=rec.record_type,
                    line_number=rec.line_number,
                    provider_subject_no=rec.provider_subject_no,
                    field_name="Outstanding Payments Number",
                    offending_value="",
                    description=desc,
                    fix_suggestion=fix,
                    severity="business_rule",
                )
            )

        # 10-272
        if before_end and outstanding_bal_str == "":
            code, desc, fix = _rule_or_default(
                rule_loader,
                "10-272",
                "Outstanding Balance is required when Contract Phase is AC and Contract Reference Date is before Contract End Planned Date",
                "Provide Outstanding Balance for active contracts before the planned end date.",
            )
            errors.append(
                FieldError(
                    error_code=code,
                    category_prefix="10",
                    record_type=rec.record_type,
                    line_number=rec.line_number,
                    provider_subject_no=rec.provider_subject_no,
                    field_name="Outstanding Balance",
                    offending_value="",
                    description=desc,
                    fix_suggestion=fix,
                    severity="business_rule",
                )
            )

        # 10-274
        num_zero_or_empty = outstanding_num is None or outstanding_num == 0
        bal_zero_or_empty = outstanding_bal is None or outstanding_bal == 0
        num_positive = outstanding_num is not None and outstanding_num > 0
        bal_positive = outstanding_bal is not None and outstanding_bal > 0
        if (num_zero_or_empty and bal_positive) or (num_positive and bal_zero_or_empty):
            code, desc, fix = _rule_or_default(
                rule_loader,
                "10-274",
                "Outstanding Payments Number and Outstanding Balance must both be provided for active contracts when either is non-zero",
                "Provide both Outstanding Payments Number and Outstanding Balance, or set both to 0.",
            )
            errors.append(
                FieldError(
                    error_code=code,
                    category_prefix="10",
                    record_type=rec.record_type,
                    line_number=rec.line_number,
                    provider_subject_no=rec.provider_subject_no,
                    field_name="Outstanding Payments Number / Outstanding Balance",
                    offending_value=f"{outstanding_num_str} / {outstanding_bal_str}",
                    description=desc,
                    fix_suggestion=fix,
                    severity="business_rule",
                )
            )

    return errors


def _parse_date(value: str) -> datetime | None:
    if not re.fullmatch(r"\d{8}", value):
        return None
    try:
        return datetime.strptime(value, "%d%m%Y")
    except ValueError:
        return None


def _parse_int(value: str) -> int | None:
    if value == "":
        return None
    try:
        return int(value)
    except ValueError:
        return None


def conditional_identification_length(
    records: list[Record],
    rule_loader: RuleLoader,
) -> list[FieldError]:
    """TIN=9-12, SSS=10, GSIS=11 for Identification 1/2/3."""
    errors: list[FieldError] = []
    id_map = {
        "10": (9, 12, "TIN", "20-050"),
        "11": (10, 10, "SSS", "20-051"),
        "12": (11, 11, "GSIS", "20-052"),
    }
    for rec in records:
        if rec.record_type != "ID":
            continue
        for i in (1, 2, 3):
            type_field = f"Identification {i}: Type"
            num_field = f"Identification {i}: Number"
            id_type = rec.fields.get(type_field, "")
            number = rec.fields.get(num_field, "")
            if id_type == "" or number == "" or id_type not in id_map:
                continue
            min_len, max_len, label, code = id_map[id_type]
            if number.isdigit() and min_len <= len(number) <= max_len:
                continue
            rule = rule_loader.get_rule(code)
            desc = (
                rule.get("description")
                if rule
                else f"{label} identification number must be {min_len}-{max_len} digits."
            )
            fix = (
                rule.get("rephrased_fix") or rule.get("solution")
                if rule
                else f"Enter a valid {label} number."
            )
            errors.append(
                FieldError(
                    error_code=code,
                    category_prefix="20",
                    record_type=rec.record_type,
                    line_number=rec.line_number,
                    provider_subject_no=rec.provider_subject_no,
                    field_name=num_field,
                    offending_value=number,
                    description=desc,
                    fix_suggestion=fix,
                    severity="business_rule",
                )
            )
    return errors
