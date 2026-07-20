"""Detect input file type and perform light file-level validation."""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


FILENAME_RE = re.compile(r"^[A-Za-z0-9]{8}_CSDF_\d{14}\.txt$")


@dataclass
class FileInfo:
    path: Path
    file_type: str  # 'txt' or 'xlsx'
    provider_code: str | None
    has_bom: bool


def detect_file(path: str | Path) -> FileInfo:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {p}")

    suffix = p.suffix.lower()
    if suffix == ".txt":
        file_type = "txt"
    elif suffix in {".xlsx", ".xlsm"}:
        file_type = "xlsx"
    else:
        raise ValueError(f"Unsupported file type: {suffix}")

    provider_code = _extract_provider_code(p.name) if file_type == "txt" else None
    has_bom = _has_bom(p) if file_type == "txt" else False
    return FileInfo(path=p, file_type=file_type, provider_code=provider_code, has_bom=has_bom)


def _extract_provider_code(filename: str) -> str | None:
    m = re.match(r"^([A-Za-z0-9]{8})_CSDF_\d{14}\.txt$", filename)
    return m.group(1) if m else None


def _has_bom(path: Path) -> bool:
    with path.open("rb") as f:
        return f.read(3) == b"\xef\xbb\xbf"


def is_valid_filename(filename: str) -> bool:
    return bool(FILENAME_RE.match(filename))
