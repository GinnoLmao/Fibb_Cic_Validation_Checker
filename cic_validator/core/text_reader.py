"""Read pipe-delimited CSDF .txt files into Record objects."""
from __future__ import annotations

from pathlib import Path

from cic_validator.core.models import Record
from cic_validator.core.schema_loader import SchemaLoader


def read_text_file(
    path: str | Path,
    schema: SchemaLoader,
) -> list[Record]:
    p = Path(path)
    with p.open("r", encoding="utf-8-sig") as f:
        raw_lines = f.readlines()

    records: list[Record] = []
    for idx, line in enumerate(raw_lines, start=1):
        line = line.rstrip("\n\r")
        if line == "":
            continue
        parts = line.split("|")
        rt = parts[0] if parts else ""
        expected = schema.get_field_count(rt) if rt in schema.record_types() else 0
        # Map known fields; if field count is wrong we still map what we can.
        field_names = [
            f["name"]
            for f in schema.get_fields(rt)
        ]
        fields = {}
        for i, name in enumerate(field_names):
            fields[name] = parts[i] if i < len(parts) else ""

        psn = fields.get("Provider Subject No") or None
        records.append(
            Record(record_type=rt, line_number=idx, provider_subject_no=psn, fields=fields, raw_field_count=len(parts))
        )

    return records
