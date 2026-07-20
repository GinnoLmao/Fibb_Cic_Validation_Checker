"""Filterable/sortable results table for validation errors."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

import ttkbootstrap as ttkb
from ttkbootstrap.constants import *

from cic_validator.core.models import FieldError


COLUMNS = ("status", "line", "type", "subject", "field", "code", "issue")
HEADERS = {
    "status": "",
    "line": "Line",
    "type": "Type",
    "subject": "Subject No.",
    "field": "Field",
    "code": "Code",
    "issue": "Issue",
}


class ResultsView(ttkb.Frame):
    def __init__(self, parent, on_select, **kwargs):
        super().__init__(parent, **kwargs)
        self.on_select = on_select
        self._errors: list[FieldError] = []
        self._sort_col: str | None = None
        self._sort_reverse: bool = False

        self._build()

    def _build(self) -> None:
        # Toolbar
        self.toolbar = ttkb.Frame(self)
        self.toolbar.pack(fill=X, pady=(0, 8))

        ttkb.Label(self.toolbar, text="Filter:").pack(side=LEFT, padx=(0, 6))
        self.type_var = ttkb.StringVar(value="All Types")
        self.type_combo = ttkb.Combobox(
            self.toolbar,
            textvariable=self.type_var,
            values=["All Types"],
            state="readonly",
            width=14,
        )
        self.type_combo.pack(side=LEFT, padx=(0, 6))
        self.type_combo.bind("<<ComboboxSelected>>", lambda _e: self._apply_filter())

        self.sev_var = ttkb.StringVar(value="All Severities")
        self.sev_combo = ttkb.Combobox(
            self.toolbar,
            textvariable=self.sev_var,
            values=["All Severities", "Structural", "Field", "Business rule"],
            state="readonly",
            width=14,
        )
        self.sev_combo.pack(side=LEFT, padx=(0, 6))
        self.sev_combo.bind("<<ComboboxSelected>>", lambda _e: self._apply_filter())

        self.search_var = ttkb.StringVar()
        self.search_entry = ttkb.Entry(self.toolbar, textvariable=self.search_var, width=24)
        self.search_entry.pack(side=LEFT, padx=(0, 6))
        self.search_var.trace_add("write", lambda *_args: self._apply_filter())

        # Treeview
        self.tree = ttkb.Treeview(
            self,
            columns=COLUMNS,
            show="headings",
            selectmode="browse",
            bootstyle="table",
        )
        for col in COLUMNS:
            self.tree.heading(col, text=HEADERS[col], command=lambda c=col: self._sort_by(c))
            width = 40 if col == "status" else 70 if col == "line" else 90 if col in ("type", "code") else 140
            self.tree.column(col, width=width, anchor=W if col != "status" else CENTER)

        self.tree.pack(side=LEFT, fill=BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

        # Scrollbar
        self.scrollbar = ttkb.Scrollbar(self, orient=VERTICAL, command=self.tree.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Empty state placeholder
        self.empty_label = ttkb.Label(
            self,
            text="Choose an Excel masterfile or a CSDF .txt file to begin",
            bootstyle="secondary",
            font=("Segoe UI", 11),
        )

    def set_errors(self, errors: list[FieldError]) -> None:
        self._errors = errors
        self._update_type_filter()
        self._apply_filter()
        if not errors:
            self.tree.pack_forget()
            self.scrollbar.pack_forget()
            self.empty_label.pack(expand=True)
        else:
            self.empty_label.pack_forget()
            self.tree.pack(side=LEFT, fill=BOTH, expand=True)
            self.scrollbar.pack(side=RIGHT, fill=Y)

    def _update_type_filter(self) -> None:
        types = sorted({e.record_type for e in self._errors if e.record_type})
        values = ["All Types"] + types
        self.type_combo.configure(values=values)
        if self.type_var.get() not in values:
            self.type_var.set("All Types")

    def _apply_filter(self) -> None:
        selected_type = self.type_var.get()
        selected_sev = self.sev_var.get()
        search = self.search_var.get().lower()

        severities = {
            "Structural": "structural",
            "Field": "field",
            "Business rule": "business_rule",
        }

        filtered = []
        for e in self._errors:
            if selected_type != "All Types" and e.record_type != selected_type:
                continue
            if selected_sev != "All Severities" and e.severity != severities.get(selected_sev):
                continue
            if search and search not in (
                (e.description or "") + (e.field_name or "") + (e.record_type or "") + (e.error_code or "")
            ).lower():
                continue
            filtered.append(e)

        self._populate(filtered)

    def _populate(self, errors: list[FieldError]) -> None:
        self.tree.delete(*self.tree.get_children())
        for e in errors:
            if e.severity == "structural":
                indicator = "●"
                tag = "error"
            elif e.severity == "field":
                indicator = "●"
                tag = "warning"
            else:
                indicator = "●"
                tag = "info"
            self.tree.insert(
                "",
                END,
                values=(
                    indicator,
                    e.line_number,
                    e.record_type,
                    e.provider_subject_no or "",
                    e.field_name or "",
                    e.error_code,
                    e.description[:60] + "..." if len(e.description) > 60 else e.description,
                ),
                tags=(tag,),
            )
        self.tree.tag_configure("error", foreground="#dc3545")
        self.tree.tag_configure("warning", foreground="#f0ad4e")
        self.tree.tag_configure("info", foreground="#1e3a5f")

    def _sort_by(self, col: str) -> None:
        if self._sort_col == col:
            self._sort_reverse = not self._sort_reverse
        else:
            self._sort_col = col
            self._sort_reverse = False
        key_map = {
            "line": lambda e: e.line_number,
            "type": lambda e: e.record_type,
            "subject": lambda e: e.provider_subject_no or "",
            "field": lambda e: e.field_name or "",
            "code": lambda e: e.error_code,
            "issue": lambda e: e.description,
            "status": lambda e: e.severity,
        }
        self._errors.sort(key=key_map[col], reverse=self._sort_reverse)
        self._apply_filter()

    def _on_select(self, _event=None) -> None:
        selection = self.tree.selection()
        if not selection:
            return
        item = self.tree.item(selection[0])
        values = item.get("values", [])
        if len(values) < 7:
            return
        line = values[1]
        selected = [e for e in self._errors if e.line_number == line]
        if selected:
            self.on_select(selected[0])

    def reset(self) -> None:
        self._errors = []
        self.tree.delete(*self.tree.get_children())
        self.tree.pack_forget()
        self.scrollbar.pack_forget()
        self.empty_label.pack(expand=True)
        self.type_var.set("All Types")
        self.sev_var.set("All Severities")
        self.search_var.set("")
