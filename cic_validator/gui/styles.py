"""Theme and styling configuration for the CIC Submission Validator GUI."""
from __future__ import annotations

import ttkbootstrap as ttk


def apply_theme() -> ttk.Style:
    return ttk.Style("flatly")


# Color palette (semantic only)
COLOR_ACCENT = "#1e3a5f"
COLOR_SUCCESS = "#28a745"
COLOR_WARNING = "#f0ad4e"
COLOR_ERROR = "#dc3545"
COLOR_NEUTRAL = "#6c757d"

FONT_FAMILY = "Segoe UI"

TITLE_FONT = (FONT_FAMILY, 18, "bold")
HEADER_FONT = (FONT_FAMILY, 12, "bold")
BODY_FONT = (FONT_FAMILY, 10)
SMALL_FONT = (FONT_FAMILY, 9)
STAT_NUMBER_FONT = (FONT_FAMILY, 24, "bold")
STAT_LABEL_FONT = (FONT_FAMILY, 9)
