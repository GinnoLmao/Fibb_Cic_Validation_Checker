"""Stage 2 — field-level validation (mandatory, format, domain, length, numeric)."""
from __future__ import annotations

from cic_validator.core.models import FieldError, Record
from cic_validator.core.domain_loader import DomainLoader
from cic_validator.core.rule_loader import RuleLoader
from cic_validator.core.schema_loader import SchemaLoader
from cic_validator.core import rule_primitives as primitives


def validate_field_level(
    records: list[Record],
    schema: SchemaLoader,
    domain_loader: DomainLoader,
    rule_loader: RuleLoader,
) -> list[FieldError]:
    errors: list[FieldError] = []

    for rec in records:
        if rec.record_type not in schema.record_types():
            continue

        for field in schema.get_fields(rec.record_type):
            name = field["name"]
            data_type = field.get("data_type")
            domain_key = field.get("domain")

            # 1. Mandatory check (unconditional or conditional)
            if field.get("mandatory"):
                if field.get("mandatory_type") == "conditional":
                    cond = field.get("mandatory_condition")
                    err = primitives.required_conditional(
                        rec,
                        field,
                        cond["field"],
                        cond["values"],
                        rule_loader,
                    )
                else:
                    err = primitives.required(rec, field, rule_loader)
                if err:
                    errors.append(err)
                    # If a field is empty and mandatory, skip further format/domain checks.
                    if rec.fields.get(name, "") == "":
                        continue

            # 2. Domain / date / numeric / length checks
            if domain_key:
                err = primitives.domain_lookup(rec, field, domain_loader, rule_loader)
                if err:
                    errors.append(err)
            elif data_type == "date":
                err = primitives.date_format(rec, field, rule_loader)
                if err:
                    errors.append(err)
            elif data_type == "yesno":
                err = primitives.domain_lookup(
                    rec,
                    {
                        "name": name,
                        "domain": "ID - Individual :: YesNoDomain",
                        "data_type": "domain",
                        "max_length": field.get("max_length"),
                    },
                    domain_loader,
                    rule_loader,
                )
                if err:
                    errors.append(err)

            # Numeric+length check for numeric fields
            if data_type == "numeric":
                err = primitives.numeric_and_length(rec, field, rule_loader)
                if err:
                    errors.append(err)
            else:
                # Generic max length for non-numeric fields
                err = primitives.max_length(rec, field, rule_loader)
                if err:
                    errors.append(err)

    return errors
