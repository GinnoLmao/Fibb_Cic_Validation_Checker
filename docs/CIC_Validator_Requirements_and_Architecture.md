# CIC Credit Data Submission Validator
## Requirements Analysis & System Architecture Specification — v1.1 (revised)

**Prepared for:** Bank IT Officer (Credit Data Submission to Credit Information Corporation)
**Purpose of this document:** Complete, execution-ready specification for an agentic AI coder to build the system from scratch, with no further design decisions required.
**Status:** v1.1 — revised to reflect corrections and additions made after the original draft (see version note below).

**Companion data files (bundled alongside this document — this is the current, corrected file set):**
- `CIC_Fields_Excel_Complete_Reference.md` — the authoritative, complete companion document: full file-format rules, every record type's field count, the **definitive mandatory-fields list** (§3 of that document — supersedes any mandatory-field information in this document), conditional/group mandatory rules (§4), and the **complete** domain/valid-value tables for every coded field, including the full PSIC/PSOC/Currency/Country lists written out in full. Treat this document as the primary data reference; this architecture document covers structure and build process.
- `record_type_field_schema.json` — verified, position-indexed field list for all 10 CIC record types.
- `error_rules_consolidated.json` — 703 canonical CIC error rules.
- `domains_master.json` — the complete, machine-readable form of every domain table in the Complete Reference document. **This is fully populated — there is no missing or placeholder domain data.** Load this directly as the application's runtime domain source (as `domains.json`); no extraction step is required to build it.
- `sample_data.txt` and a real CIC-issued `ERROR_SUMMARY` file — test fixtures. `sample_data.txt` contains one confirmed, intentional structural defect (a missing delimiter in one `ID` record) useful as a primary integration-test case — see §9 Phase 5.

**Version note:** the original draft of this document assumed the domain/lookup data and full mandatory-field list still needed to be extracted from source Excel workbooks, and specified a plain-Tkinter GUI. Both of those have since been superseded: domain extraction is complete (see `domains_master.json` and the Complete Reference document), and the GUI specification in §6 has been replaced with a modern themed design. Sections below have been corrected accordingly — where you see a note like *"(superseded — see below)"* it means the surrounding text reflects the outdated assumption and the corrected version follows.

---

## 1. Problem Statement

The bank submits credit data to the Credit Information Corporation (CIC) as a pipe-delimited text file (CSDF format). CIC validates submissions in three sequential phases — **PRE** (structural), **CPS/CPC** (Checking Phase, Subject/Contract field-level and business-rule validation), and **LPS/LPC** (Loading Phase, DB load) — but feedback on errors can take **months** to come back, and a single structural error can invalidate an entire submission. The bank's IT officer currently has no way to catch these errors before submission.

**Goal:** A standalone desktop application that ingests the bank's data (Excel masterfile or the final pipe-delimited `.txt`) and reproduces CIC's PRE + CPS/CPC validation logic locally, so errors are caught and explained — with row/field-level detail and plain-English fixes — in seconds, not months.

## 2. Goals

1. Validate submission data against the **complete CIC rule set**: structural (record type, field count, provider code), field-level (format/length/domain/date), and cross-field/business rules (mandatory combinations, conditional rules, numeric ranges, duplicate detection).
2. Support **all 10 CIC record types**: `HD`, `ID`, `BD`, `CI`, `CN`, `CC`, `CS`(a.k.a. `UT`), `NE`, `SL`, `FT`.
3. Accept **either** an Excel masterfile (`.xlsx`) or a converted pipe-delimited `.txt` file, auto-detected — no manual mode switch.
4. Present results in a **clean, uncluttered desktop GUI**, plus a **downloadable, redesigned `.txt` report** that is dramatically easier to read and act on than CIC's raw `ERROR_SUMMARY` output.
5. Be **packaged as a standalone Windows application** (no Python/pip required on the target machine) for deployment on a separate bank workstation.
6. Be **config-driven**: schema, domains, and error rules live in external JSON files, not hardcoded — so future CIC manual revisions only require a config update, not a rebuild.

## 3. Non-Goals (v1)

- Not a replacement for the actual CIC submission/upload process (FTPS upload, encryption, zipping remain manual per the existing CIC deck).
- No CSV/Excel export of the report — only the on-screen GUI table and the downloadable clean `.txt` report (per explicit requirement).
- No auto-correction of data (v1 detects and explains; it does not silently rewrite the source file).
- No multi-user/server component — single-user, single-machine desktop tool.

---

## 4. Reference Data Understanding

### 4.1 Submission File Lifecycle (from `Data_Format__FileZilla_.pdf`)

1. Data encoded into an Excel masterfile.
2. Saved as CSV, then Windows Region "List Separator" is changed from `,` to `|` (one-time OS setting) so subsequent CSV saves are pipe-delimited.
3. Saved as `.txt`, named `<ProviderCode>_CSDF_<Timestamp>.txt`.
   - `ProviderCode`: 8-alphanumeric assigned provider number.
   - `Timestamp`: `YYYYMMDDhhmmss`, 24-hour clock, file-creation time.
   - Example: `BANK1234_CSDF_20150130143010.txt`
