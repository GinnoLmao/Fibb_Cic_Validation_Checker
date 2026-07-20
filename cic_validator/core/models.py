"""Core data models for the CIC Submission Validator."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


@dataclass
class Record:
    record_type: str
    line_number: int
    provider_subject_no: str | None
    fields: dict[str, str]
    raw_field_count: int | None = None

    def get(self, name: str, default: str = "") -> str:
        return self.fields.get(name, default)


@dataclass
class FieldError:
    error_code: str
    category_prefix: str
    record_type: str
    line_number: int
    provider_subject_no: str | None
    field_name: str | None
    offending_value: str | None
    description: str
    fix_suggestion: str
    severity: Literal["structural", "field", "business_rule"]


@dataclass
class ReportSummary:
    file_name: str
    total_records: int
    records_by_type: dict[str, int]
    total_errors: int
    errors_by_severity: dict[str, int]
    errors_by_code: dict[str, int]
    is_submission_ready: bool


def severity_from_prefix(prefix: str) -> Literal["structural", "field", "business_rule"]:
    if prefix in {"3", "30", "40"}:
        return "structural"
    if prefix in {"10"}:
        return "field"
    return "business_rule"
