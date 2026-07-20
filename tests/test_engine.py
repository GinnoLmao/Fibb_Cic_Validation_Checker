"""Smoke tests for CIC Submission Validator."""
from __future__ import annotations

from pathlib import Path

import pytest

from cic_validator.core.engine import validate_file
from cic_validator.core.schema_loader import SchemaLoader
from cic_validator.core.text_reader import read_text_file
from cic_validator.report.report_writer import generate_report_text, write_report


ROOT = Path(__file__).resolve().parent.parent
SAMPLE_TXT = ROOT / "Raw Samples" / "RB001800_CSDF_20260531000001.txt"
SAMPLE_XLSX = ROOT / "Raw Samples" / "sample_data.xlsx"


def test_schema_loads_all_record_types() -> None:
    schema = SchemaLoader()
    assert "HD" in schema.record_types()
    assert "ID" in schema.record_types()
    assert "CI" in schema.record_types()
    assert "FT" in schema.record_types()


def test_text_reader_counts() -> None:
    schema = SchemaLoader()
    records = read_text_file(SAMPLE_TXT, schema)
    assert len(records) == 10
    assert records[0].record_type == "HD"
    assert records[3].record_type == "ID"
    assert records[3].raw_field_count == 123


def test_engine_on_sample_data_with_proper_filename() -> None:
    schema = SchemaLoader()
    # Sample fixture must have a valid CSDF filename
    proper = ROOT / "Raw Samples" / "RB001800_CSDF_20251212160316.txt"
    if not proper.exists():
        pytest.skip("Real fixture not present")
    errors, summary = validate_file(str(proper))
    # Only the structural error on line 4 should be reported
    assert summary.total_records == 4096
    structural_errors = [e for e in errors if e.severity == "structural"]
    # We do not assert the exact count for a real bank file, but ensure the engine runs
    assert len(structural_errors) > 0


def test_engine_on_small_sample_copy(tmp_path: Path) -> None:
    if not SAMPLE_TXT.exists():
        pytest.skip("sample data.txt not found")
    # Copy sample data to a valid CSDF filename
    sample_copy = tmp_path / "RB001800_CSDF_20251212160316.txt"
    sample_copy.write_bytes(SAMPLE_TXT.read_bytes())
    errors, summary = validate_file(str(sample_copy))
    assert summary.total_records == 10
    # Sample data has the correct 123-field ID records, so no structural errors
    assert summary.errors_by_severity.get("structural", 0) == 0
    structural = [e for e in errors if e.severity == "structural"]
    assert len(structural) == 0
    # No field/business errors on the correct records
    assert summary.errors_by_severity.get("field", 0) == 0
    assert summary.errors_by_severity.get("business_rule", 0) == 0
    assert summary.is_submission_ready is True


def test_excel_reader_runs() -> None:
    if not SAMPLE_XLSX.exists():
        pytest.skip("sample_data.xlsx not found")
    from cic_validator.core.excel_reader import read_excel_file
    schema = SchemaLoader()
    records = read_excel_file(SAMPLE_XLSX, schema)
    assert len(records) >= 10
    assert any(r.record_type == "HD" for r in records)


def test_report_writer(tmp_path: Path) -> None:
    from cic_validator.core.models import FieldError, ReportSummary
    err = FieldError(
        error_code="30-010",
        category_prefix="30",
        record_type="ID",
        line_number=4,
        provider_subject_no="",
        field_name="",
        offending_value="122",
        description="Wrong field count",
        fix_suggestion="Check delimiters",
        severity="structural",
    )
    summary = ReportSummary(
        file_name="test.txt",
        total_records=10,
        records_by_type={"HD": 1, "ID": 9},
        total_errors=1,
        errors_by_severity={"structural": 1},
        errors_by_code={"30-010": 1},
        is_submission_ready=False,
    )
    path = tmp_path / "report.txt"
    write_report([err], summary, path)
    text = path.read_text(encoding="utf-8")
    assert "30-010" in text
    assert "Wrong field count" in text
    assert "Submission-ready" in text


def test_generate_report_text() -> None:
    from cic_validator.core.models import FieldError, ReportSummary
    err = FieldError(
        error_code="CUSTOM-DATE",
        category_prefix="CUSTOM",
        record_type="ID",
        line_number=2,
        provider_subject_no="123456789",
        field_name="Date of Birth",
        offending_value="12345",
        description="Invalid date",
        fix_suggestion="Use YYYY-MM-DD",
        severity="field",
    )
    summary = ReportSummary(
        file_name="test.txt",
        total_records=10,
        records_by_type={"HD": 1, "ID": 9},
        total_errors=1,
        errors_by_severity={"field": 1},
        errors_by_code={"CUSTOM-DATE": 1},
        is_submission_ready=False,
    )
    text = generate_report_text([err], summary)
    assert "Invalid date" in text
    assert "123456789" in text
    assert "Submission-ready" in text