4. File must be UTF-8, **without BOM**.
5. `.txt` is zipped, then the zip is encrypted (GPG), then uploaded via FTPS (FileZilla) into the provider's `/Submission/Input` folder.
6. CIC runs 3 validation phases (see 4.2), and eventually returns an `ERROR_SUMMARY` report (see sample provided: `RB001800_CSDF_20251212160316_ERROR_SUMMARY_LPS.txt`) — flat pipe format: `ProviderCode|ErrorType|ErrorCode|Total Number of Errors|Error Description`. This is what our tool's output must be a dramatically clearer replacement for, run **locally and instantly** instead of waiting for CIC.

### 4.2 Validation Phases (map directly to our engine's stages)

| CIC Phase | Our Engine Stage | What it checks |
|---|---|---|
| **PRE** (Pre-Validation) | **Stage 1 — Structural** | Record type recognized; correct field count per record type; provider code present, correct length, consistent between filename and file content |
| **CPS / CPC** (Checking Phase Subject / Contract) | **Stage 2 — Field-level** + **Stage 3 — Cross-field/business rules** | Per-field format/domain/length/date validity; mandatory-field combinations; conditional rules; numeric ranges (e.g. age); duplicate detection (e.g. Provider Subject No.) |
| **LPS / LPC** (Loading Phase) | *(out of scope — DB load on CIC's side)* | N/A — but the sample `ERROR_SUMMARY_LPS.txt` shows LPS-stage errors are still just Stage 2/3-type rule violations (e.g. `10-090` duplicate subject, `20-137` age range) — our Stage 2/3 already covers these |

### 4.3 Record Types & Field Counts (verified against `30-010` error explanation and cross-checked against the `test` sheet header rows — **exact match**)

| Code | Name | Field Count |
|---|---|---|
| `HD` | Header | 6 |
| `ID` | Individual Data | 123 |
| `BD` | Business Data | 49 |
| `CI` | Installment Contract | 143 |
| `CN` | Non-Installment Contract | 127 |
| `CC` | Credit Card | 143 |
| `CS` / `UT` | Services/Utilities | 29 |
| `NE` | Negative Event | 10 |
| `SL` | Subject Link | 7 |
| `FT` | Footer | 4 |

Full, position-indexed field names for every record type are provided in `schema/record_type_field_schema.json` (verified: extracted field counts match the table above exactly for all 10 types). This file is the **canonical schema source** — do not hand-transcribe field lists into code; parse this JSON at build/runtime.

### 4.4 Domain / Lookup Tables — ✅ COMPLETE (superseded original extraction plan)

**This section originally described a domain-extraction task as a Phase 1 build blocker. That extraction has already been done.** `domains_master.json` contains every domain table, fully populated — including the complete PSIC (2,037 entries), PSOC (637 entries), Currency (178 entries), and Country (249 entries) reference lists, plus every smaller coded domain (Title, Gender, Civil Status, Address Type per record type, Identification Type, Contact Type, Role, Contract Phase, Contract Type per product, Contract Status per product, Event Status, Company Role, Firm Size, Legal Form, Payment Method/Periodicity, Good Type, Guarantees, Credit Purpose, Yes/No, etc.). The full human-readable version of every table is also in `CIC_Fields_Excel_Complete_Reference.md` §5.

**What the agentic build should do:** load `domains_master.json` directly as `domains.json` at Phase 1 — there is no extraction algorithm to write or debug for v1. A `tools/extract_domains.py` script implementing a domain re-extraction algorithm is still worth writing (see §9 Phase 1 and §8 config-update path) so that a **future** CIC manual revision can be re-extracted without re-doing this work by hand, but it is a non-blocking utility, not a Phase 1 dependency.

**Known layout quirk worth preserving in `extract_domains.py`'s design, for future re-extractions:** the source Excel sheets are laid out as a tiled grid of small lookup tables — multiple domain tables sit side-by-side in the same header row, and additional tables are stacked vertically below, each introduced by its own header cell. Two specific quirks were found and corrected during the original extraction: (1) some domain tables use a 3-column layout (Value | short description | long-form sub-description) rather than a plain 2-column Value/Description pair — a naive 2-column reader will drastically undercount these (this affected `CI`'s and `CN`'s `ContractTypeDomain`, both now corrected in `domains_master.json`); (2) some tables have no blank-row separator before the next table's header, causing a naive parser to bleed one table's rows into the next unless it explicitly stops at the next detected header rather than relying on blank-row detection alone.

### 4.4a Mandatory Fields — ✅ COMPLETE (new section, not in original draft)

The original draft of this document did not include a mandatory-fields specification. This gap has since been closed: **`CIC_Fields_Excel_Complete_Reference.md` §3 is the definitive, corrected mandatory-fields list** for all 10 record types, and §4 of that document covers conditional-mandatory fields (e.g. `CI`'s `Last Payment Amount` and `Overdue Days` are only mandatory once `Contract Phase` is Active/Closed/Closed-in-Advance) and "at least one of" group rules (e.g. address completeness, at-least-one-Contact:Type).

**This has direct architectural impact, not just data impact:** a plain missing-mandatory-field check must run *before* any domain/format check for that field, since an empty mandatory field and a malformed one are different errors with different fix messages. See §5.5's `required()` and new `at_least_one_group_of()` primitives, and §9 Phase 2 for how the field schema gets annotated with this information.

**Important correction:** an earlier attempt at determining mandatory fields undercounted badly by only checking a single header row's font color, and found essentially one mandatory field per record type. That was wrong. The corrected list in the Complete Reference document was derived from two combined sources — a fully worked, annotated sample record and the CIC error rulebook's explicit `FIELD 'X' IS MANDATORY` rules — and is substantially larger and more accurate. Do not use any other mandatory-field list.

### 4.5 Error Rulebook

`Error_Codes_and_Descriptions.xlsx`, sheet `Consolidated`, is the **canonical, de-duplicated rule source** (703 unique error codes after dedup — verified programmatically). Columns: `Error Code`, `Error Description`, `Solution`, `Re-phrased`. This has been extracted into `schema/error_rules_consolidated.json` already — use it directly as the seed for the rule engine's rule table; do not re-parse the spreadsheet at runtime.

**Error code prefix taxonomy** (inferred from code structure and cross-checked against the real `ERROR_SUMMARY_LPS.txt` sample, all of whose codes exist in the Consolidated sheet):

| Prefix | Meaning (observed) | Example |
|---|---|---|
| `10-xxx` | Field-level content/format/domain error | `10-004` FIELD 'GENDER' IS NOT CORRECT |
| `20-xxx` | Cross-field / conditional business rule | `20-137` INDIVIDUAL AGE SHOULD BE BETWEEN 18 AND 100 YEARS |
| `1-xxx` / `2-xxx` | Mutual-exclusivity / either-or field rules | `1-001` FIELDS 'ROLE' AND 'COMPANY ROLE' CANNOT BE BOTH EMPTY OR FILLED IN |
| `30-xxx` | Structural / Pre-Validation (file & record level) | `30-009` RECORD TYPE IS NOT VALID; `30-010` FIELD COUNT NOT VALID FOR RECORD TYPE |
| `40-xxx` | Provider/filename consistency | `40-006` PROVIDER CODE IN FILENAME INCONSISTENT WITH SUBMITTING PROVIDER |
| `50-xxx` / `60-xxx` | Additional field/cross-record rules (contract-level, per `Categorized (Contract)` sheet) | — |
| `99-xxx` | Miscellaneous/other | — |

**Representative business rules seen in real production data** (from the supplied `ERROR_SUMMARY_LPS.txt` — all present in the Consolidated rulebook, confirming full coverage):
- `10-090` — duplicate Provider Subject No. assigned to another subject (cross-record uniqueness check).
- `20-137` — individual age must be between 18–100 (computed from Date of Birth vs. Subject Reference Date).
- `20-050` / `20-052` — conditional format rules: if Identification Code = `TIN`, number must be 9–12 digits, numeric only; if `GSIS`, number must be exactly 11 digits (note: Consolidated sheet says "10 or 11" in one variant, other sheets say "11" only — this remains an open item, still unresolved as of this revision; default to the stricter `=11` and flag it, see §11).
- `20-094` / `20-138` / `20-139` / `20-130` — a cluster of address-completeness rules: if any single address sub-field is filled, `Address:Type` must be filled; either `FullAddress` OR the trio `StreetNo`+`City`+`Province` must be filled; both Address 1 and Address 2 `Type` must be present.
- `20-104` — at least one `Contact:Type` must be filled in.
- `10-069` — `Identification Type` and `Identification Code`(Number) must be both-empty or both-filled (paired mandatory fields — this pattern recurs across ID/Contact/Address triplets and should be implemented as a **generic "paired fields" rule type**, not one-off code).

These patterns (paired-mandatory, conditional-format-by-code, address-completeness, numeric-range, cross-record-uniqueness) should be implemented as **reusable rule primitives** in the engine (§7.4), not hand-coded per error number — the 703-row rulebook is large, but the underlying rule *shapes* are a small, finite set.

### 4.6 File-Level Rules

- **Filename regex:** `^[A-Za-z0-9]{8}_CSDF_\d{14}\.txt$`
- **Encoding:** UTF-8, no BOM (flag if BOM detected — `EF BB BF` at file start).
- **Delimiter:** `|` (pipe), no quoting/escaping observed in samples.
- **Date format (all date fields):** `DDMMYYYY`, no separators, always 8 digits.
- **Provider Code consistency:** the `ProviderCode` in the filename, in the `HD` record, and in every subsequent detail record must match (errors `30-003`, `30-006`, `40-006`).

---

## 5. Application Architecture

### 5.1 Tech Stack

- **Python 3.11+**
- **`ttkbootstrap`** (a themed layer over `ttk`) for the GUI — **superseded from plain Tkinter/ttk in the original draft.** This is the one added GUI dependency; it stays lightweight and PyInstaller-compatible while giving a modern, flat, themed look (see §6 for the full design directive). Note it in `requirements.txt` and the README's tech-stack section.
- **openpyxl** for `.xlsx` reading (masterfile mode).
- **Standard library only** for `.txt` parsing (no pandas dependency needed for correctness/simplicity of packaging — pandas is optional/avoid unless a clear need arises, to keep the PyInstaller build small and dependency-light).
- **PyInstaller** for packaging into a standalone Windows executable.

### 5.2 Module / File Structure

```
cic_validator/
├── main.py                      # App entry point, launches GUI
├── gui/
│   ├── app_window.py             # Main window: file picker, validate button, results view
│   ├── results_view.py           # Filterable/sortable results table (themed Treeview)
│   └── styles.py                 # ttkbootstrap theme + custom palette (fonts, colors, spacing) — see §6
├── core/
│   ├── file_detector.py          # Detects input type (.xlsx vs .txt), validates filename/encoding
│   ├── excel_reader.py           # Reads masterfile rows into normalized record dicts
│   ├── text_reader.py            # Reads pipe-delimited .txt into normalized record dicts
│   ├── schema_loader.py          # Loads record_type_field_schema.json (with mandatory-field annotations, §4.4a)
│   ├── domain_loader.py          # Loads domains.json (= domains_master.json, already complete — see §4.4)
│   ├── rule_loader.py            # Loads error_rules_consolidated.json into rule objects
│   ├── rule_primitives.py        # Reusable rule types: required, max_length, domain_lookup,
│   │                              #   date_format, conditional_format_by_code, paired_fields,
│   │                              #   at_least_one_of, at_least_one_group_of, numeric_range,
│   │                              #   cross_record_unique — see §5.5
│   ├── validators/
│   │   ├── structural.py         # Stage 1: record type, field count, provider code (PRE)
│   │   ├── field_level.py        # Stage 2: per-field checks (10-xxx) — mandatory check runs first, see §4.4a
│   │   └── business_rules.py     # Stage 3: cross-field/cross-record checks (20-xxx, 1-xxx, etc.)
│   ├── engine.py                 # Orchestrates Stage 1 → 2 → 3, collects ValidationResult list
│   └── models.py                 # Dataclasses: Record, FieldError, ValidationResult, ReportSummary
├── report/
│   └── report_writer.py          # Builds the clean, human-readable downloadable .txt report
├── schema/
│   ├── record_type_field_schema.json   # annotated in Phase 2 with mandatory/mandatory_type/mandatory_condition
│   ├── domains.json                     # = domains_master.json, copied in directly at Phase 1 — already complete
│   ├── error_rules_consolidated.json
│   └── unmapped_rules.json              # rules that couldn't be auto-bound to a field+primitive (Phase 2) — reviewed, not guessed
├── tools/
│   └── extract_domains.py        # Non-blocking utility for future re-extraction if the CIC manual is revised — see §4.4
├── tests/
│   └── ...                       # Unit tests per rule primitive + integration test using sample_data.txt (§9 Phase 5)
├── build.spec                    # PyInstaller spec file
└── requirements.txt               # includes ttkbootstrap
```

### 5.3 Data Flow

```
[User picks file] 
      │
      ▼
file_detector.py ── determines: Excel masterfile | CSDF .txt | invalid
      │
      ├── Excel path ──► excel_reader.py ──► List[Record]
      └── .txt path  ──► text_reader.py  ──► List[Record]  (+ filename/encoding checks)
      │
      ▼
engine.py
   Stage 1 (structural.py)   — uses schema_loader
   Stage 2 (field_level.py)  — uses schema_loader + domain_loader
   Stage 3 (business_rules.py) — uses rule_primitives + cross-record indexes
      │
      ▼
List[FieldError] + ReportSummary
      │
      ├──► results_view.py   (on-screen GUI table, filterable/sortable)
      └──► report_writer.py  (clean downloadable .txt, on demand)
```

### 5.4 Core Data Models (`core/models.py`)

```python
@dataclass
class Record:
    record_type: str          # e.g. "ID"
    line_number: int          # 1-indexed source line/row
    provider_subject_no: str | None
    fields: dict[str, str]    # field name -> raw value (position-mapped via schema)

@dataclass
class FieldError:
    error_code: str
    category_prefix: str      # "10", "20", "30", "1", etc.
    record_type: str
    line_number: int
    provider_subject_no: str | None
    field_name: str | None    # None for record-level/structural errors
    offending_value: str | None
    description: str          # from rulebook
    fix_suggestion: str       # from rulebook "solution"/"rephrased_fix"
    severity: Literal["structural", "field", "business_rule"]

@dataclass
class ReportSummary:
    file_name: str
    total_records: int
    records_by_type: dict[str, int]
    total_errors: int
    errors_by_severity: dict[str, int]
    errors_by_code: dict[str, int]
    is_submission_ready: bool   # True only if zero structural + zero field + zero business errors
```

### 5.5 Rule Primitives (`core/rule_primitives.py`) — implement once, apply many times

| Primitive | Used for | Example error codes |
|---|---|---|
| `required(field)` | Unconditional mandatory field presence | See `CIC_Fields_Excel_Complete_Reference.md` §3 — this list is now much larger than originally scoped (e.g. `10-109`, `10-120`, `20-001`–`20-004`, `10-150`–`10-163`, and many more) |
| `required_conditional(field, condition)` | **New primitive — not in original draft.** Conditional mandatory fields, e.g. `CI`'s `Last Payment Amount`/`Overdue Days` only mandatory when Contract Phase ∈ {AC, CL, CA} | `20-089`, `20-090`, `20-092`, `10-253`, `10-268` — see Complete Reference §4 |
| `at_least_one_group_of(group_a_fields, group_b_fields)` | **New primitive — not in original draft.** "Either this whole group is filled, or that whole group is" — needed for address-completeness rules (FullAddress alone, OR StreetNo+City+Province together) | `20-131`, `20-132`, `20-139`, `20-141`, `2-139`, `2-141`, `2-143`, `2-145`, `2-146`, `2-150`, `2-151` — see Complete Reference §4 |
| `max_length(field, n)` | Length caps | `10-003`, `10-118` |
| `domain_lookup(field, domain_name)` | Controlled-vocabulary fields | `10-004`, `10-006`, `10-009`, `10-010` |
| `date_format(field, "DDMMYYYY")` | All date fields | `10-005`, `10-011`, `10-013` |
| `conditional_format_by_code(trigger_field, trigger_value, target_field, pattern)` | e.g. TIN/GSIS length-by-type rules | `20-050`, `20-052` |
| `paired_fields(field_a, field_b)` | Both-empty-or-both-filled pairs | `10-069`, `1-001` |
| `at_least_one_of(fields)` | e.g. Contact:Type | `20-104` |
| `numeric_range(field_or_derived, min, max)` | Age range | `20-137` |
| `cross_record_unique(field, scope)` | Duplicate Provider Subject No. | `10-090` |
| `record_type_valid()` / `field_count_matches_schema()` | Structural | `30-009`, `30-010` |
| `provider_code_consistency()` | Filename ↔ HD ↔ detail records | `30-003`, `30-006`, `40-006` |

**Check ordering within `field_level.py` matters:** for every field, `required()` (or `required_conditional()`) must run *before* `domain_lookup()`/`date_format()`/other content checks on that same field — an empty mandatory field and a malformed one are different errors with different messages, and running content checks on an empty value produces a confusing/wrong error.

Each rule loaded from `error_rules_consolidated.json` should declare which primitive(s) and which field(s)/record type(s) it applies to. Since the JSON only has free-text descriptions (no machine-readable field bindings), **Phase 2 of the build (§9)** requires a one-time semi-automated mapping pass: parse each rule's description text (which consistently names the field in single-quotes, e.g. `FIELD 'GENDER' IS NOT CORRECT`) to bind it to a schema field name + primitive. Where text parsing is ambiguous, record the rule in `schema/unmapped_rules.json` (`{error_code, description, reason_unmapped}`) and implement a documented no-op rather than guessing — a wrong binding produces false positives/negatives, which undermines trust in the tool.

---

## 6. GUI Specification — Modern Themed Design (supersedes original plain-Tkinter spec)

**This entire section was rewritten.** The original draft specified a plain `ttk` interface. That has been replaced with a modern, themed design using `ttkbootstrap` — still a single window, still no nested dialogs beyond the file picker and save dialog, but with deliberate visual polish. The functional layout (file picker → validate → summary → filterable results table → detail panel → download report) is unchanged; only its visual execution is upgraded.

### 6.1 Design Principles

- **Library:** `ttkbootstrap` (a themed layer over `ttk`) — the single added GUI dependency. Chosen because it's PyInstaller-compatible and lightweight, while giving flat, modern, consistently-styled widgets without a heavyweight framework.
- **Theme:** a clean flat light theme (e.g. `ttkbootstrap`'s `"flatly"` or `"cosmo"`). Define a small, deliberate palette in `gui/styles.py`:
  - One accent color (a navy/deep-blue tone, evoking the CIC brand) for primary actions and header accents.
  - A neutral gray/white base for everything else.
  - Status colors (green/amber/red) used *only* to indicate pass/warning/error — never decoratively.
- **Whitespace and grouping:** generous padding; related controls grouped into visually distinct cards/panels (file selection, summary stats, and the results table each read as a separate visual block) rather than a flat stack of unrelated widgets.
- **Consistency:** consistent corner rounding and button styling throughout (handled natively by the `ttkbootstrap` theme); one font family with a clear size/weight hierarchy distinguishing window title, section headers, table content, and helper/secondary text.
- **Zero added clutter:** this is a visual redesign of the *existing* flow — no new screens, no new features, still no CSV/Excel export anywhere in the UI.

### 6.2 Layout (single main window, ~1100×700, resizable)

```
┌──────────────────────────────────────────────────────────────────┐
│  CIC Submission Validator                                    [_][□][X] │
├──────────────────────────────────────────────────────────────────┤
│  ┌── File card ─────────────────────────────────────────────┐    │
│  │  [ Choose File... ]   No file selected                    │    │
│  │  [        Validate        ]  (disabled until file chosen) │    │
│  └────────────────────────────────────────────────────────────┘  │
├──────────────────────────────────────────────────────────────────┤
│  ┌── Summary stat cards ────────────────────────────────────┐    │
│  │   1,204        1,180           37                          │  │
│  │   Total       ✅ Clean       ⚠ Errors                      │  │
│  │   Records                    2 structural·20 field·15 biz  │  │
│  └────────────────────────────────────────────────────────────┘  │
├──────────────────────────────────────────────────────────────────┤
│  Filter: [ All Types ▾ ] [ All Severities ▾ ] [ Search field... ] │
│  ┌── Results table card ────────────────────────────────────┐    │
│  │ ● │ Line │ Type │ Subject No. │ Field    │ Code   │ Issue │    │
│  │ 🔴│  42  │ ID   │ PSN-001A    │ Gender   │ 10-004 │ ...   │    │
│  │  (alternating row shading, hover highlight, status dot)   │    │
│  └────────────────────────────────────────────────────────────┘  │
│  (click a row → detail panel below shows full description + fix) │
│  ┌── Detail panel card ─────────────────────────────────────┐    │
│  │  Error 10-004 — FIELD 'GENDER' IS NOT CORRECT              │  │
│  │  Line 42, record ID, Provider Subject No. PSN-001A          │  │
│  │  Value found: "Male"                                        │  │
│  │  Fix: Gender must be one of M, F. Replace "Male" with "M".  │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                    │
│  [ Download Clean Report (.txt) ]  (secondary/outline style)      │
└──────────────────────────────────────────────────────────────────┘
```

### 6.3 Component Notes

- **Summary panel:** compact stat cards — large number, small label underneath (e.g. "1,204" over "Total Records") — scannable in under a second, not a dense line of text.
- **Results table:** themed `ttk.Treeview` (styled via `ttkbootstrap`) with alternating row shading and a hover/selection highlight; status conveyed via a small colored dot/icon in its own leading column, not by coloring entire rows (which gets visually noisy at scale).
- **Progress feedback:** a themed, *determinate* progress bar with a live "Validating record X of Y" label during processing of large files, so the UI never appears frozen.
- **Buttons:** exactly one accent-colored primary action ("Validate"); every other action ("Download Clean Report") styled as clearly secondary/outline. Never show multiple competing high-emphasis buttons at once.
- **Empty/initial state:** a friendly, unobtrusive placeholder icon plus a short one-line hint ("Choose an Excel masterfile or a CSDF .txt file to begin"), styled consistently with the rest of the theme, instead of a blank white table area.
- **No CSV/Excel export button anywhere** — only "Download Clean Report (.txt)," as specified in §3 Non-Goals.

---

## 7. Downloadable Report Specification (`report/report_writer.py`)

Replaces CIC's flat, aggregate-only `ProviderCode|ErrorType|ErrorCode|Total Number of Errors|Error Description` format with a structured, readable document. Target format (plain `.txt`, fixed-width/aligned sections, no external dependencies so it opens cleanly in Notepad):

```
==============================================================
 CIC SUBMISSION VALIDATION REPORT
==============================================================
 Source file : RB001800_CSDF_20251212160316.txt
 Validated   : 2026-07-16 14:32
 Provider    : RB001800

 SUMMARY
 --------------------------------------------------------------
 Total records            : 1,204
 Records with no errors   : 1,180
 Records with errors      :    24
 Total errors found       :    37
   Structural (PRE)       :     2
   Field-level            :    20
   Business rule          :    15
 Submission-ready         : NO — resolve errors below before upload
==============================================================

 SECTION 1: STRUCTURAL ERRORS (fix these first — they can invalidate
            the entire file)
 --------------------------------------------------------------
 [1] Line 618 — Record Type "D" is not a recognized record type
     Error Code : 30-009
     Why        : Valid record types are HD, ID, BD, CI, CN, CC, CS,
                  NE, SL, FT. "D" is not one of these.
     Fix        : Check line 618 — this was likely meant to be "ID".

 SECTION 2: FIELD-LEVEL ERRORS
 --------------------------------------------------------------
 [2] Line 42 — Record ID — Provider Subject No. PSN-001A
     Field      : Gender
     Value found: "Male"
     Error Code : 10-004
     Why        : Gender must be one of: M, F
     Fix        : Replace "Male" with "M"
 ... (grouped, numbered, one block per error)

 SECTION 3: BUSINESS RULE / CROSS-FIELD ERRORS
 --------------------------------------------------------------
 [3] Line 205 — Record ID — Provider Subject No. PSN-118C
     Rule       : Individual age must be between 18 and 100 years
     Error Code : 20-137
     Why        : Date of Birth 14121974 vs. Subject Reference Date
                  31052026 computes to an out-of-range age.
     Fix        : Verify Date of Birth is correct.

==============================================================
 END OF REPORT
==============================================================
```

- Errors within each section grouped by `Provider Subject No.` when present, so the officer can jump to one subject and see everything wrong with it at once, rather than one error at a time out of context.
- Report is generated in-memory from the same `List[FieldError]` used for the on-screen table — one source of truth, no duplicate logic.
- Save dialog defaults to `<original_filename>_VALIDATION_REPORT_<timestamp>.txt`.

---

## 8. Packaging & Deployment

- Build with **PyInstaller**, one-folder mode (`--onedir`, not `--onefile`) for faster startup and easier debugging on-site; ship the folder as a zip.
- Bundle `schema/*.json` alongside the executable (PyInstaller `--add-data`); the app loads them from the executable's own directory, not from a hardcoded dev path.
- **Bundle `ttkbootstrap`'s theme assets too** — verify these aren't silently excluded by PyInstaller's default module analysis (a common gotcha with themed Tkinter libraries); test the packaged build's visual appearance, not just that it launches.
- Target: Windows 10/11 64-bit (matches the bank workstation environment implied by the CIC FileZilla screenshots).
- No installer required for v1 — a folder the officer can copy via USB/network share and run `CIC_Validator.exe` directly satisfies "deployed on a separate computer."
- Document the rebuild command in a `README.md`:
  ```
  pyinstaller --onedir --windowed --add-data "schema;schema" --name CIC_Validator main.py
  ```
- **Config update path:** since CIC revises its manual periodically, document that `schema/error_rules_consolidated.json`, `schema/domains.json`, and `schema/record_type_field_schema.json` can be swapped out (re-run `tools/extract_domains.py` against an updated CIC Excel workbook, following the layout-quirk handling notes in §4.4) without touching application code, then just re-zip the folder.

---

## 9. Build Sequence (for the agentic coder to execute, in order) — revised

**Phase 0 — Setup**
- Scaffold the module structure from §5.2.
- Place `record_type_field_schema.json`, `error_rules_consolidated.json`, and `domains_master.json` into `schema/` (the last one copied/renamed directly to `schema/domains.json` — see Phase 1).

**Phase 1 — Load config, verify structural data** *(no longer an extraction phase — domains are already complete)*
- Load `domains_master.json` directly as `schema/domains.json`. **Do not write a from-scratch extraction algorithm as a blocking task** — the domain data is already fully populated (see §4.4).
- Write `tools/extract_domains.py` as a non-blocking utility implementing the layout-handling notes in §4.4, for future re-extraction only — it is not required to produce today's `domains.json`.
- Write an automated test asserting `record_type_field_schema.json` field counts equal the table in §4.3 exactly.
- Spot-check domain sanity: Gender resolves to exactly `{M, F}`; YesNoDomain to `{0,1}`; Address Type (Individual) to `{MI, AI}`; Address Type (Business) to `{MT, AT}` — use as automated assertions.

**Phase 2 — Mandatory-field annotation + rule-to-field binding** *(expanded from original scope)*
- **New step:** annotate `record_type_field_schema.json` with `mandatory: true/false`, `mandatory_type: "unconditional"|"conditional"`, and `mandatory_condition` (where applicable) for every field, using `CIC_Fields_Excel_Complete_Reference.md` §3 and §4 as the source. Add a separate `address_completeness_rules` structure per record type for the "at least one of" address groups (see that document's §5 recommended-schema-update pattern).
- Write an automated test asserting every field named in the Complete Reference §3 is flagged `mandatory: true` in the annotated schema.
- Parse `schema/error_rules_consolidated.json`; for each rule, extract the quoted field name from `Error Description` where present (regex `FIELD '([^']+)'`), map to the corresponding schema field(s) (may appear multiple times, e.g. `Address 1:`/`Address 2:` variants, `ID 1/2/3:` variants), and assign a rule primitive per §5.5's table (including the new `required_conditional()` and `at_least_one_group_of()` primitives).
- Rules that don't match the `FIELD '...'` pattern require reading the `Solution`/`Re-phrased` text and hand-classifying — don't guess silently. Rules that can't be confidently automated become a documented no-op (`# TODO: manual rule, needs CIC manual confirmation`) **and** get recorded in `schema/unmapped_rules.json` (`{error_code, description, reason_unmapped}`) for later review.

**Phase 3 — Core engine**
- Implement `core/models.py`, `core/rule_primitives.py` (including `required_conditional()` and `at_least_one_group_of()`), `core/validators/*.py`, `core/engine.py` per §5.4–5.5.
- Implement `core/file_detector.py`, `core/excel_reader.py`, `core/text_reader.py`.
- Ensure `field_level.py` runs the mandatory check before any content/format check on the same field (§5.5 ordering note).

**Phase 4 — Report + GUI**
- Implement `report/report_writer.py` per §7.
- Implement `gui/*` per the revised §6 (`ttkbootstrap`-based, modern themed design), wired to `core/engine.py`.

**Phase 5 — Testing**
- Unit tests per rule primitive, including the two new primitives.
- **Primary integration test:** use `sample_data.txt` (1 HD, 4 ID, 4 CI, 1 FT records). It contains one confirmed, intentional structural defect — a missing delimiter in one `ID` record's `ID 3: Issued By` field, which shifts every field after position 76 by one. Assert the engine reports exactly one error, `30-010` (FIELD COUNT NOT VALID FOR RECORD TYPE), on that record, and zero errors on every other record in the file.
- Secondary reference: the real `ERROR_SUMMARY_LPS.txt` file — use only as a reference for what CIC's old flat report format looks like; do not attempt to reproduce its format (§7 supersedes it), and do not assume its error codes are reproducible without full-file context (e.g. duplicate-detection rules need the whole file, not a single record).

**Phase 6 — Packaging**
- Build PyInstaller spec, verify the packaged `.exe` runs standalone with `ttkbootstrap` theme assets correctly bundled (test on a machine without a Python install if possible), produce the deployable folder/zip.

---

## 10. Acceptance Criteria

- [ ] App launches as a standalone `.exe` with no Python installed on the target machine.
- [ ] Both `.xlsx` and `.txt` inputs are accepted with no manual mode selection.
- [ ] All 10 record types are recognized and validated (structural + mandatory-field + field-content + business rules).
- [ ] Every field listed in `CIC_Fields_Excel_Complete_Reference.md` §3 is enforced as mandatory; every conditional-mandatory rule in §4 triggers correctly based on its stated condition.
- [ ] Filename convention, encoding (UTF-8 no BOM), and pipe-delimiter are checked for `.txt` inputs.
- [ ] On-screen results are filterable by record type and severity, and sortable.
- [ ] The GUI matches the modern themed design in the revised §6 — not plain default Tkinter styling.
- [ ] Downloadable `.txt` report matches the format in §7 and requires no external app beyond Notepad to read cleanly.
- [ ] No CSV/Excel export exists anywhere in the UI.
- [ ] `sample_data.txt` produces exactly the expected single structural error (§9 Phase 5) and zero errors elsewhere.

---

## 11. Open Assumptions / Items Requiring Confirmation — updated (some items resolved, some new)

### Still open (unresolved as of this revision)

1. **`20-052` GSIS ID length discrepancy**: `Consolidated` sheet text says "length = 10 or 11"; other sheets say "length = 11" only. Still unresolved — confirm against the current CIC Submission Manual before finalizing; default to the stricter `=11` if no clarification is available, and log this as a low-confidence rule in code comments.
2. **`BD`, `CN`, `CC`, `CS` record type sample data** in the source workbook's `test` sheet contains only the record-type code with no populated sample values (unlike `ID`/`CI`, which have full worked examples). Field *names* and mandatory-field lists for these types are confirmed via the rulebook (see Complete Reference §3), but there's no worked-example cross-check the way `ID` and `CI` got. Recommend the officer supply a real/representative sample row per missing type during Phase 5 testing.
3. **`CI`'s `Contract Type` field vs. `Transaction Type / Sub-facility` field** use two different domains (confirmed distinct by schema position and separate source tables). `Transaction Type / Sub-facility` is **not treated as mandatory** in `CI`, `CN`, `CC`, or `CS` because the 703-rule rulebook contains no mandatory rule for this field; keep it as a domain-validated optional field until an explicit mandatory rule is found.
4. **`Guarantee Code`, `Company Role`, and `Company Link Reference Date`** mandatory rules were matched to record type by context rather than an exact schema field-name text match — verify directly against the schema during implementation.
5. **`Billed Amount`** appears in the rulebook associated with both `CC` and `CS` contexts, but the schema only has a confirmed exact field under `CS` — treat the `CC` association as unconfirmed until cross-checked.
6. **PSIC, PSOC, Currency, and Country domains** (2,037 / 637 / 178 / 249 entries respectively) are fully populated in `domains_master.json` but were not spot-verified entry-by-entry against original source material — recommend a light sampling check (10–15 entries per list) before treating them as certain.
7. **Rules without automatable field bindings** (structural/relational rules described in prose only) need the manual mapping pass in §9 Phase 2 — expected to be the single largest time investment in the build; results get recorded in `schema/unmapped_rules.json`, not guessed.

### Resolved since the original draft (kept here for traceability — do not re-open without new evidence)

- ~~Domain/lookup table extraction~~ — **done.** `domains_master.json` is complete, including full PSIC/PSOC/Currency/Country lists (see §4.4).
- ~~Mandatory-fields list~~ — **done.** An initial attempt undercounted badly (found via a single header-row color check); the corrected, complete list is in `CIC_Fields_Excel_Complete_Reference.md` §3–§4, derived from a worked example plus the rulebook's explicit mandatory-field rules (see §4.4a).
- ~~`CI`'s and `CN`'s `ContractTypeDomain` extraction~~ — **corrected.** A 3-column source layout (Value / short description / long-form sub-description) had caused an early extraction pass to find only 1 entry each; both are now complete (21 entries for CI, 11 for CN) in `domains_master.json`.
- ~~GUI framework~~ — **changed.** Plain `ttk` replaced with `ttkbootstrap` per the revised §6, for a modern themed look.
