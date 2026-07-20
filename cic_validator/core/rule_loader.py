"""Load CIC error rules and provide lookup helpers."""
from __future__ import annotations

import json
import re

from cic_validator.core._paths import resource_path


_RULES_PATH = resource_path("error_rules_consolidated.json")
_BINDINGS_PATH = resource_path("rule_bindings.json")
_UNMAPPED_PATH = resource_path("unmapped_rules.json")


def _normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", text.lower())


class RuleLoader:
    def __init__(self, rules: list | None = None, bindings: list | None = None):
        self.rules = rules or self._load_rules()
        self.bindings = bindings or self._load_bindings()
        self._rules_by_code: dict[str, dict] = {r["error_code"]: r for r in self.rules}
        self._bindings_by_code: dict[str, dict] = {b["error_code"]: b for b in self.bindings}

    @staticmethod
    def _load_rules() -> list[dict]:
        with _RULES_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def _load_bindings() -> list[dict]:
        if not _BINDINGS_PATH.exists():
            return []
        with _BINDINGS_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)

    def get_rule(self, code: str) -> dict | None:
        return self._rules_by_code.get(code)

    def get_binding(self, code: str) -> dict | None:
        return self._bindings_by_code.get(code)

    def find_code(self, pattern: str, field_name: str | None = None) -> dict | None:
        """Return the first rule whose description loosely matches *pattern* and *field_name*."""
        norm_pattern = _normalize(pattern)
        norm_field = _normalize(field_name) if field_name else None
        for rule in self.rules:
            desc = rule.get("description", "")
            norm_desc = _normalize(desc)
            if norm_pattern in norm_desc:
                if norm_field is None or norm_field in norm_desc:
                    return rule
        return None

    def unmapped_rules(self) -> list[dict]:
        if not _UNMAPPED_PATH.exists():
            return []
        with _UNMAPPED_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)


_rule_loader: RuleLoader | None = None


def get_rule_loader() -> RuleLoader:
    global _rule_loader
    if _rule_loader is None:
        _rule_loader = RuleLoader()
    return _rule_loader
