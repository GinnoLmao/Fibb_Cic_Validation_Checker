"""Load the annotated record-type field schema."""
from __future__ import annotations

import json
from pathlib import Path

from cic_validator.core._paths import resource_path


_SCHEMA_PATH = resource_path("record_type_field_schema.json")


def load_schema() -> dict:
    with _SCHEMA_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


class SchemaLoader:
    def __init__(self, schema: dict | None = None):
        self.schema = schema or load_schema()

    def get_record_type(self, code: str) -> dict:
        return self.schema.get(code, {})

    def get_fields(self, code: str) -> list[dict]:
        return self.get_record_type(code).get("fields", [])

    def get_field(self, code: str, name: str) -> dict | None:
        for f in self.get_fields(code):
            if f["name"] == name:
                return f
        return None

    def get_field_by_position(self, code: str, position: int) -> dict | None:
        for f in self.get_fields(code):
            if f["position"] == position:
                return f
        return None

    def get_field_count(self, code: str) -> int:
        return self.get_record_type(code).get("field_count", 0)

    def get_group_rules(self, code: str) -> list[dict]:
        return self.get_record_type(code).get("group_rules", [])

    def record_types(self) -> list[str]:
        return list(self.schema.keys())


_schema_loader: SchemaLoader | None = None


def get_schema_loader() -> SchemaLoader:
    global _schema_loader
    if _schema_loader is None:
        _schema_loader = SchemaLoader()
    return _schema_loader
