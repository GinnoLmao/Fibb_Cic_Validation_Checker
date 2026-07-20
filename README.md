# CIC Submission Validator

A standalone Windows desktop application that validates CIC (Credit Information Corporation) credit-data submission files locally before upload. It supports both pipe-delimited `.txt` files and Excel `.xlsx` masterfiles, checks structural layout, field-level rules, and business/cross-field rules, then produces a plain-text report with explanations and fix suggestions.

---

## Table of Contents

- [What it does](#what-it-does)
- [System requirements](#system-requirements)
- [Quick start: run the executable](#quick-start-run-the-executable)
- [Install from source](#install-from-source)
- [Usage](#usage)
  - [Graphical user interface (GUI)](#graphical-user-interface-gui)
  - [Command-line interface (CLI)](#command-line-interface-cli)
  - [Run tests](#run-tests)
- [Project structure](#project-structure)
- [How validation works](#how-validation-works)
- [Editing the schema or rules](#editing-the-schema-or-rules)
- [Rebuilding the executable](#rebuilding-the-executable)
- [Sample test result](#sample-test-result)
- [Troubleshooting](#troubleshooting)

---

## What it does

The validator reads a CIC submission file and checks it in three stages:

1. **Structural / pre-validation** — record order, required header/footer presence, filename format, and exact field count per record type.
2. **Field-level validation** — mandatory/conditional presence, data type, length, domain values, and date formatting.
3. **Business / cross-field rules** — record-type-specific logic such as contact type/value pairs, ID number/value pairs, address ownership flags, and conditional mandatory fields.

Results are shown in the GUI and can be saved as a text report grouped by severity.

### Supported file types

| Format | Expected layout |
|--------|-----------------|
| `.txt` | Pipe-delimited (`\|`) rows. First field is the record type (`HD`, `ID`, `CI`, `FT`, ...). |
| `.xlsx` | One row per record. First column is the record type. Column order must match the CIC field schema. |

The expected filename for a CSDF text submission is:

```text
<ProviderCode>_CSDF_YYYYMMDDhhmmss.txt
```

For example: `RB001800_CSDF_20251212160316.txt`.

---

## System requirements

- Windows 10 or Windows 11 (64-bit)
- For source/Python usage: Python 3.12+ and PowerShell / Command Prompt
- Optional: Excel files need no local Microsoft Excel install; the app uses `openpyxl`

---

## Quick start: run the executable

The fastest way to use the app is the pre-built single-file executable.

1. Open the project folder.
2. Go to `dist\CICSubmissionValidator.exe`.
3. Double-click it.
4. In the app, click **Browse**, select your `.txt` or `.xlsx` CIC file, and click **Validate**.
5. Review results. If there are errors, click **Save Report** to export a `.txt` report.

> The `.exe` is built from `run_gui.py` using PyInstaller and already contains the schema files it needs, so it can be copied to another Windows PC and run without Python installed.

---

## Install from source

If you prefer to run the Python code directly or want to modify the validator:

1. Open a PowerShell or Command Prompt in the project root.
2. Create the virtual environment:

   ```powershell
   python -m venv .venv
   ```

3. Activate it:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

4. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

---

## Usage

### Graphical user interface (GUI)

From the project root with the virtual environment active:

```powershell
.\.venv\Scripts\python.exe run_gui.py
```

What you can do in the GUI:

- **Browse** — pick a `.txt` or `.xlsx` file.
- **Validate** — run the full validation engine.
- Summary cards show total records, clean records, total errors, and submission-readiness.
- **Filter / search** the results table by record type, severity, or keyword.
- Click an error row to see full details and fix suggestions.
- **Save Report** — export the current validation report to a `.txt` file.

### Command-line interface (CLI)

The CLI is useful for automation, CI/CD, or quick checks.

```powershell
.\.venv\Scripts\python.exe run_cli.py "path\to\file.txt"
```

Save a report:

```powershell
.\.venv\Scripts\python.exe run_cli.py "path\to\file.txt" -r "path\to\report.txt"
```

Quiet mode (prints only the final submission-ready status):

```powershell
.\.venv\Scripts\python.exe run_cli.py "path\to\file.txt" -q
```

Exit codes:

- `0` — file is submission-ready (no errors)
- `1` — errors found, or the file does not exist

### Run tests

```powershell
.\.venv\Scripts\python.exe -m pytest tests -q
```

The test suite covers schema loading, text/Excel reading, the validation engine, and report generation.

---

## Using VS Code

The `.vscode/` folder contains `settings.json` and `launch.json` so you can run and debug the project from VS Code.

### 1. Set the Python interpreter

1. Open the project folder in VS Code.
2. Press `Ctrl + Shift + P` (or `Cmd + Shift + P` on Mac) and type **Python: Select Interpreter**.
3. Choose the interpreter inside the virtual environment:

   ```text
   .\.venv\Scripts\python.exe
   ```

   If it is not listed, click **Enter interpreter path...** and browse to `.venv/Scripts/python.exe`.

   The `.vscode/settings.json` file already sets `python.defaultInterpreterPath` to `${workspaceFolder}/.venv/Scripts/python.exe`, so VS Code should suggest it automatically.

### 2. Open the Run and Debug panel

Press `Ctrl + Shift + D` (or `Cmd + Shift + D` on Mac).

### 3. Pick a launch configuration

At the top of the Run and Debug panel, select one of:

- **Python: Run GUI** — launches the desktop app.
- **Python: Run CLI (sample)** — runs the CLI against `Raw Samples/sample data.txt` and writes `report.txt`.
- **Python: Run Tests** — runs the pytest suite.

### 4. Start debugging

Press `F5` or click the green play button (▶).

### If the GUI does not open

1. Try running it manually in the integrated terminal:

   ```powershell
   .\.venv\Scripts\python.exe run_gui.py
   ```

   If that works, the problem is the launch configuration or the selected interpreter.
2. Make sure the **Python** extension by Microsoft is installed.
3. Make sure the interpreter at the bottom-right of VS Code shows `.venv` (e.g., `Python 3.14.x (.venv)`). If it shows a different Python, click it and select the `.venv` one.
4. If the terminal shows an error, copy the full error message and check:
   - `ModuleNotFoundError` → reinstall dependencies with `pip install -r requirements.txt`.
   - `ImportError` or `DLL load failed` → try using the plain `python.exe` in the venv instead of `pythonw.exe`.

### Useful VS Code extensions

- **Python** (Microsoft) — required for Python debugging.
- **Python Test Explorer** — optional, for a GUI test runner.

---

## Project structure

```text
FIBB_CIC_Validation_Checker_V1/
├── .venv/                                  # Python virtual environment
├── .vscode/                                # VS Code launch configurations
│   ├── launch.json
│   └── settings.json
├── dist/                                   # Output folder for the .exe
├── docs/                                   # Reference / source documentation files
├── Raw Samples/                            # Example CIC files
│   ├── RB001800_CSDF_20260531000000.txt
│   ├── RB001800_CSDF_20260531000001.txt
│   ├── sample_data.xlsx
│   └── RB001800_CSDF_20251212160316.txt
├── cic_validator/
│   ├── __init__.py
│   ├── cli.py                              # Command-line entry point
│   ├── core/
│   │   ├── models.py                       # Record / FieldError / ReportSummary dataclasses
│   │   ├── schema_loader.py                # Loads the annotated field schema
│   │   ├── domain_loader.py                # Loads valid-value tables
│   │   ├── rule_loader.py                  # Loads CIC error rules and rule bindings
│   │   ├── rule_primitives.py              # Helper predicates (date, numeric, etc.)
│   │   ├── file_detector.py                # Detects file type and filename format
│   │   ├── text_reader.py                  # Reads pipe-delimited .txt files
│   │   ├── excel_reader.py                 # Reads .xlsx masterfiles
│   │   ├── engine.py                       # Orchestrates all validation stages
│   │   ├── _paths.py                       # Resolves schema files in dev and frozen mode
│   │   └── validators/
│   │       ├── structural.py               # Structural / pre-validation checks
│   │       ├── field_level.py              # Field-level checks
│   │       └── business_rules.py           # Cross-field business rules
│   ├── gui/
│   │   ├── app_window.py                   # Main ttkbootstrap window
│   │   ├── results_view.py                 # Filterable results table
│   │   └── styles.py                       # Theme constants
│   ├── report/
│   │   └── report_writer.py                # Text report generator
│   ├── schema/                             # Runtime schema JSON files
│   │   ├── record_type_field_schema.json   # Annotated CIC field schema
│   │   ├── domains.json                    # Domain / valid-value tables
│   │   ├── error_rules_consolidated.json   # CIC error rule definitions
│   │   ├── rule_bindings.json              # Auto-bound rule -> field map
│   │   └── unmapped_rules.json             # Rules not yet auto-bound
│   └── tools/
│       ├── annotate_schema.py              # Adds metadata to the raw schema
│       └── generate_rule_bindings.py       # Generates rule_bindings.json
├── tests/
│   └── test_engine.py                      # pytest test suite
├── requirements.txt                        # Python dependencies
├── run_gui.py                              # GUI launcher
├── run_cli.py                              # CLI launcher
└── README.md                               # This file
```

---

## How validation works

The validation pipeline in `cic_validator/core/engine.py` does the following:

1. **Detect the file type** (`file_detector.py`) and pick the right reader.
2. **Parse records** into `Record` objects (`text_reader.py` or `excel_reader.py`).
3. **Stage 1 — Structural validation** (`validators/structural.py`):
   - Header must be first, footer last.
   - Each record must have the exact field count defined for its record type.
   - Filename must follow `<ProviderCode>_CSDF_YYYYMMDDhhmmss.txt` for text submissions.
   - Records with structural defects are still parsed but skip later stages to avoid shifted-field false positives.
4. **Stage 2 — Field-level validation** (`validators/field_level.py`):
   - Mandatory and conditional-mandatory fields.
   - Data type (numeric, date, yes/no, domain value).
   - Maximum field length.
5. **Stage 3 — Business rules** (`validators/business_rules.py`):
   - Cross-field checks such as "Contact Type and Contact Value must both be filled or both empty".
   - Conditional rules driven by the `group_rules` metadata in the schema.

Each error is stored as a `FieldError` with a severity (`structural`, `field`, `business_rule`), a CIC error code (e.g. `30-010`), a description, and a fix suggestion.

---

## Editing the schema or rules

Most validation behavior is data-driven from JSON files in `cic_validator/schema/`.

### Change field metadata

Edit `cic_validator/schema/record_type_field_schema.json`. Each field has:

```json
{
  "position": 2,
  "name": "Provider Subject No",
  "data_type": "string",
  "max_length": 20,
  "mandatory": true,
  "mandatory_type": "unconditional",
  "domain": null,
  "block": "A"
}
```

Common data types: `string`, `numeric`, `date`, `yesno`, `domain`.

### Change domain values

Edit `cic_validator/schema/domains.json`.

### Change error rules or bindings

- `cic_validator/schema/error_rules_consolidated.json` stores the rule catalog.
- `cic_validator/schema/rule_bindings.json` maps a rule code to one or more fields.
- `cic_validator/schema/unmapped_rules.json` lists rules the automatic binder could not assign; you can manually add them to `rule_bindings.json`.

### Regenerate from source

Reference/source files (for example `record_type_field_schema_corrected.json`, `domains_master.json`, and the CIC reference markdowns) are kept in `docs/` for documentation purposes.

If you receive a newer corrected schema or domain file:

1. Place it in `docs/`.
2. Replace the corresponding runtime file in `cic_validator/schema/` (or update the tooling scripts if they read from `docs/`).
3. Rerun the tooling scripts:

```powershell
.\.venv\Scripts\python.exe -m cic_validator.tools.annotate_schema
.\.venv\Scripts\python.exe -m cic_validator.tools.generate_rule_bindings
```

These scripts produce the runtime files in `cic_validator/schema/`.

---

## Rebuilding the executable

After any code or schema change, rebuild the `.exe`:

```powershell
.\.venv\Scripts\python.exe -m PyInstaller --clean --onefile --windowed --name CICSubmissionValidator --add-data "cic_validator\schema;cic_validator\schema" --hidden-import cic_validator.cli --hidden-import cic_validator.gui.app_window --collect-data ttkbootstrap run_gui.py
```

The new executable appears at:

```text
dist\CICSubmissionValidator.exe
```

### How schema files are found in the .exe

`cic_validator/core/_paths.py` checks for PyInstaller's `sys._MEIPASS` when the app is frozen, so the executable can locate the bundled `cic_validator/schema/` files even though they are extracted to a temporary folder at runtime.

---

## Sample test result

Using the provided fixtures `Raw Samples\RB001800_CSDF_20260531000000.txt` and `Raw Samples\RB001800_CSDF_20260531000001.txt` (formerly `test data.txt` and `sample data.txt`, renamed to valid CSDF filenames), the validator reports no structural, field-level, or business-rule errors. This is the same behavior verified by `tests/test_engine.py::test_engine_on_small_sample_copy`.

---

## Troubleshooting

| Problem | Likely cause | Fix |
|---------|--------------|-----|
| `.exe` flashes and closes | Missing display, or error before GUI opens | Run `run_gui.py` from source to see the traceback, or run the CLI for headless output. |
| Schema file not found | PyInstaller did not bundle `cic_validator/schema/` | Rebuild with the `--add-data` flag shown above. |
| Excel file reads zero records | Wrong sheet or missing record-type column | Ensure the first column contains the record type (`HD`, `ID`, `CI`, `FT`, etc.). |
| Every record shows many errors | File delimiters are wrong or columns shifted | Open the `.txt` in a text editor and verify pipe (`\|`) separators and field count. |
| Report shows `Line 0` for filename error | Filename does not match CSDF convention | Rename the file to `<ProviderCode>_CSDF_YYYYMMDDhhmmss.txt`. |

If you find a validation rule that should be added or corrected, edit `cic_validator/schema/rule_bindings.json` or the relevant validator module and rerun the tests before rebuilding the executable.
