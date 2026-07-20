"""Validation engine orchestrator."""
from __future__ import annotations

from pathlib import Path

from cic_validator.core.models import FieldError, Record, ReportSummary
from cic_validator.core.domain_loader import DomainLoader, get_domain_loader
from cic_validator.core.rule_loader import RuleLoader, get_rule_loader
from cic_validator.core.schema_loader import SchemaLoader, get_schema_loader
from cic_validator.core.file_detector import FileInfo, detect_file
from cic_validator.core.text_reader import read_text_file
from cic_validator.core.excel_reader import read_excel_file
from cic_validator.core.validators import structural, field_level, business_rules


def _records_from_file(path: Path, file_info: FileInfo, schema: SchemaLoader) -> list[Record]:
    if file_info.file_type == "txt":
        return read_text_file(path, schema)
    return read_excel_file(path, schema)


def _structurally_sound_line_numbers(
    records: list[Record], schema: SchemaLoader
) -> set[int]:
    """Return line numbers of records that have a valid type and expected field count."""
    sound = set()
    for rec in records:
        if rec.record_type not in schema.record_types():
            continue
        expected = schema.get_field_count(rec.record_type)
        if rec.raw_field_count is not None and rec.raw_field_count != expected:
            continue
        sound.add(rec.line_number)
    return sound


def validate_file(path: str | Path) -> tuple[list[FieldError], ReportSummary]:
    p = Path(path)
    file_info = detect_file(p)
    schema = get_schema_loader()
    domain_loader = get_domain_loader()
    rule_loader = get_rule_loader()

    records = _records_from_file(p, file_info, schema)

    errors: list[FieldError] = []
    errors.extend(structural.validate_structural(records, file_info, schema, rule_loader))

    # Only run content / business-rule checks on structurally sound records.
    sound_lines = _structurally_sound_line_numbers(records, schema)
    sound_records = [r for r in records if r.line_number in sound_lines]

    errors.extend(field_level.validate_field_level(sound_records, schema, domain_loader, rule_loader))
    errors.extend(business_rules.validate_business_rules(sound_records, schema, rule_loader))
    errors.extend(business_rules.conditional_identification_length(sound_records, rule_loader))

    summary = _build_summary(p.name, records, errors)
    return errors, summary


def _build_summary(file_name: str, records: list[Record], errors: list[FieldError]) -> ReportSummary:
    records_by_type: dict[str, int] = {}
    for r in records:
        records_by_type[r.record_type] = records_by_type.get(r.record_type, 0) + 1

    errors_by_severity: dict[str, int] = {}
    errors_by_code: dict[str, int] = {}
    for e in errors:
        errors_by_severity[e.severity] = errors_by_severity.get(e.severity, 0) + 1
        errors_by_code[e.error_code] = errors_by_code.get(e.error_code, 0) + 1

    is_ready = (
        errors_by_severity.get("structural", 0) == 0
        and errors_by_severity.get("field", 0) == 0
        and errors_by_severity.get("business_rule", 0) == 0
    )

    return ReportSummary(
        file_name=file_name,
        total_records=len(records),
        records_by_type=records_by_type,
        total_errors=len(errors),
        errors_by_severity=errors_by_severity,
        errors_by_code=errors_by_code,
        is_submission_ready=is_ready,
    )
