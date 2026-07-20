"""Generate the clean, human-readable validation report (.txt)."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

from cic_validator.core.models import FieldError, ReportSummary


def _section_header(title: str) -> list[str]:
    return [
        "",
        title,
        "-" * 62,
    ]


def _format_error_block(idx: int, error: FieldError) -> list[str]:
    lines: list[str] = []
    subject = error.provider_subject_no or "-"
    lines.append(f"[{idx}] Line {error.line_number} - Record {error.record_type} - Provider Subject No. {subject}")
    if error.field_name:
        lines.append(f"     Field      : {error.field_name}")
    if error.offending_value:
        lines.append(f"     Value found: {error.offending_value}")
    lines.append(f"     Error Code : {error.error_code}")
    lines.append(f"     Why        : {error.description}")
    fix = (error.fix_suggestion or "").replace("\n", "\n                  ")
    lines.append(f"     Fix        : {fix}")
    lines.append("")
    return lines


def generate_report_text(errors: list[FieldError], summary: ReportSummary) -> str:
    lines: list[str] = []
    lines.append("=" * 62)
    lines.append(" CIC SUBMISSION VALIDATION REPORT")
    lines.append("=" * 62)
    lines.append(f" Source file : {summary.file_name}")
    lines.append(f" Validated   : {datetime.now():%Y-%m-%d %H:%M}")
    # Provider code from filename or HD if available
    provider = _extract_provider_code(summary.file_name) or "-"
    lines.append(f" Provider    : {provider}")
    lines.append("")

    # Summary
    lines.extend(_section_header(" SUMMARY"))
    clean_records = summary.total_records - len({e.line_number for e in errors})
    lines.append(f" Total records            : {summary.total_records:,}")
    lines.append(f" Records with no errors   : {clean_records:,}")
    lines.append(f" Records with errors      : {len({e.line_number for e in errors}):,}")
    lines.append(f" Total errors found       : {summary.total_errors:,}")
    lines.append(f"   Structural (PRE)       : {summary.errors_by_severity.get('structural', 0):,}")
    lines.append(f"   Field-level            : {summary.errors_by_severity.get('field', 0):,}")
    lines.append(f"   Business rule          : {summary.errors_by_severity.get('business_rule', 0):,}")
    status = "YES - ready for upload" if summary.is_submission_ready else "NO - resolve errors below before upload"
    lines.append(f" Submission-ready         : {status}")
    lines.append("=" * 62)

    sections = [
        ("structural", " SECTION 1: STRUCTURAL ERRORS (fix these first - they can invalidate the entire file)"),
        ("field", " SECTION 2: FIELD-LEVEL ERRORS"),
        ("business_rule", " SECTION 3: BUSINESS RULE / CROSS-FIELD ERRORS"),
    ]

    for severity, title in sections:
        section_errors = [e for e in errors if e.severity == severity]
        if not section_errors:
            continue
        lines.extend(_section_header(title))
        # Sort by provider subject no (None last), then line number
        section_errors.sort(key=lambda e: (e.provider_subject_no or "~~~", e.line_number))
        for i, err in enumerate(section_errors, start=1):
            lines.extend(_format_error_block(i, err))

    lines.append("")
    lines.append("=" * 62)
    lines.append(" END OF REPORT")
    lines.append("=" * 62)
    return "\n".join(lines)


def _extract_provider_code(filename: str) -> str | None:
    from cic_validator.core.file_detector import _extract_provider_code as extract
    return extract(filename)


def write_report(
    errors: list[FieldError],
    summary: ReportSummary,
    output_path: str | Path,
) -> Path:
    text = generate_report_text(errors, summary)
    p = Path(output_path)
    p.write_text(text, encoding="utf-8")
    return p
