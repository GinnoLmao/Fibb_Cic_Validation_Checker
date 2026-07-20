"""Entry point for the CIC Submission Validator GUI."""
import sys


def _self_test(argv: list[str]) -> int:
    """Headless smoke test for the frozen executable."""
    from cic_validator.core.engine import validate_file
    from cic_validator.report.report_writer import write_report

    input_path = argv[2]
    output_path = argv[3]
    errors, summary = validate_file(input_path)
    write_report(errors, summary, output_path)
    return 0 if summary.is_submission_ready else 1


if __name__ == "__main__":
    if len(sys.argv) >= 4 and sys.argv[1] == "--self-test":
        sys.exit(_self_test(sys.argv))
    from cic_validator.gui.app_window import main

    main()
