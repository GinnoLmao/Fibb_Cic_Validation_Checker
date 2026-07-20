"""Stage 1 — structural / pre-validation checks."""
from __future__ import annotations

from cic_validator.core.models import FieldError, Record, severity_from_prefix
from cic_validator.core.schema_loader import SchemaLoader
from cic_validator.core.rule_loader import RuleLoader
from cic_validator.core.file_detector import FileInfo


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


def validate_structural(
    records: list[Record],
    file_info: FileInfo,
    schema: SchemaLoader,
    rule_loader: RuleLoader,
) -> list[FieldError]:
    errors: list[FieldError] = []
    valid_types = set(schema.record_types())

    # 1. Filename / encoding checks for .txt
    if file_info.file_type == "txt":
        if not file_info.provider_code:
            desc, fix, sev = (
                "Filename format is not valid",
                "Filename must be <ProviderCode>_CSDF_YYYYMMDDhhmmss.txt",
                "structural",
            )
            errors.append(
                FieldError(
                    error_code="30-002",
                    category_prefix="30",
                    record_type="",
                    line_number=0,
                    provider_subject_no=None,
                    field_name=None,
                    offending_value=file_info.path.name,
                    description=desc,
                    fix_suggestion=fix,
                    severity=sev,
                )
            )
        if file_info.has_bom:
            code, desc, fix = _rule_or_default(
                rule_loader,
                "3-017",
                "Character set of file is not UTF-8",
                "Save the file as UTF-8 without BOM.",
            )
            errors.append(
                FieldError(
                    error_code=code,
                    category_prefix="30",
                    record_type="",
                    line_number=0,
                    provider_subject_no=None,
                    field_name=None,
                    offending_value="BOM detected",
                    description=desc,
                    fix_suggestion=fix,
                    severity=severity_from_prefix("30"),
                )
            )

    # 2. Header / footer presence and position
    if not records:
        code, desc, fix = _rule_or_default(
            rule_loader,
            "3-016",
            "File specified is empty",
            "The file contains no records.",
        )
        errors.append(
            FieldError(
                error_code=code,
                category_prefix="30",
                record_type="",
                line_number=0,
                provider_subject_no=None,
                field_name=None,
                offending_value=None,
                description=desc,
                fix_suggestion=fix,
                severity=severity_from_prefix("30"),
            )
        )
        return errors

    if records[0].record_type != "HD":
        code, desc, fix = _rule_or_default(
            rule_loader,
            "3-013",
            "Header is not present",
            "The file must start with an HD record.",
        )
        errors.append(
            FieldError(
                error_code=code,
                category_prefix="30",
                record_type=records[0].record_type,
                line_number=records[0].line_number,
                provider_subject_no=None,
                field_name=None,
                offending_value=records[0].record_type,
                description=desc,
                fix_suggestion=fix,
                severity=severity_from_prefix("30"),
            )
        )

    if records[-1].record_type != "FT":
        code, desc, fix = _rule_or_default(
            rule_loader,
            "30-014",
            "Footer is not present",
            "The file must end with an FT record.",
        )
        errors.append(
            FieldError(
                error_code=code,
                category_prefix="30",
                record_type=records[-1].record_type,
                line_number=records[-1].line_number,
                provider_subject_no=None,
                field_name=None,
                offending_value=records[-1].record_type,
                description=desc,
                fix_suggestion=fix,
                severity=severity_from_prefix("30"),
            )
        )

    # 3. Record type and field count
    for rec in records:
        if rec.record_type not in valid_types:
            code, desc, fix = _rule_or_default(
                rule_loader,
                "30-009",
                "Record type is not valid",
                "Record type must be one of HD, ID, BD, CI, CN, CC, CS, NE, SL, FT.",
            )
            errors.append(
                FieldError(
                    error_code=code,
                    category_prefix="30",
                    record_type=rec.record_type,
                    line_number=rec.line_number,
                    provider_subject_no=rec.provider_subject_no,
                    field_name=None,
                    offending_value=rec.record_type,
                    description=desc,
                    fix_suggestion=fix,
                    severity=severity_from_prefix("30"),
                )
            )
            continue

        expected = schema.get_field_count(rec.record_type)
        if rec.raw_field_count is not None and rec.raw_field_count != expected:
            code, desc, fix = _rule_or_default(
                rule_loader,
                "30-010",
                "Number of fields is not valid for the specified record type",
                f"Record type {rec.record_type} expects {expected} fields; found {rec.raw_field_count}.",
            )
            errors.append(
                FieldError(
                    error_code=code,
                    category_prefix="30",
                    record_type=rec.record_type,
                    line_number=rec.line_number,
                    provider_subject_no=rec.provider_subject_no,
                    field_name=None,
                    offending_value=str(rec.raw_field_count),
                    description=desc,
                    fix_suggestion=fix,
                    severity=severity_from_prefix("30"),
                )
            )

    # 4. Provider code consistency
    if file_info.file_type == "txt" and file_info.provider_code:
        hd_code = records[0].fields.get("Provider Code") if records[0].record_type == "HD" else None
        if hd_code and hd_code != file_info.provider_code:
            code, desc, fix = _rule_or_default(
                rule_loader,
                "30-006",
                "Provider code inside the file is not valid or different from the provider specified in filename",
                "Ensure the Provider Code in the HD record matches the filename.",
            )
            errors.append(
                FieldError(
                    error_code=code,
                    category_prefix="30",
                    record_type="HD",
                    line_number=records[0].line_number,
                    provider_subject_no=None,
                    field_name="Provider Code",
                    offending_value=hd_code,
                    description=desc,
                    fix_suggestion=fix,
                    severity=severity_from_prefix("30"),
                )
            )

        for rec in records:
            if rec.record_type in {"HD", "FT"}:
                continue
            rec_code = rec.fields.get("Provider Code", "")
            if rec_code and rec_code != file_info.provider_code:
                code, desc, fix = _rule_or_default(
                    rule_loader,
                    "40-006",
                    "Provider code in filename inconsistent with submitting provider",
                    "Ensure Provider Code matches the filename in every detail record.",
                )
                errors.append(
                    FieldError(
                        error_code=code,
                        category_prefix="40",
                        record_type=rec.record_type,
                        line_number=rec.line_number,
                        provider_subject_no=rec.provider_subject_no,
                        field_name="Provider Code",
                        offending_value=rec_code,
                        description=desc,
                        fix_suggestion=fix,
                        severity=severity_from_prefix("40"),
                    )
                )

    # 5. Footer record count
    ft_records = [r for r in records if r.record_type == "FT"]
    if ft_records:
        ft = ft_records[-1]
        footer_count_str = ft.fields.get("No. of records", "")
        detail_count = len([r for r in records if r.record_type not in {"HD", "FT"}])
        if footer_count_str != str(detail_count):
            code, desc, fix = _rule_or_default(
                rule_loader,
                "30-011",
                "Number of records after the header is not valid",
                f"Footer says {footer_count_str} detail records; file contains {detail_count}.",
            )
            errors.append(
                FieldError(
                    error_code=code,
                    category_prefix="30",
                    record_type="FT",
                    line_number=ft.line_number,
                    provider_subject_no=None,
                    field_name="No. of records",
                    offending_value=footer_count_str,
                    description=desc,
                    fix_suggestion=fix,
                    severity=severity_from_prefix("30"),
                )
            )

    return errors
