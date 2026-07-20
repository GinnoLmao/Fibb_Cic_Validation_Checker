"""Main application window for the CIC Submission Validator."""
from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox
from typing import List

import ttkbootstrap as ttkb
from ttkbootstrap.constants import *

from cic_validator.core.engine import validate_file
from cic_validator.core.models import FieldError, ReportSummary
from cic_validator.gui.results_view import ResultsView
from cic_validator.gui.styles import (
    BODY_FONT,
    COLOR_ACCENT,
    COLOR_ERROR,
    COLOR_NEUTRAL,
    COLOR_SUCCESS,
    COLOR_WARNING,
    HEADER_FONT,
    SMALL_FONT,
    STAT_LABEL_FONT,
    STAT_NUMBER_FONT,
    TITLE_FONT,
    apply_theme,
)
from cic_validator.report.report_writer import write_report


class AppWindow:
    def __init__(self, root: ttkb.Window) -> None:
        self.root = root
        self.root.title("CIC Submission Validator")
        self.root.geometry("1100x750")
        self.root.minsize(900, 600)
        apply_theme()

        self._current_path: Path | None = None
        self._errors: List[FieldError] = []
        self._summary: ReportSummary | None = None

        self._build_ui()

    def _build_ui(self) -> None:
        # Main container
        self.main_frame = ttkb.Frame(self.root, padding=20)
        self.main_frame.pack(fill=BOTH, expand=True)

        # Header
        header = ttkb.Frame(self.main_frame)
        header.pack(fill=X, pady=(0, 16))
        ttkb.Label(
            header,
            text="CIC Submission Validator",
            font=TITLE_FONT,
            foreground=COLOR_ACCENT,
        ).pack(side=LEFT)
        self.status_label = ttkb.Label(
            header,
            text="Ready",
            font=SMALL_FONT,
            bootstyle="secondary",
        )
        self.status_label.pack(side=RIGHT)

        # File selection card
        file_card = ttkb.Frame(self.main_frame, bootstyle="default")
        file_card.pack(fill=X, pady=(0, 16))
        ttkb.Label(file_card, text="File to validate", font=HEADER_FONT).pack(anchor=W, padx=12, pady=(12, 6))

        file_row = ttkb.Frame(file_card)
        file_row.pack(fill=X, padx=12, pady=(0, 12))
        self.path_var = ttkb.StringVar()
        self.path_entry = ttkb.Entry(file_row, textvariable=self.path_var, state="readonly", font=BODY_FONT)
        self.path_entry.pack(side=LEFT, fill=X, expand=True, padx=(0, 10))
        self.browse_btn = ttkb.Button(
            file_row,
            text="Browse",
            command=self._browse_file,
            bootstyle="outline",
            width=10,
        )
        self.browse_btn.pack(side=LEFT, padx=(0, 6))
        self.validate_btn = ttkb.Button(
            file_row,
            text="Validate",
            command=self._start_validation,
            bootstyle="primary",
            width=12,
        )
        self.validate_btn.pack(side=LEFT)

        # Progress bar
        self.progress = ttkb.Progressbar(self.main_frame, mode="indeterminate", bootstyle="primary")
        # hidden until validation starts

        # Summary cards
        self.summary_frame = ttkb.Frame(self.main_frame)
        self.summary_frame.pack(fill=X, pady=(0, 16))
        self._summary_cards = []
        labels = [
            ("Total Records", "total_records", COLOR_NEUTRAL),
            ("Clean Records", "clean_records", COLOR_SUCCESS),
            ("Errors Found", "total_errors", COLOR_ERROR),
            ("Submission Ready", "ready", COLOR_ACCENT),
        ]
        for title, key, color in labels:
            card = ttkb.Frame(self.summary_frame, bootstyle="default")
            card.pack(side=LEFT, fill=BOTH, expand=True, padx=4)
            val = ttkb.Label(card, text="—", font=STAT_NUMBER_FONT, foreground=color)
            val.pack(pady=(10, 0))
            lbl = ttkb.Label(card, text=title, font=STAT_LABEL_FONT, bootstyle="secondary")
            lbl.pack(pady=(0, 10))
            self._summary_cards.append((key, val, title))

        # Severity breakdown
        self.severity_frame = ttkb.Frame(self.main_frame)
        self.severity_frame.pack(fill=X, pady=(0, 16))
        self.severity_labels = {}
        sev_items = [
            ("Structural", "structural", COLOR_ERROR),
            ("Field-level", "field", COLOR_WARNING),
            ("Business rule", "business_rule", COLOR_ACCENT),
        ]
        for text, key, color in sev_items:
            lbl = ttkb.Label(
                self.severity_frame,
                text=f"{text}: 0",
                font=BODY_FONT,
                foreground=color,
            )
            lbl.pack(side=LEFT, padx=12)
            self.severity_labels[key] = lbl

        # Results table
        self.results_view = ResultsView(self.main_frame, on_select=self._show_error_detail)
        self.results_view.pack(fill=BOTH, expand=True, pady=(0, 16))

        # Detail panel
        detail_card = ttkb.Frame(self.main_frame, bootstyle="default")
        detail_card.pack(fill=X, pady=(0, 16))
        ttkb.Label(detail_card, text="Selected Error Detail", font=HEADER_FONT).pack(anchor=W, padx=12, pady=(12, 6))
        self.detail_text = tk.Text(
            detail_card,
            wrap=WORD,
            height=8,
            font=BODY_FONT,
            relief=FLAT,
            bg=self.root.style.colors.bg,
            fg=self.root.style.colors.fg,
            padx=8,
            pady=8,
        )
        self.detail_text.pack(fill=X, padx=12, pady=(0, 12))
        self.detail_text.configure(state="disabled")

        # Actions
        actions = ttkb.Frame(self.main_frame)
        actions.pack(fill=X)
        self.save_btn = ttkb.Button(
            actions,
            text="Save Report",
            command=self._save_report,
            bootstyle="success",
            state="disabled",
            width=14,
        )
        self.save_btn.pack(side=LEFT, padx=(0, 10))
        ttkb.Button(
            actions,
            text="Exit",
            command=self.root.quit,
            bootstyle="outline",
            width=10,
        ).pack(side=RIGHT)

    def _browse_file(self) -> None:
        filetypes = [
            ("CIC files", "*.txt *.xlsx"),
            ("Text files", "*.txt"),
            ("Excel files", "*.xlsx"),
            ("All files", "*.*"),
        ]
        path = filedialog.askopenfilename(
            title="Select CIC Submission File",
            filetypes=filetypes,
        )
        if not path:
            return
        self._current_path = Path(path)
        self.path_var.set(str(self._current_path))
        self._reset_results()
        self._start_validation()

    def _reset_results(self) -> None:
        self._errors = []
        self._summary = None
        self.results_view.reset()
        self._update_summary(ReportSummary(file_name="", total_records=0, records_by_type={}, total_errors=0, errors_by_severity={}, errors_by_code={}, is_submission_ready=False), clean=False)
        self.detail_text.configure(state="normal")
        self.detail_text.delete("1.0", END)
        self.detail_text.configure(state="disabled")
        self.save_btn.configure(state="disabled")

    def _start_validation(self) -> None:
        if not self._current_path:
            messagebox.showwarning("No file", "Please select a CIC submission file first.")
            return
        self.validate_btn.configure(state="disabled")
        self.browse_btn.configure(state="disabled")
        self.save_btn.configure(state="disabled")
        self.status_label.configure(text="Validating...", bootstyle="warning")
        self.progress.pack(fill=X, pady=(0, 16), after=self.file_card_ref())
        self.progress.start(10)
        self._run_validation_thread()

    def file_card_ref(self) -> ttkb.Frame:
        # Helper to know where to insert progress bar; the summary_frame is first
        return self.summary_frame

    def _run_validation_thread(self) -> None:
        import threading

        def run():
            try:
                errors, summary = validate_file(str(self._current_path))
                self.root.after(0, self._validation_done, errors, summary)
            except Exception as exc:
                self.root.after(0, self._validation_failed, str(exc))

        threading.Thread(target=run, daemon=True).start()

    def _validation_done(self, errors: List[FieldError], summary: ReportSummary) -> None:
        self._errors = errors
        self._summary = summary
        self.progress.stop()
        self.progress.pack_forget()
        self.validate_btn.configure(state="normal")
        self.browse_btn.configure(state="normal")
        self.save_btn.configure(state="normal")
        self.results_view.set_errors(errors)
        clean = len({e.line_number for e in errors}) == 0
        self._update_summary(summary, clean=clean)
        self.status_label.configure(
            text="Validation complete" + (" — ready for upload" if summary.is_submission_ready else " — errors found"),
            bootstyle="success" if summary.is_submission_ready else "danger",
        )
        self._show_error_detail(None)

    def _validation_failed(self, message: str) -> None:
        self.progress.stop()
        self.progress.pack_forget()
        self.validate_btn.configure(state="normal")
        self.browse_btn.configure(state="normal")
        self.status_label.configure(text="Validation failed", bootstyle="danger")
        messagebox.showerror("Validation failed", message)

    def _update_summary(self, summary: ReportSummary, clean: bool) -> None:
        clean_records = summary.total_records - len({e.line_number for e in self._errors})
        values = {
            "total_records": f"{summary.total_records:,}",
            "clean_records": f"{clean_records:,}",
            "total_errors": f"{summary.total_errors:,}",
            "ready": "YES" if summary.is_submission_ready else "NO",
        }
        for key, label, title in self._summary_cards:
            label.configure(text=values[key])
            if title == "Submission Ready":
                label.configure(foreground=COLOR_SUCCESS if summary.is_submission_ready else COLOR_ERROR)
        for key, label in self.severity_labels.items():
            count = summary.errors_by_severity.get(key, 0)
            label.configure(text=f"{self._friendly_severity(key)}: {count}")

    def _friendly_severity(self, key: str) -> str:
        return {"structural": "Structural", "field": "Field-level", "business_rule": "Business rule"}.get(key, key)

    def _show_error_detail(self, error: FieldError | None) -> None:
        self.detail_text.configure(state="normal")
        self.detail_text.delete("1.0", END)
        if error is None:
            if not self._errors:
                self.detail_text.insert(END, "No errors to display.")
            else:
                self.detail_text.insert(END, "Select an error from the table above to see details.")
        else:
            subject = error.provider_subject_no or "—"
            lines = [
                f"Line {error.line_number} — Record {error.record_type} — Provider Subject No. {subject}",
                f"Error Code: {error.error_code}",
                f"Severity  : {error.severity}",
                f"Field     : {error.field_name or '—'}",
                f"Value     : {error.offending_value or '—'}",
                "",
                f"Issue: {error.description}",
                "",
                f"Fix suggestion: {error.fix_suggestion or '—'}",
            ]
            self.detail_text.insert(END, "\n".join(lines))
        self.detail_text.configure(state="disabled")

    def _save_report(self) -> None:
        if not self._summary or not self._current_path:
            return
        default = self._current_path.with_name(self._current_path.stem + "_validation_report.txt")
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text report", "*.txt")],
            initialfile=default.name,
            title="Save Validation Report",
        )
        if not path:
            return
        try:
            write_report(self._errors, self._summary, path)
            messagebox.showinfo("Saved", f"Report saved to:\n{path}")
        except Exception as exc:
            messagebox.showerror("Error", f"Could not save report:\n{exc}")


def main() -> None:
    root = ttkb.Window(themename="flatly")
    AppWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
