"""Resolve package resource paths for both normal and PyInstaller-frozen runs."""
from __future__ import annotations

import sys
from pathlib import Path


def is_frozen() -> bool:
    return getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS")


def schema_dir() -> Path:
    """Return the directory containing the JSON schema files."""
    if is_frozen():
        # PyInstaller onefile extracts the package to <MEIPASS>\cic_validator
        return Path(sys._MEIPASS) / "cic_validator" / "schema"  # type: ignore[attr-defined]
    return Path(__file__).resolve().parents[1] / "schema"


def resource_path(relative_path: str) -> Path:
    """Return an absolute path to a package resource."""
    return schema_dir() / relative_path
