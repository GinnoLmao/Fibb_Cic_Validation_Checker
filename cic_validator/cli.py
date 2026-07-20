"""Command-line interface for the CIC Submission Validator."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from cic_validator.core.engine import validate_file
from cic_validator.report.report_writer import write_report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate a CIC credit-data submission file (pipe-delimited .txt or .xlsx).",
    )
    parser.add_argument("file", help="Path to the submission file")
    parser.add_argument(
        "--report",
        "-r",
        metavar="PATH",
        help="Write a human-readable validation report to PATH",
    )
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Only print the final submission-ready status",
    )
    args = parser.parse_args(argv)

    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: file not found: {file_path}", file=sys.stderr)
        return 1

    errors, summary = validate_file(str(file_path))

    if not args.quiet:
        print(f"File: {summary.file_name}")
        print(f"Total records: {summary.total_records:,}")
        print(f"Errors found : {summary.total_errors:,}")
        print(f"  Structural : {summary.errors_by_severity.get('structural', 0):,}")
        print(f"  Field-level: {summary.errors_by_severity.get('field', 0):,}")
        print(f"  Business   : {summary.errors_by_severity.get('business_rule', 0):,}")
    print(f"Submission-ready: {'YES' if summary.is_submission_ready else 'NO'}")

    if args.report:
        write_report(errors, summary, args.report)
        if not args.quiet:
            print(f"Report written to: {args.report}")

    return 0 if summary.is_submission_ready else 1


if __name__ == "__main__":
    sys.exit(main())
