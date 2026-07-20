"""Load domain/valid-value tables and provide lookup helpers."""
from __future__ import annotations

import json

from cic_validator.core._paths import resource_path


_DOMAINS_PATH = resource_path("domains.json")


def _normalize(value) -> str:
    if value is None:
        return ""
    return str(value).strip()


class DomainLoader:
    def __init__(self, raw: dict | None = None):
        self.raw = raw or self._load()
        self._cache: dict[str, set[str]] = {}

    @staticmethod
    def _load() -> dict:
        with _DOMAINS_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)

    def values(self, domain_key: str) -> set[str]:
        if domain_key not in self._cache:
            entries = self.raw.get(domain_key, [])
            self._cache[domain_key] = {_normalize(e.get("value")) for e in entries}
        return self._cache[domain_key]

    def is_valid(self, domain_key: str, value: str) -> bool:
        if value is None or value == "":
            return True  # empty values are handled by mandatory checks
        return _normalize(value) in self.values(domain_key)

    def keys(self) -> list[str]:
        return list(self.raw.keys())


_domain_loader: DomainLoader | None = None


def get_domain_loader() -> DomainLoader:
    global _domain_loader
    if _domain_loader is None:
        _domain_loader = DomainLoader()
    return _domain_loader
