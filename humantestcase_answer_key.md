# humantestcase.txt — Answer Key

Ground-truth reference for cross-checking the validator's output against `humantestcase.txt`.
Each entry below lists the line number, what was done to that record, and the error code(s)
the validator should report. **A blank expected-codes list means the record is a true negative**
— the validator should report ZERO errors for that line.

Codes marked `10-xxx`, `20-xxx`, `30-xxx`, or `unmapped` are cases where the exact CIC error code
couldn't be pinned down from the rulebook text alone (the underlying rule category is correct,
but confirm the precise code against the validator's own rule bindings rather than treating
this placeholder as authoritative).

## Summary

| Category | Count | Meaning |
|---|---|---|
| clean | 1011 | Unmodified real record — must produce zero errors |
| missing_mandatory | 114 | An unconditionally mandatory field left blank |
| formatting | 75 | Whitespace padding, case mismatch, Excel artifacts (trailing .00, leading apostrophe), smart quotes |
| valid_optional_blank | 72 | An optional (non-mandatory) field intentionally left blank — must NOT be flagged |
| domain_violation | 45 | Field value not in its valid code list |
| structural_missing_delim | 35 | A pipe delimiter is missing, shifting all subsequent fields |
| conditional_mandatory | 30 | A CI field left blank when its trigger condition (Contract Phase) makes it mandatory |
| date_format | 26 | Date field in wrong format (ISO instead of DDMMYYYY, or day/month swapped) |
| address_completeness | 20 | Address:Type filled but neither FullAddress nor the address trio is filled |
| age_range | 20 | Date of Birth manipulated so computed age falls outside 18-100 |
| structural_extra_delim | 20 | An extra pipe delimiter was inserted, shifting all subsequent fields |
| numeric_typo | 19 | Letter typed where a digit was expected (O/0 confusion) |
| natural_structural | 17 | Genuine malformed record found in real production data (not synthetic) |
| structural_record_type | 15 | Record Type code is misspelled/wrong |
| contact_missing | 15 | Both Contact 1 and Contact 2 are entirely blank |
| paired_field | 13 | One half of a Type/Number pair filled, the other left blank |
| duplicate_psn | 10 | Provider Subject No duplicated from another record in the file |
| structural_provider_code | 10 | Provider Code inconsistent with the file's actual provider |
| structural_ft_count_mismatch | 1 | Footer's declared record count does not match actual detail record count |

**Total lines (including HD and FT): 1568**

## Line-by-Line Detail

| Line | Type | Category | Expected Code(s) | What was done |
|---|---|---|---|---|
| 1 | HD | clean | *(none — should pass clean)* | Clean header record |
| 2 | ID | numeric_typo | 10-xxx | Field 'Identification 1: Number' has a letter 'O' typed instead of digit '0': '3173O62396' |
| 3 | ID | missing_mandatory | 10-120 | Mandatory field 'Provider Subject No' left blank (simulates encoder skipping a required cell) |
| 4 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 5 | ID | missing_mandatory | unmapped | Mandatory field 'Civil Status' left blank (simulates encoder skipping a required cell) |
| 6 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 7 | CI | conditional_mandatory | 20-090 | Contract Phase is 'AC' so 'Overdue Days' is conditionally mandatory, but it was left blank |
| 8 | ID | valid_optional_blank | *(none — should pass clean)* | Optional field 'Identification 2: Type' intentionally left blank — should NOT be flagged as an error |
| 9 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 10 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 11 | ID | date_format | 10-005 | Field 'Date of Birth' entered as ISO date '1976-02-20' instead of DDMMYYYY '20021976' (common spreadsheet auto-format error) |
| 12 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 13 | ID | address_completeness | 20-139 | Address 2: Address Type is filled but neither FullAddress nor the StreetNo+City+Province trio is filled in |
| 14 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 15 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 16 | ID | structural_missing_delim | 30-010 | Missing delimiter after 'Address 1: FullAddress' (position 32) — merges with next field and shifts every subsequent field left by one |
| 17 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 18 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 19 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 20 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 21 | ID | valid_optional_blank | *(none — should pass clean)* | Optional field 'Identification 3: Type' intentionally left blank — should NOT be flagged as an error |
| 22 | CI | missing_mandatory | 10-023 | Mandatory field 'Contract Type' left blank (simulates encoder skipping a required cell) |
| 23 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 24 | ID | paired_field | 10-069 | 'Identification 1: Type' is filled in but 'Identification 1: Number' was left blank — paired fields must be both empty or both filled |
| 25 | ID | date_format | 10-005 | Field 'Date of Birth' entered as ISO date '1976-11-10' instead of DDMMYYYY '10111976' (common spreadsheet auto-format error) |
| 26 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 27 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 28 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 29 | ID | formatting | 10-xxx | Field 'First Name' has leading/trailing whitespace padding (copy-paste artifact) |
| 30 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 31 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 32 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 33 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 34 | I | structural_record_type | 30-009 | Record Type typo: 'I' instead of 'ID' (fat-fingered or autocorrected) |
| 35 | ID | duplicate_psn | 10-090 | Provider Subject No duplicated to '1190028646', which is already used by another subject in this file |
| 36 | ID | age_range | 20-137 | Date of Birth changed to '22082015' so computed age is out of the 18-100 valid range |
| 37 | ID | missing_mandatory | 20-004 | Mandatory field 'Date of Birth' left blank (simulates encoder skipping a required cell) |
| 38 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 39 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 40 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 41 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 42 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 43 | ID | natural_structural | 30-010 | Naturally-occurring malformed record from source data (124 fields instead of 123) — real human data-entry error, not synthetically injected |
| 44 | ID | valid_optional_blank | *(none — should pass clean)* | Optional field 'Previous Last Name' intentionally left blank — should NOT be flagged as an error |
| 45 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 46 | CI | missing_mandatory | 30-024 | Mandatory field 'Provider Contract No' left blank (simulates encoder skipping a required cell) |
| 47 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 48 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 49 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 50 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 51 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 52 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 53 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 54 | ID | formatting | 10-xxx | Field 'First Name' has leading/trailing whitespace padding (copy-paste artifact) |
| 55 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 56 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 57 | ID | missing_mandatory | 10-109 | Mandatory field 'Subject Reference Date' left blank (simulates encoder skipping a required cell) |
| 58 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 59 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 60 | ID | paired_field | 10-069 | 'ID 1: Type' is filled in but 'ID 1: Number' was left blank — paired fields must be both empty or both filled |
| 61 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 62 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 63 | ID | missing_mandatory | unmapped | Mandatory field 'Identification 1: Type' left blank (simulates encoder skipping a required cell) |
| 64 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 65 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 66 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 67 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 68 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 69 | CI | numeric_typo | 10-xxx | Field 'Financed Amount' has a letter 'O' typed instead of digit '0': '50O000' |
| 70 | CI | date_format | 10-005 | Field 'Contract Start Date' entered as ISO date '2024-07-31' instead of DDMMYYYY '31072024' (common spreadsheet auto-format error) |
| 71 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 72 | CI | domain_violation | 10-xxx | Contract Status entered as 'ACTIVE' (spelled out) instead of a valid domain code |
| 73 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 74 | ID | valid_optional_blank | *(none — should pass clean)* | Optional field 'Spouse First Name' intentionally left blank — should NOT be flagged as an error |
| 75 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 76 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 77 | ID | valid_optional_blank | *(none — should pass clean)* | Optional field 'Previous Last Name' intentionally left blank — should NOT be flagged as an error |
| 78 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 79 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 80 | CI | missing_mandatory | 10-163 | Mandatory field 'Payment Periodicity' left blank (simulates encoder skipping a required cell) |
| 81 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 82 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 83 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 84 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 85 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 86 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 87 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 88 | ID | structural_extra_delim | 30-010 | Extra delimiter inserted before 'ID 1: Issued By' (position 64) — adds a spurious empty field and shifts everything after right by one |
| 89 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 90 | ID | formatting | 10-xxx | Field 'Gender' has leading/trailing whitespace padding (copy-paste artifact) |
| 91 | ID | structural_extra_delim | 30-010 | Extra delimiter inserted before 'Contact 1: Type' (position 77) — adds a spurious empty field and shifts everything after right by one |
| 92 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 93 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 94 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 95 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 96 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 97 | ID | formatting | 10-xxx | Field 'First Name' has leading/trailing whitespace padding (copy-paste artifact) |
| 98 | ID | duplicate_psn | 10-090 | Provider Subject No duplicated to '1190023358', which is already used by another subject in this file |
| 99 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 100 | ID | formatting | 10-xxx | Field 'Gender' value lower-cased ('F' -> 'f'), domain codes are case-sensitive |
| 101 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 102 | ID | contact_missing | 20-104 | Both Contact 1 and Contact 2 Type/Value are blank — at least one Contact:Type must be filled |
| 103 | CI | conditional_mandatory | 20-089 | Contract Phase is 'AC' so 'Last payment amount' is conditionally mandatory, but it was left blank |
| 104 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 105 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 106 | ID | address_completeness | 20-139 | Address 2: Address Type is filled but neither FullAddress nor the StreetNo+City+Province trio is filled in |
| 107 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 108 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 109 | ID | paired_field | 10-069 | 'ID 1: Type' is filled in but 'ID 1: Number' was left blank — paired fields must be both empty or both filled |
| 110 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 111 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 112 | ID | missing_mandatory | 10-120 | Mandatory field 'Provider Subject No' left blank (simulates encoder skipping a required cell) |
| 113 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 114 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 115 | ID | valid_optional_blank | *(none — should pass clean)* | Optional field 'Identification 2: Type' intentionally left blank — should NOT be flagged as an error |
| 116 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 117 | CI | conditional_mandatory | 20-090 | Contract Phase is 'AC' so 'Overdue Days' is conditionally mandatory, but it was left blank |
| 118 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 119 | ID | date_format | 10-005 | Field 'Date of Birth' entered as ISO date '1972-08-17' instead of DDMMYYYY '17081972' (common spreadsheet auto-format error) |
| 120 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 121 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 122 | CI | numeric_typo | 10-xxx | Field 'Financed Amount' has a letter 'O' typed instead of digit '0': '500O000' |
| 123 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 124 | ID | missing_mandatory | 20-002 | Mandatory field 'First Name' left blank (simulates encoder skipping a required cell) |
| 125 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 126 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 127 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 128 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 129 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 130 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 131 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 132 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 133 | ID | valid_optional_blank | *(none — should pass clean)* | Optional field 'Identification 2: Type' intentionally left blank — should NOT be flagged as an error |
| 134 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 135 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 136 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 137 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 138 | CI | date_format | 10-005 | Field 'Contract Start Date' entered as ISO date '2023-11-15' instead of DDMMYYYY '15112023' (common spreadsheet auto-format error) |
| 139 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 140 | ID | formatting | 10-xxx | Field 'Gender' value lower-cased ('F' -> 'f'), domain codes are case-sensitive |
| 141 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 142 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 143 | CI | missing_mandatory | 10-024 | Mandatory field 'Contract Phase' left blank (simulates encoder skipping a required cell) |
| 144 | ID | date_format | 10-005 | Field 'Date of Birth' entered as ISO date '1981-09-28' instead of DDMMYYYY '28091981' (common spreadsheet auto-format error) |
| 145 | ID | formatting | 10-xxx | Field 'First Name' has leading/trailing whitespace padding (copy-paste artifact) |
| 146 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 147 | CI | formatting | 10-xxx | Field 'Financed Amount' has a trailing '.00' from an Excel-formatted numeric cell ('730000.00' instead of '730000') |
| 148 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 149 | ID | structural_extra_delim | 30-010 | Extra delimiter inserted before 'Address 1: FullAddress' (position 32) — adds a spurious empty field and shifts everything after right by one |
| 150 | ID | age_range | 20-137 | Date of Birth changed to '20041920' so computed age is out of the 18-100 valid range |
| 151 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 152 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 153 | ID | contact_missing | 20-104 | Both Contact 1 and Contact 2 Type/Value are blank — at least one Contact:Type must be filled |
| 154 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 155 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 156 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 157 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 158 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 159 | CI | valid_optional_blank | *(none — should pass clean)* | Optional field 'Good Type' intentionally left blank — should NOT be flagged as an error |
| 160 | CI | domain_violation | 10-xxx | Role entered as 'Borrower' (spelled out) instead of domain code 'B' |
| 161 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 162 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 163 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 164 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 165 | ID | valid_optional_blank | *(none — should pass clean)* | Optional field 'Spouse First Name' intentionally left blank — should NOT be flagged as an error |
| 166 | ID | formatting | 10-xxx | Field 'Provider Subject No' has a leading apostrophe left over from Excel 'format as text' trick: "'1190029447" |
| 167 | ID | address_completeness | 20-139 | Address 2: Address Type is filled but neither FullAddress nor the StreetNo+City+Province trio is filled in |
| 168 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 169 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 170 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 171 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 172 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 173 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 174 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 175 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 176 | ID | structural_missing_delim | 30-010 | Missing delimiter after 'Middle Name' (position 8) — merges with next field and shifts every subsequent field left by one |
| 177 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 178 | CI | valid_optional_blank | *(none — should pass clean)* | Optional field 'New/Used Code' intentionally left blank — should NOT be flagged as an error |
| 179 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 180 | CI | numeric_typo | 10-xxx | Field 'Financed Amount' has a letter 'O' typed instead of digit '0': '150O000' |
| 181 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 182 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 183 | ID | formatting | 10-xxx | Field 'Gender' has leading/trailing whitespace padding (copy-paste artifact) |
| 184 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 185 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 186 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 187 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 188 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 189 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 190 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 191 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 192 | CI | valid_optional_blank | *(none — should pass clean)* | Optional field 'Purpose of credit' intentionally left blank — should NOT be flagged as an error |
| 193 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 194 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 195 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 196 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 197 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 198 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 199 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 200 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 201 | ID | formatting | 10-xxx | Field 'Gender' has leading/trailing whitespace padding (copy-paste artifact) |
| 202 | ID | natural_structural | 30-010 | Naturally-occurring malformed record from source data (125 fields instead of 123) — real human data-entry error, not synthetically injected |
| 203 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 204 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 205 | ID | numeric_typo | 10-xxx | Field 'Identification 1: Number' has a letter 'O' typed instead of digit '0': '2890O68880' |
| 206 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 207 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 208 | ID | formatting | 10-xxx | Field 'Gender' has leading/trailing whitespace padding (copy-paste artifact) |
| 209 | ID | formatting | 10-xxx | Field 'Gender' value lower-cased ('F' -> 'f'), domain codes are case-sensitive |
| 210 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 211 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 212 | ID | address_completeness | 20-139 | Address 1: Address Type is filled but neither FullAddress nor the StreetNo+City+Province trio is filled in |
| 213 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 214 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 215 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 216 | ID | structural_extra_delim | 30-010 | Extra delimiter inserted before 'Contact 1: Type' (position 77) — adds a spurious empty field and shifts everything after right by one |
| 217 | ID | missing_mandatory | unmapped | Mandatory field 'Identification 1: Type' left blank (simulates encoder skipping a required cell) |
| 218 | CI | missing_mandatory | 10-163 | Mandatory field 'Payment Periodicity' left blank (simulates encoder skipping a required cell) |
| 219 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 220 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 221 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 222 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 223 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 224 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 225 | ID | valid_optional_blank | *(none — should pass clean)* | Optional field 'Previous Last Name' intentionally left blank — should NOT be flagged as an error |
| 226 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 227 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 228 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 229 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 230 | CI | missing_mandatory | 10-152 | Mandatory field 'Role' left blank (simulates encoder skipping a required cell) |
| 231 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 232 | ID | structural_missing_delim | 30-010 | Missing delimiter after 'ID 1: Issued By' (position 64) — merges with next field and shifts every subsequent field left by one |
| 233 | ID | formatting | 10-xxx | Field 'Provider Subject No' has a leading apostrophe left over from Excel 'format as text' trick: "'1190012938" |
| 234 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 235 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 236 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 237 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 238 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 239 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 240 | CI | conditional_mandatory | 20-089 | Contract Phase is 'AC' so 'Last payment amount' is conditionally mandatory, but it was left blank |
| 241 | ID | structural_extra_delim | 30-010 | Extra delimiter inserted before 'Middle Name' (position 8) — adds a spurious empty field and shifts everything after right by one |
| 242 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 243 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 244 | ID | formatting | 10-xxx | Field 'Gender' has leading/trailing whitespace padding (copy-paste artifact) |
| 245 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 246 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 247 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 248 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 249 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 250 | ID | date_format | 10-005 | Field 'Date of Birth' entered as ISO date '1975-06-01' instead of DDMMYYYY '01061975' (common spreadsheet auto-format error) |
| 251 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 252 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 253 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 254 | ID | date_format | 10-005 | Field 'Date of Birth' entered as ISO date '1985-08-23' instead of DDMMYYYY '23081985' (common spreadsheet auto-format error) |
| 255 | CI | valid_optional_blank | *(none — should pass clean)* | Optional field 'New/Used Code' intentionally left blank — should NOT be flagged as an error |
| 256 | ID | age_range | 20-137 | Date of Birth changed to '10012015' so computed age is out of the 18-100 valid range |
| 257 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 258 | CI | conditional_mandatory | 20-090 | Contract Phase is 'CL' so 'Overdue Days' is conditionally mandatory, but it was left blank |
| 259 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 260 | ID | contact_missing | 20-104 | Both Contact 1 and Contact 2 Type/Value are blank — at least one Contact:Type must be filled |
| 261 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 262 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 263 | ID | numeric_typo | 10-xxx | Field 'Identification 1: Number' has a letter 'O' typed instead of digit '0': '4724O86296' |
| 264 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 265 | CI | date_format | 10-005 | Field 'Contract Start Date' entered as ISO date '2025-04-29' instead of DDMMYYYY '29042025' (common spreadsheet auto-format error) |
| 266 | ID | formatting | 10-xxx | Field 'Gender' has leading/trailing whitespace padding (copy-paste artifact) |
| 267 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 268 | ID | contact_missing | 20-104 | Both Contact 1 and Contact 2 Type/Value are blank — at least one Contact:Type must be filled |
| 269 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 270 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 271 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 272 | ID | formatting | 10-xxx | Field 'Gender' value lower-cased ('F' -> 'f'), domain codes are case-sensitive |
| 273 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 274 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 275 | CI | domain_violation | 10-xxx | Role entered as 'Borrower' (spelled out) instead of domain code 'B' |
| 276 | ID | address_completeness | 20-139 | Address 2: Address Type is filled but neither FullAddress nor the StreetNo+City+Province trio is filled in |
| 277 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 278 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 279 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 280 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 281 | CI | missing_mandatory | 10-030 | Mandatory field 'Installments Number' left blank (simulates encoder skipping a required cell) |
| 282 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 283 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 284 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 285 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 286 | D | structural_record_type | 30-009 | Record Type typo: 'D' instead of 'ID' (fat-fingered or autocorrected) |
| 287 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 288 | ID | structural_missing_delim | 30-010 | Missing delimiter after 'ID 1: Issued By' (position 64) — merges with next field and shifts every subsequent field left by one |
| 289 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 290 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 291 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 292 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 293 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 294 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 295 | ID | duplicate_psn | 10-090 | Provider Subject No duplicated to '1160003723', which is already used by another subject in this file |
| 296 | CI | missing_mandatory | 10-163 | Mandatory field 'Payment Periodicity' left blank (simulates encoder skipping a required cell) |
| 297 | ID | domain_violation | 10-004 | Gender entered as 'MALE' instead of domain code M/F |
| 298 | ID | age_range | 20-137 | Date of Birth changed to '03071920' so computed age is out of the 18-100 valid range |
| 299 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 300 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 301 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 302 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 303 | CI | valid_optional_blank | *(none — should pass clean)* | Optional field 'Good Type' intentionally left blank — should NOT be flagged as an error |
| 304 | CI | valid_optional_blank | *(none — should pass clean)* | Optional field 'Board Resolution flag' intentionally left blank — should NOT be flagged as an error |
| 305 | ID | missing_mandatory | unmapped | Mandatory field 'Middle Name' left blank (simulates encoder skipping a required cell) |
| 306 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 307 | CI | date_format | 10-005 | Field 'Contract Start Date' entered as ISO date '2023-11-23' instead of DDMMYYYY '23112023' (common spreadsheet auto-format error) |
| 308 | ID | missing_mandatory | 10-109 | Mandatory field 'Subject Reference Date' left blank (simulates encoder skipping a required cell) |
| 309 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 310 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 311 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 312 | CI | conditional_mandatory | 10-268 | Contract Phase is 'AC' so 'Monthly Payment Amount' is conditionally mandatory, but it was left blank |
| 313 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 314 | ID | duplicate_psn | 10-090 | Provider Subject No duplicated to '1190015105', which is already used by another subject in this file |
| 315 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 316 | ID | missing_mandatory | unmapped | Mandatory field 'Identification 1: Type' left blank (simulates encoder skipping a required cell) |
| 317 | ID | address_completeness | 20-139 | Address 1: Address Type is filled but neither FullAddress nor the StreetNo+City+Province trio is filled in |
| 318 | ID | valid_optional_blank | *(none — should pass clean)* | Optional field 'Number of Dependents' intentionally left blank — should NOT be flagged as an error |
| 319 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 320 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 321 | ID | formatting | 10-xxx | Field 'Gender' has leading/trailing whitespace padding (copy-paste artifact) |
| 322 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 323 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 324 | CI | missing_mandatory | 10-161 | Mandatory field 'Financed Amount' left blank (simulates encoder skipping a required cell) |
| 325 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 326 | CI | conditional_mandatory | 10-268 | Contract Phase is 'AC' so 'Monthly Payment Amount' is conditionally mandatory, but it was left blank |
| 327 | CI | missing_mandatory | 10-023 | Mandatory field 'Contract Type' left blank (simulates encoder skipping a required cell) |
| 328 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 329 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 330 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 331 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 332 | CI | conditional_mandatory | 20-090 | Contract Phase is 'CA' so 'Overdue Days' is conditionally mandatory, but it was left blank |
| 333 | CI | structural_missing_delim | 30-010 | Missing delimiter after 'Payment Method' (position 24) — merges with next field and shifts every subsequent field left by one |
| 334 | ID | valid_optional_blank | *(none — should pass clean)* | Optional field 'Number of Dependents' intentionally left blank — should NOT be flagged as an error |
| 335 | ID | domain_violation | 10-004 | Gender entered as 'Male' instead of domain code M/F |
| 336 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 337 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 338 | ID | missing_mandatory | 20-004 | Mandatory field 'Date of Birth' left blank (simulates encoder skipping a required cell) |
| 339 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 340 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 341 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 342 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 343 | CI | missing_mandatory | 10-027 | Mandatory field 'Currency' left blank (simulates encoder skipping a required cell) |
| 344 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 345 | CI | valid_optional_blank | *(none — should pass clean)* | Optional field 'Board Resolution flag' intentionally left blank — should NOT be flagged as an error |
| 346 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 347 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 348 | CI | valid_optional_blank | *(none — should pass clean)* | Optional field 'Board Resolution flag' intentionally left blank — should NOT be flagged as an error |
| 349 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 350 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 351 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 352 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 353 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 354 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 355 | ID | date_format | 10-005 | Field 'Date of Birth' day/month swapped: '02081983' instead of '08021983' (encoder used MM/DD habit) |
| 356 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 357 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 358 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 359 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 360 | ID | missing_mandatory | unmapped | Mandatory field 'Title' left blank (simulates encoder skipping a required cell) |
| 361 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 362 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 363 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 364 | CI | formatting | 10-xxx | Field 'Financed Amount' has a trailing '.00' from an Excel-formatted numeric cell ('2500000.00' instead of '2500000') |
| 365 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 366 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 367 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 368 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 369 | ID | formatting | 10-xxx | Field 'Gender' has leading/trailing whitespace padding (copy-paste artifact) |
| 370 | CI | structural_missing_delim | 30-010 | Missing delimiter after 'Good Type' (position 35) — merges with next field and shifts every subsequent field left by one |
| 371 | ID | valid_optional_blank | *(none — should pass clean)* | Optional field 'Father First Name' intentionally left blank — should NOT be flagged as an error |
| 372 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 373 | ID | missing_mandatory | 20-003 | Mandatory field 'Last Name' left blank (simulates encoder skipping a required cell) |
| 374 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 375 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 376 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 377 | ID | formatting | 10-xxx | Field 'Gender' value lower-cased ('F' -> 'f'), domain codes are case-sensitive |
| 378 | ID | domain_violation | 10-004 | Gender entered as 'Female' instead of domain code M/F |
| 379 | ID | domain_violation | 10-004 | Gender entered as 'MALE' instead of domain code M/F |
| 380 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 381 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 382 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 383 | ID  | structural_record_type | 30-009 | Record Type typo: 'ID ' instead of 'ID' (fat-fingered or autocorrected) |
| 384 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 385 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 386 | CI | missing_mandatory | 10-152 | Mandatory field 'Role' left blank (simulates encoder skipping a required cell) |
| 387 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 388 | ID | natural_structural | 30-010 | Naturally-occurring malformed record from source data (125 fields instead of 123) — real human data-entry error, not synthetically injected |
| 389 | CI | date_format | 10-005 | Field 'Contract Start Date' entered as ISO date '2025-01-24' instead of DDMMYYYY '24012025' (common spreadsheet auto-format error) |
| 390 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 391 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 392 | ID | missing_mandatory | unmapped | Mandatory field 'Middle Name' left blank (simulates encoder skipping a required cell) |
| 393 | CI | structural_missing_delim | 30-010 | Missing delimiter after 'Payment Method' (position 24) — merges with next field and shifts every subsequent field left by one |
| 394 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 395 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 396 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 397 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 398 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 399 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 400 | ID | formatting | 10-xxx | Last Name contains a Word-autocorrected curly apostrophe (’) instead of a straight one |
| 401 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 402 | ID | missing_mandatory | unmapped | Mandatory field 'Mother’s Maiden FULL NAME' left blank (simulates encoder skipping a required cell) |
| 403 | CI | missing_mandatory | 10-023 | Mandatory field 'Contract Type' left blank (simulates encoder skipping a required cell) |
| 404 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 405 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 406 | CI | missing_mandatory | 10-024 | Mandatory field 'Contract Phase' left blank (simulates encoder skipping a required cell) |
| 407 | ID | formatting | 10-xxx | Field 'First Name' has leading/trailing whitespace padding (copy-paste artifact) |
| 408 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 409 | ID | structural_missing_delim | 30-010 | Missing delimiter after 'ID 1: Issued By' (position 64) — merges with next field and shifts every subsequent field left by one |
| 410 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 411 | ID  | structural_record_type | 30-009 | Record Type typo: 'ID ' instead of 'ID' (fat-fingered or autocorrected) |
| 412 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 413 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 414 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 415 | ID | formatting | 10-xxx | Field 'First Name' has leading/trailing whitespace padding (copy-paste artifact) |
| 416 | ID | structural_missing_delim | 30-010 | Missing delimiter after 'ID 1: Issued By' (position 64) — merges with next field and shifts every subsequent field left by one |
| 417 | CI | missing_mandatory | 10-163 | Mandatory field 'Payment Periodicity' left blank (simulates encoder skipping a required cell) |
| 418 | CI | missing_mandatory | 10-027 | Mandatory field 'Currency' left blank (simulates encoder skipping a required cell) |
| 419 | ID | valid_optional_blank | *(none — should pass clean)* | Optional field 'Father First Name' intentionally left blank — should NOT be flagged as an error |
| 420 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 421 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 422 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 423 | ID | address_completeness | 20-139 | Address 2: Address Type is filled but neither FullAddress nor the StreetNo+City+Province trio is filled in |
| 424 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 425 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 426 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 427 | ID | structural_extra_delim | 30-010 | Extra delimiter inserted before 'Address 1: FullAddress' (position 32) — adds a spurious empty field and shifts everything after right by one |
| 428 | CI | numeric_typo | 10-xxx | Field 'Financed Amount' has a letter 'O' typed instead of digit '0': '134O6400' |
| 429 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 430 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 431 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 432 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 433 | ID | address_completeness | 20-139 | Address 2: Address Type is filled but neither FullAddress nor the StreetNo+City+Province trio is filled in |
| 434 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 435 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 436 | ID | contact_missing | 20-104 | Both Contact 1 and Contact 2 Type/Value are blank — at least one Contact:Type must be filled |
| 437 | ID | address_completeness | 20-139 | Address 1: Address Type is filled but neither FullAddress nor the StreetNo+City+Province trio is filled in |
| 438 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 439 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 440 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 441 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 442 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 443 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 444 | ID | numeric_typo | 10-xxx | Field 'Identification 1: Number' has a letter 'O' typed instead of digit '0': '7047O73123' |
| 445 | ID  | structural_record_type | 30-009 | Record Type typo: 'ID ' instead of 'ID' (fat-fingered or autocorrected) |
| 446 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 447 | ID | address_completeness | 20-139 | Address 1: Address Type is filled but neither FullAddress nor the StreetNo+City+Province trio is filled in |
| 448 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 449 | CI | domain_violation | 10-xxx | Contract Status entered as 'ACTIVE' (spelled out) instead of a valid domain code |
| 450 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 451 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 452 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 453 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 454 | ID | missing_mandatory | 20-004 | Mandatory field 'Date of Birth' left blank (simulates encoder skipping a required cell) |
| 455 | ID | age_range | 20-137 | Date of Birth changed to '20111920' so computed age is out of the 18-100 valid range |
| 456 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 457 | CI | missing_mandatory | 30-024 | Mandatory field 'Provider Contract No' left blank (simulates encoder skipping a required cell) |
| 458 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 459 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 460 | ID | formatting | 10-xxx | Field 'First Name' has leading/trailing whitespace padding (copy-paste artifact) |
| 461 | CI | conditional_mandatory | 10-268 | Contract Phase is 'AC' so 'Monthly Payment Amount' is conditionally mandatory, but it was left blank |
| 462 | CI | formatting | 10-xxx | Field 'Financed Amount' has a trailing '.00' from an Excel-formatted numeric cell ('800000.00' instead of '800000') |
| 463 | ID | duplicate_psn | 10-090 | Provider Subject No duplicated to '1190030310', which is already used by another subject in this file |
| 464 | ID | valid_optional_blank | *(none — should pass clean)* | Optional field 'Identification 3: Type' intentionally left blank — should NOT be flagged as an error |
| 465 | ID | missing_mandatory | 20-002 | Mandatory field 'First Name' left blank (simulates encoder skipping a required cell) |
| 466 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 467 | ID | formatting | 10-xxx | Field 'Gender' value lower-cased ('F' -> 'f'), domain codes are case-sensitive |
| 468 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 469 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 470 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 471 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 472 | CI | valid_optional_blank | *(none — should pass clean)* | Optional field 'Good Type' intentionally left blank — should NOT be flagged as an error |
| 473 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 474 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 475 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 476 | ID | missing_mandatory | 20-002 | Mandatory field 'First Name' left blank (simulates encoder skipping a required cell) |
| 477 | CI | domain_violation | 10-xxx | Role entered as 'Borrower' (spelled out) instead of domain code 'B' |
| 478 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 479 | ID | domain_violation | 10-xxx | Civil Status set to '9', which is not in the valid domain {1,2,3,4} |
| 480 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 481 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 482 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 483 | ID | numeric_typo | 10-xxx | Field 'Identification 1: Number' has a letter 'O' typed instead of digit '0': '4658O10551' |
| 484 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 485 | ID | date_format | 10-005 | Field 'Date of Birth' entered as ISO date '1979-02-04' instead of DDMMYYYY '04021979' (common spreadsheet auto-format error) |
| 486 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 487 | CI | conditional_mandatory | 20-089 | Contract Phase is 'AC' so 'Last payment amount' is conditionally mandatory, but it was left blank |
| 488 | ID | missing_mandatory | 10-109 | Mandatory field 'Subject Reference Date' left blank (simulates encoder skipping a required cell) |
| 489 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 490 | ID | natural_structural | 30-010 | Naturally-occurring malformed record from source data (121 fields instead of 123) — real human data-entry error, not synthetically injected |
| 491 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 492 | ID | missing_mandatory | 20-004 | Mandatory field 'Date of Birth' left blank (simulates encoder skipping a required cell) |
| 493 | ID | paired_field | 10-069 | 'ID 1: Type' is filled in but 'ID 1: Number' was left blank — paired fields must be both empty or both filled |
| 494 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 495 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 496 | ID | valid_optional_blank | *(none — should pass clean)* | Optional field 'Identification 3: Type' intentionally left blank — should NOT be flagged as an error |
| 497 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 498 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 499 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 500 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 501 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 502 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 503 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 504 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 505 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 506 | CI | date_format | 10-005 | Field 'Contract Start Date' entered as ISO date '2022-07-12' instead of DDMMYYYY '12072022' (common spreadsheet auto-format error) |
| 507 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 508 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 509 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 510 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 511 | ID | missing_mandatory | unmapped | Mandatory field 'Middle Name' left blank (simulates encoder skipping a required cell) |
| 512 | ID | missing_mandatory | 20-004 | Mandatory field 'Date of Birth' left blank (simulates encoder skipping a required cell) |
| 513 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 514 | CI | valid_optional_blank | *(none — should pass clean)* | Optional field 'Purpose of credit' intentionally left blank — should NOT be flagged as an error |
| 515 | ID | valid_optional_blank | *(none — should pass clean)* | Optional field 'Spouse First Name' intentionally left blank — should NOT be flagged as an error |
| 516 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 517 | ID | structural_missing_delim | 30-010 | Missing delimiter after 'Contact 1: Type' (position 77) — merges with next field and shifts every subsequent field left by one |
| 518 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 519 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 520 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 521 | ID | missing_mandatory | 20-004 | Mandatory field 'Date of Birth' left blank (simulates encoder skipping a required cell) |
| 522 | CI | missing_mandatory | 10-163 | Mandatory field 'Payment Periodicity' left blank (simulates encoder skipping a required cell) |
| 523 | CI | valid_optional_blank | *(none — should pass clean)* | Optional field 'Purpose of credit' intentionally left blank — should NOT be flagged as an error |
| 524 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 525 | I | structural_record_type | 30-009 | Record Type typo: 'I' instead of 'ID' (fat-fingered or autocorrected) |
| 526 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 527 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 528 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 529 | ID | address_completeness | 20-139 | Address 1: Address Type is filled but neither FullAddress nor the StreetNo+City+Province trio is filled in |
| 530 | ID | domain_violation | 10-xxx | Civil Status set to '9', which is not in the valid domain {1,2,3,4} |
| 531 | CI | domain_violation | 10-xxx | Role entered as 'Borrower' (spelled out) instead of domain code 'B' |
| 532 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 533 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 534 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 535 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 536 | ID | paired_field | 10-069 | 'Identification 1: Type' is filled in but 'Identification 1: Number' was left blank — paired fields must be both empty or both filled |
| 537 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 538 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 539 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 540 | ID | structural_provider_code | 30-003 | Provider Code changed to 'RB001900' — inconsistent with the file's actual submitting provider 'RB001800' |
| 541 | ID | formatting | 10-xxx | Last Name contains a Word-autocorrected curly apostrophe (’) instead of a straight one |
| 542 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 543 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 544 | ID | valid_optional_blank | *(none — should pass clean)* | Optional field 'Spouse First Name' intentionally left blank — should NOT be flagged as an error |
| 545 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 546 | ID | formatting | 10-xxx | Field 'Provider Subject No' has a leading apostrophe left over from Excel 'format as text' trick: "'1190028845" |
| 547 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 548 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 549 | ID | contact_missing | 20-104 | Both Contact 1 and Contact 2 Type/Value are blank — at least one Contact:Type must be filled |
| 550 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 551 | ID | domain_violation | 10-004 | Gender entered as 'm' instead of domain code M/F |
| 552 | CI | domain_violation | 10-xxx | Contract Status entered as 'ACTIVE' (spelled out) instead of a valid domain code |
| 553 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 554 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 555 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 556 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 557 | ID | domain_violation | 10-004 | Gender entered as 'MALE' instead of domain code M/F |
| 558 | CI | conditional_mandatory | 20-090 | Contract Phase is 'AC' so 'Overdue Days' is conditionally mandatory, but it was left blank |
| 559 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 560 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 561 | ID | missing_mandatory | unmapped | Mandatory field 'Title' left blank (simulates encoder skipping a required cell) |
| 562 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 563 | ID | structural_extra_delim | 30-010 | Extra delimiter inserted before 'Address 1: FullAddress' (position 32) — adds a spurious empty field and shifts everything after right by one |
| 564 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 565 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 566 | CI | missing_mandatory | 10-161 | Mandatory field 'Financed Amount' left blank (simulates encoder skipping a required cell) |
| 567 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 568 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 569 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 570 | I | structural_record_type | 30-009 | Record Type typo: 'I' instead of 'ID' (fat-fingered or autocorrected) |
| 571 | ID | paired_field | 10-069 | 'Identification 1: Type' is filled in but 'Identification 1: Number' was left blank — paired fields must be both empty or both filled |
| 572 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 573 | ID | structural_missing_delim | 30-010 | Missing delimiter after 'Middle Name' (position 8) — merges with next field and shifts every subsequent field left by one |
| 574 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 575 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 576 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 577 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 578 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 579 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 580 | CI | conditional_mandatory | 10-268 | Contract Phase is 'AC' so 'Monthly Payment Amount' is conditionally mandatory, but it was left blank |
| 581 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 582 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 583 | ID | missing_mandatory | 20-003 | Mandatory field 'Last Name' left blank (simulates encoder skipping a required cell) |
| 584 | ID | formatting | 10-xxx | Last Name contains a Word-autocorrected curly apostrophe (’) instead of a straight one |
| 585 | ID | valid_optional_blank | *(none — should pass clean)* | Optional field 'Previous Last Name' intentionally left blank — should NOT be flagged as an error |
| 586 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 587 | I | structural_record_type | 30-009 | Record Type typo: 'I' instead of 'ID' (fat-fingered or autocorrected) |
| 588 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 589 | CI | numeric_typo | 10-xxx | Field 'Financed Amount' has a letter 'O' typed instead of digit '0': '135O0000' |
| 590 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 591 | ID | duplicate_psn | 10-090 | Provider Subject No duplicated to '1190022717', which is already used by another subject in this file |
| 592 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 593 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 594 | CI | formatting | 10-xxx | Field 'Financed Amount' has a trailing '.00' from an Excel-formatted numeric cell ('758400.00' instead of '758400') |
| 595 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 596 | CI | valid_optional_blank | *(none — should pass clean)* | Optional field 'New/Used Code' intentionally left blank — should NOT be flagged as an error |
| 597 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 598 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 599 | ID | formatting | 10-xxx | Field 'Provider Subject No' has a leading apostrophe left over from Excel 'format as text' trick: "'1190026791" |
| 600 | ID | formatting | 10-xxx | Field 'Provider Subject No' has a leading apostrophe left over from Excel 'format as text' trick: "'1190023281" |
| 601 | CI | valid_optional_blank | *(none — should pass clean)* | Optional field 'Good Type' intentionally left blank — should NOT be flagged as an error |
| 602 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 603 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 604 | CI | missing_mandatory | 30-024 | Mandatory field 'Provider Contract No' left blank (simulates encoder skipping a required cell) |
| 605 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 606 | ID | address_completeness | 20-139 | Address 1: Address Type is filled but neither FullAddress nor the StreetNo+City+Province trio is filled in |
| 607 | ID | domain_violation | 10-xxx | Civil Status set to '9', which is not in the valid domain {1,2,3,4} |
| 608 | ID | missing_mandatory | unmapped | Mandatory field 'Civil Status' left blank (simulates encoder skipping a required cell) |
| 609 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 610 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 611 | CI | domain_violation | 10-xxx | Contract Status entered as 'ACTIVE' (spelled out) instead of a valid domain code |
| 612 | CI | structural_missing_delim | 30-010 | Missing delimiter after 'Good Type' (position 35) — merges with next field and shifts every subsequent field left by one |
| 613 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 614 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 615 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 616 | I | structural_record_type | 30-009 | Record Type typo: 'I' instead of 'ID' (fat-fingered or autocorrected) |
| 617 | ID | valid_optional_blank | *(none — should pass clean)* | Optional field 'Identification 3: Type' intentionally left blank — should NOT be flagged as an error |
| 618 | ID | domain_violation | 10-004 | Gender entered as 'MALE' instead of domain code M/F |
| 619 | CI | formatting | 10-xxx | Field 'Financed Amount' has a trailing '.00' from an Excel-formatted numeric cell ('1500000.00' instead of '1500000') |
| 620 | ID | missing_mandatory | 20-001 | Mandatory field 'Gender' left blank (simulates encoder skipping a required cell) |
| 621 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 622 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 623 | ID | missing_mandatory | unmapped | Mandatory field 'Identification 1: Type' left blank (simulates encoder skipping a required cell) |
| 624 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 625 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 626 | CI | valid_optional_blank | *(none — should pass clean)* | Optional field 'Purpose of credit' intentionally left blank — should NOT be flagged as an error |
| 627 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 628 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 629 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 630 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 631 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 632 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 633 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 634 | CI | formatting | 10-xxx | Field 'Financed Amount' has a trailing '.00' from an Excel-formatted numeric cell ('500000.00' instead of '500000') |
| 635 | CI | date_format | 10-005 | Field 'Contract Start Date' entered as ISO date '2024-06-13' instead of DDMMYYYY '13062024' (common spreadsheet auto-format error) |
| 636 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 637 | ID | structural_extra_delim | 30-010 | Extra delimiter inserted before 'Address 1: FullAddress' (position 32) — adds a spurious empty field and shifts everything after right by one |
| 638 | ID | natural_structural | 30-010 | Naturally-occurring malformed record from source data (124 fields instead of 123) — real human data-entry error, not synthetically injected |
| 639 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 640 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 641 | ID | valid_optional_blank | *(none — should pass clean)* | Optional field 'Number of Dependents' intentionally left blank — should NOT be flagged as an error |
| 642 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 643 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 644 | ID | structural_missing_delim | 30-010 | Missing delimiter after 'Contact 1: Type' (position 77) — merges with next field and shifts every subsequent field left by one |
| 645 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 646 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 647 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 648 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 649 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 650 | ID | address_completeness | 20-139 | Address 1: Address Type is filled but neither FullAddress nor the StreetNo+City+Province trio is filled in |
| 651 | ID | domain_violation | 10-004 | Gender entered as 'f' instead of domain code M/F |
| 652 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 653 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 654 | ID | formatting | 10-xxx | Field 'Gender' has leading/trailing whitespace padding (copy-paste artifact) |
| 655 | ID | address_completeness | 20-139 | Address 2: Address Type is filled but neither FullAddress nor the StreetNo+City+Province trio is filled in |
| 656 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 657 | ID | structural_extra_delim | 30-010 | Extra delimiter inserted before 'ID 1: Issued By' (position 64) — adds a spurious empty field and shifts everything after right by one |
| 658 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 659 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 660 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 661 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 662 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 663 | ID | age_range | 20-137 | Date of Birth changed to '17071920' so computed age is out of the 18-100 valid range |
| 664 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 665 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 666 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 667 | ID | structural_extra_delim | 30-010 | Extra delimiter inserted before 'Middle Name' (position 8) — adds a spurious empty field and shifts everything after right by one |
| 668 | ID | age_range | 20-137 | Date of Birth changed to '13111920' so computed age is out of the 18-100 valid range |
| 669 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 670 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 671 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 672 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 673 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 674 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 675 | CI | formatting | 10-xxx | Field 'Financed Amount' has a trailing '.00' from an Excel-formatted numeric cell ('35000.00' instead of '35000') |
| 676 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 677 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 678 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 679 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 680 | CI | missing_mandatory | 10-030 | Mandatory field 'Installments Number' left blank (simulates encoder skipping a required cell) |
| 681 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 682 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 683 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 684 | ID | missing_mandatory | unmapped | Mandatory field 'Identification 1: Type' left blank (simulates encoder skipping a required cell) |
| 685 | ID | formatting | 10-xxx | Field 'Provider Subject No' has a leading apostrophe left over from Excel 'format as text' trick: "'1190025196" |
| 686 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 687 | ID | contact_missing | 20-104 | Both Contact 1 and Contact 2 Type/Value are blank — at least one Contact:Type must be filled |
| 688 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 689 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 690 | CI | structural_missing_delim | 30-010 | Missing delimiter after 'Good Type' (position 35) — merges with next field and shifts every subsequent field left by one |
| 691 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 692 | ID | formatting | 10-xxx | Last Name contains a Word-autocorrected curly apostrophe (’) instead of a straight one |
| 693 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 694 | ID | domain_violation | 10-xxx | Civil Status set to '9', which is not in the valid domain {1,2,3,4} |
| 695 | ID | missing_mandatory | 20-003 | Mandatory field 'Last Name' left blank (simulates encoder skipping a required cell) |
| 696 | ID | paired_field | 10-069 | 'ID 1: Type' is filled in but 'ID 1: Number' was left blank — paired fields must be both empty or both filled |
| 697 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 698 | ID | age_range | 20-137 | Date of Birth changed to '09122015' so computed age is out of the 18-100 valid range |
| 699 | ID | structural_missing_delim | 30-010 | Missing delimiter after 'Middle Name' (position 8) — merges with next field and shifts every subsequent field left by one |
| 700 | CI | formatting | 10-xxx | Field 'Financed Amount' has a trailing '.00' from an Excel-formatted numeric cell ('1150400.00' instead of '1150400') |
| 701 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 702 | ID | missing_mandatory | 20-003 | Mandatory field 'Last Name' left blank (simulates encoder skipping a required cell) |
| 703 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 704 | CI | conditional_mandatory | 10-268 | Contract Phase is 'AC' so 'Monthly Payment Amount' is conditionally mandatory, but it was left blank |
| 705 | ID | contact_missing | 20-104 | Both Contact 1 and Contact 2 Type/Value are blank — at least one Contact:Type must be filled |
| 706 | CI | missing_mandatory | 10-161 | Mandatory field 'Financed Amount' left blank (simulates encoder skipping a required cell) |
| 707 | ID | missing_mandatory | 20-001 | Mandatory field 'Gender' left blank (simulates encoder skipping a required cell) |
| 708 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 709 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 710 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 711 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 712 | ID | duplicate_psn | 10-090 | Provider Subject No duplicated to '1190030011', which is already used by another subject in this file |
| 713 | CI | formatting | 10-xxx | Field 'Financed Amount' has a trailing '.00' from an Excel-formatted numeric cell ('150000.00' instead of '150000') |
| 714 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 715 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 716 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 717 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 718 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 719 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 720 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 721 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 722 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 723 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 724 | CI | conditional_mandatory | 20-090 | Contract Phase is 'AC' so 'Overdue Days' is conditionally mandatory, but it was left blank |
| 725 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 726 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 727 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 728 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 729 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 730 | ID | address_completeness | 20-139 | Address 1: Address Type is filled but neither FullAddress nor the StreetNo+City+Province trio is filled in |
| 731 | CI | formatting | 10-xxx | Field 'Financed Amount' has a trailing '.00' from an Excel-formatted numeric cell ('500000.00' instead of '500000') |
| 732 | ID | valid_optional_blank | *(none — should pass clean)* | Optional field 'Nickname' intentionally left blank — should NOT be flagged as an error |
| 733 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 734 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 735 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 736 | ID | structural_missing_delim | 30-010 | Missing delimiter after 'Middle Name' (position 8) — merges with next field and shifts every subsequent field left by one |
| 737 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 738 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 739 | CI | domain_violation | 10-xxx | Contract Status entered as 'ACTIVE' (spelled out) instead of a valid domain code |
| 740 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 741 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 742 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 743 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 744 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 745 | ID | formatting | 10-xxx | Field 'Gender' value lower-cased ('M' -> 'm'), domain codes are case-sensitive |
| 746 | ID | missing_mandatory | 10-120 | Mandatory field 'Provider Subject No' left blank (simulates encoder skipping a required cell) |
| 747 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 748 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 749 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 750 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 751 | ID | date_format | 10-005 | Field 'Date of Birth' entered as ISO date '1975-01-27' instead of DDMMYYYY '27011975' (common spreadsheet auto-format error) |
| 752 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 753 | ID | age_range | 20-137 | Date of Birth changed to '04031920' so computed age is out of the 18-100 valid range |
| 754 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 755 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 756 | ID | age_range | 20-137 | Date of Birth changed to '16102015' so computed age is out of the 18-100 valid range |
| 757 | ID | valid_optional_blank | *(none — should pass clean)* | Optional field 'Nickname' intentionally left blank — should NOT be flagged as an error |
| 758 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 759 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 760 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 761 | ID | valid_optional_blank | *(none — should pass clean)* | Optional field 'Nickname' intentionally left blank — should NOT be flagged as an error |
| 762 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 763 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 764 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 765 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 766 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 767 | ID | contact_missing | 20-104 | Both Contact 1 and Contact 2 Type/Value are blank — at least one Contact:Type must be filled |
| 768 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 769 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 770 | ID | contact_missing | 20-104 | Both Contact 1 and Contact 2 Type/Value are blank — at least one Contact:Type must be filled |
| 771 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 772 | CI | numeric_typo | 10-xxx | Field 'Financed Amount' has a letter 'O' typed instead of digit '0': '400O000' |
| 773 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 774 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 775 | ID | missing_mandatory | unmapped | Mandatory field 'Middle Name' left blank (simulates encoder skipping a required cell) |
| 776 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 777 | ID | age_range | 20-137 | Date of Birth changed to '01112015' so computed age is out of the 18-100 valid range |
| 778 | ID | address_completeness | 20-139 | Address 2: Address Type is filled but neither FullAddress nor the StreetNo+City+Province trio is filled in |
| 779 | ID | valid_optional_blank | *(none — should pass clean)* | Optional field 'Father First Name' intentionally left blank — should NOT be flagged as an error |
| 780 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 781 | ID | age_range | 20-137 | Date of Birth changed to '09012015' so computed age is out of the 18-100 valid range |
| 782 | CI | conditional_mandatory | 20-089 | Contract Phase is 'AC' so 'Last payment amount' is conditionally mandatory, but it was left blank |
| 783 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 784 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 785 | ID | domain_violation | 10-004 | Gender entered as 'MALE' instead of domain code M/F |
| 786 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 787 | ID | domain_violation | 10-xxx | Civil Status set to '9', which is not in the valid domain {1,2,3,4} |
| 788 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 789 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 790 | ID | natural_structural | 30-010 | Naturally-occurring malformed record from source data (124 fields instead of 123) — real human data-entry error, not synthetically injected |
| 791 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 792 | CI | structural_missing_delim | 30-010 | Missing delimiter after 'Contract Status' (position 9) — merges with next field and shifts every subsequent field left by one |
| 793 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 794 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 795 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 796 | ID | missing_mandatory | 20-001 | Mandatory field 'Gender' left blank (simulates encoder skipping a required cell) |
| 797 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 798 | CI | missing_mandatory | 10-161 | Mandatory field 'Financed Amount' left blank (simulates encoder skipping a required cell) |
| 799 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 800 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 801 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 802 | ID | missing_mandatory | unmapped | Mandatory field 'Middle Name' left blank (simulates encoder skipping a required cell) |
| 803 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 804 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 805 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 806 | ID | structural_missing_delim | 30-010 | Missing delimiter after 'Address 1: FullAddress' (position 32) — merges with next field and shifts every subsequent field left by one |
| 807 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 808 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 809 | ID | valid_optional_blank | *(none — should pass clean)* | Optional field 'Car/s Owned' intentionally left blank — should NOT be flagged as an error |
| 810 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 811 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 812 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 813 | ID | valid_optional_blank | *(none — should pass clean)* | Optional field 'Previous Last Name' intentionally left blank — should NOT be flagged as an error |
| 814 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 815 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 816 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 817 | ID | structural_missing_delim | 30-010 | Missing delimiter after 'Address 1: FullAddress' (position 32) — merges with next field and shifts every subsequent field left by one |
| 818 | ID | structural_extra_delim | 30-010 | Extra delimiter inserted before 'Middle Name' (position 8) — adds a spurious empty field and shifts everything after right by one |
| 819 | ID | paired_field | 10-069 | 'ID 1: Type' is filled in but 'ID 1: Number' was left blank — paired fields must be both empty or both filled |
| 820 | ID | structural_extra_delim | 30-010 | Extra delimiter inserted before 'Address 1: FullAddress' (position 32) — adds a spurious empty field and shifts everything after right by one |
| 821 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 822 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 823 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 824 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 825 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 826 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 827 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 828 | ID | structural_provider_code | 30-003 | Provider Code changed to 'RB001900' — inconsistent with the file's actual submitting provider 'RB001800' |
| 829 | ID | missing_mandatory | unmapped | Mandatory field 'Civil Status' left blank (simulates encoder skipping a required cell) |
| 830 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 831 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 832 | ID | date_format | 10-005 | Field 'Date of Birth' entered as ISO date '1992-06-05' instead of DDMMYYYY '05061992' (common spreadsheet auto-format error) |
| 833 | ID | valid_optional_blank | *(none — should pass clean)* | Optional field 'Previous Last Name' intentionally left blank — should NOT be flagged as an error |
| 834 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 835 | ID | structural_extra_delim | 30-010 | Extra delimiter inserted before 'ID 1: Issued By' (position 64) — adds a spurious empty field and shifts everything after right by one |
| 836 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 837 | ID | natural_structural | 30-010 | Naturally-occurring malformed record from source data (122 fields instead of 123) — real human data-entry error, not synthetically injected |
| 838 | CI | valid_optional_blank | *(none — should pass clean)* | Optional field 'Purpose of credit' intentionally left blank — should NOT be flagged as an error |
| 839 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 840 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 841 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 842 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 843 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 844 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 845 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 846 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 847 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 848 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 849 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 850 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 851 | CI | missing_mandatory | 10-024 | Mandatory field 'Contract Phase' left blank (simulates encoder skipping a required cell) |
| 852 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 853 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 854 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 855 | ID | contact_missing | 20-104 | Both Contact 1 and Contact 2 Type/Value are blank — at least one Contact:Type must be filled |
| 856 | ID | structural_missing_delim | 30-010 | Missing delimiter after 'Address 1: FullAddress' (position 32) — merges with next field and shifts every subsequent field left by one |
| 857 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 858 | ID | date_format | 10-005 | Field 'Date of Birth' entered as ISO date '1993-02-04' instead of DDMMYYYY '04021993' (common spreadsheet auto-format error) |
| 859 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 860 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 861 | ID | paired_field | 10-069 | 'ID 1: Type' is filled in but 'ID 1: Number' was left blank — paired fields must be both empty or both filled |
| 862 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 863 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 864 | ID | missing_mandatory | unmapped | Mandatory field 'Mother’s Maiden FULL NAME' left blank (simulates encoder skipping a required cell) |
| 865 | ID | structural_extra_delim | 30-010 | Extra delimiter inserted before 'Contact 1: Type' (position 77) — adds a spurious empty field and shifts everything after right by one |
| 866 | ID | structural_provider_code | 30-003 | Provider Code changed to 'RB001900' — inconsistent with the file's actual submitting provider 'RB001800' |
| 867 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 868 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 869 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 870 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 871 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 872 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 873 | ID | valid_optional_blank | *(none — should pass clean)* | Optional field 'Number of Dependents' intentionally left blank — should NOT be flagged as an error |
| 874 | ID | date_format | 10-005 | Field 'Date of Birth' entered as ISO date '1958-04-24' instead of DDMMYYYY '24041958' (common spreadsheet auto-format error) |
| 875 | ID | formatting | 10-xxx | Field 'First Name' has leading/trailing whitespace padding (copy-paste artifact) |
| 876 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 877 | XX | structural_record_type | 30-009 | Record Type typo: 'XX' instead of 'ID' (fat-fingered or autocorrected) |
| 878 | I | structural_record_type | 30-009 | Record Type typo: 'I' instead of 'ID' (fat-fingered or autocorrected) |
| 879 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 880 | ID | missing_mandatory | unmapped | Mandatory field 'Civil Status' left blank (simulates encoder skipping a required cell) |
| 881 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 882 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 883 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 884 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 885 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 886 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 887 | CI | structural_missing_delim | 30-010 | Missing delimiter after 'Payment Method' (position 24) — merges with next field and shifts every subsequent field left by one |
| 888 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 889 | ID | valid_optional_blank | *(none — should pass clean)* | Optional field 'Identification 2: Type' intentionally left blank — should NOT be flagged as an error |
| 890 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 891 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 892 | ID | missing_mandatory | 20-002 | Mandatory field 'First Name' left blank (simulates encoder skipping a required cell) |
| 893 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 894 | ID | structural_missing_delim | 30-010 | Missing delimiter after 'ID 1: Issued By' (position 64) — merges with next field and shifts every subsequent field left by one |
| 895 | CI | valid_optional_blank | *(none — should pass clean)* | Optional field 'Board Resolution flag' intentionally left blank — should NOT be flagged as an error |
| 896 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 897 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 898 | CI | valid_optional_blank | *(none — should pass clean)* | Optional field 'Purpose of credit' intentionally left blank — should NOT be flagged as an error |
| 899 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 900 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 901 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 902 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 903 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 904 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 905 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 906 | CI | valid_optional_blank | *(none — should pass clean)* | Optional field 'Board Resolution flag' intentionally left blank — should NOT be flagged as an error |
| 907 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 908 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 909 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 910 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 911 | ID | structural_provider_code | 30-003 | Provider Code changed to 'RB001900' — inconsistent with the file's actual submitting provider 'RB001800' |
| 912 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 913 | ID | formatting | 10-xxx | Field 'First Name' has leading/trailing whitespace padding (copy-paste artifact) |
| 914 | ID | duplicate_psn | 10-090 | Provider Subject No duplicated to '1190024633', which is already used by another subject in this file |
| 915 | CI | structural_missing_delim | 30-010 | Missing delimiter after 'Good Type' (position 35) — merges with next field and shifts every subsequent field left by one |
| 916 | CI | structural_missing_delim | 30-010 | Missing delimiter after 'Payment Method' (position 24) — merges with next field and shifts every subsequent field left by one |
| 917 | ID | valid_optional_blank | *(none — should pass clean)* | Optional field 'Spouse First Name' intentionally left blank — should NOT be flagged as an error |
| 918 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 919 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 920 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 921 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 922 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 923 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 924 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 925 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 926 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 927 | ID | formatting | 10-xxx | Field 'Gender' value lower-cased ('F' -> 'f'), domain codes are case-sensitive |
| 928 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 929 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 930 | CI | missing_mandatory | 10-027 | Mandatory field 'Currency' left blank (simulates encoder skipping a required cell) |
| 931 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 932 | ID | structural_missing_delim | 30-010 | Missing delimiter after 'Contact 1: Type' (position 77) — merges with next field and shifts every subsequent field left by one |
| 933 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 934 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 935 | ID | missing_mandatory | 20-002 | Mandatory field 'First Name' left blank (simulates encoder skipping a required cell) |
| 936 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 937 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 938 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 939 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 940 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 941 | CI | domain_violation | 10-xxx | Role entered as 'Borrower' (spelled out) instead of domain code 'B' |
| 942 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 943 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 944 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 945 | ID | address_completeness | 20-139 | Address 1: Address Type is filled but neither FullAddress nor the StreetNo+City+Province trio is filled in |
| 946 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 947 | CI | conditional_mandatory | 20-089 | Contract Phase is 'AC' so 'Last payment amount' is conditionally mandatory, but it was left blank |
| 948 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 949 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 950 | ID | address_completeness | 20-139 | Address 1: Address Type is filled but neither FullAddress nor the StreetNo+City+Province trio is filled in |
| 951 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 952 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 953 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 954 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 955 | ID | missing_mandatory | 20-003 | Mandatory field 'Last Name' left blank (simulates encoder skipping a required cell) |
| 956 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 957 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 958 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 959 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 960 | ID | formatting | 10-xxx | Field 'Gender' value lower-cased ('M' -> 'm'), domain codes are case-sensitive |
| 961 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 962 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 963 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 964 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 965 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 966 | CI | domain_violation | 10-xxx | Contract Status entered as 'ACTIVE' (spelled out) instead of a valid domain code |
| 967 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 968 | ID | natural_structural | 30-010 | Naturally-occurring malformed record from source data (125 fields instead of 123) — real human data-entry error, not synthetically injected |
| 969 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 970 | ID | paired_field | 10-069 | 'Identification 1: Type' is filled in but 'Identification 1: Number' was left blank — paired fields must be both empty or both filled |
| 971 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 972 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 973 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 974 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 975 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 976 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 977 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 978 | ID | formatting | 10-xxx | Field 'Provider Subject No' has a leading apostrophe left over from Excel 'format as text' trick: "'1190009293" |
| 979 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 980 | ID | missing_mandatory | unmapped | Mandatory field 'Civil Status' left blank (simulates encoder skipping a required cell) |
| 981 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 982 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 983 | CI | missing_mandatory | 10-163 | Mandatory field 'Payment Periodicity' left blank (simulates encoder skipping a required cell) |
| 984 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 985 | ID | numeric_typo | 10-xxx | Field 'Identification 1: Number' has a letter 'O' typed instead of digit '0': '4944O25157' |
| 986 | Id | structural_record_type | 30-009 | Record Type typo: 'Id' instead of 'ID' (fat-fingered or autocorrected) |
| 987 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 988 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 989 | ID | structural_missing_delim | 30-010 | Missing delimiter after 'Contact 1: Type' (position 77) — merges with next field and shifts every subsequent field left by one |
| 990 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 991 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 992 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 993 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 994 | CI | date_format | 10-005 | Field 'Contract Start Date' entered as ISO date '2025-04-30' instead of DDMMYYYY '30042025' (common spreadsheet auto-format error) |
| 995 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 996 | CI | valid_optional_blank | *(none — should pass clean)* | Optional field 'New/Used Code' intentionally left blank — should NOT be flagged as an error |
| 997 | CI | domain_violation | 10-xxx | Contract Status entered as 'ACTIVE' (spelled out) instead of a valid domain code |
| 998 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 999 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1000 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1001 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1002 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1003 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1004 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1005 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1006 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1007 | CI | conditional_mandatory | 20-090 | Contract Phase is 'AC' so 'Overdue Days' is conditionally mandatory, but it was left blank |
| 1008 | ID | missing_mandatory | unmapped | Mandatory field 'Civil Status' left blank (simulates encoder skipping a required cell) |
| 1009 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1010 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1011 | ID | valid_optional_blank | *(none — should pass clean)* | Optional field 'Identification 3: Type' intentionally left blank — should NOT be flagged as an error |
| 1012 | ID | domain_violation | 10-xxx | Civil Status set to '9', which is not in the valid domain {1,2,3,4} |
| 1013 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1014 | ID | domain_violation | 10-004 | Gender entered as 'Male' instead of domain code M/F |
| 1015 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1016 | ID | domain_violation | 10-004 | Gender entered as 'Male' instead of domain code M/F |
| 1017 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1018 | ID | missing_mandatory | 20-001 | Mandatory field 'Gender' left blank (simulates encoder skipping a required cell) |
| 1019 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1020 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1021 | ID | numeric_typo | 10-xxx | Field 'Identification 1: Number' has a letter 'O' typed instead of digit '0': '2845O31791' |
| 1022 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1023 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1024 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1025 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1026 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1027 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1028 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1029 | ID | formatting | 10-xxx | Field 'First Name' has leading/trailing whitespace padding (copy-paste artifact) |
| 1030 | CI | domain_violation | 10-xxx | Role entered as 'Borrower' (spelled out) instead of domain code 'B' |
| 1031 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1032 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1033 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1034 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1035 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1036 | ID | formatting | 10-xxx | Last Name contains a Word-autocorrected curly apostrophe (’) instead of a straight one |
| 1037 | CI | formatting | 10-xxx | Field 'Financed Amount' has a trailing '.00' from an Excel-formatted numeric cell ('20000.00' instead of '20000') |
| 1038 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1039 | ID | valid_optional_blank | *(none — should pass clean)* | Optional field 'Car/s Owned' intentionally left blank — should NOT be flagged as an error |
| 1040 | ID | missing_mandatory | unmapped | Mandatory field 'Title' left blank (simulates encoder skipping a required cell) |
| 1041 | CI | conditional_mandatory | 20-089 | Contract Phase is 'AC' so 'Last payment amount' is conditionally mandatory, but it was left blank |
| 1042 | ID | formatting | 10-xxx | Field 'Provider Subject No' has a leading apostrophe left over from Excel 'format as text' trick: "'1190025992" |
| 1043 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1044 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1045 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1046 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1047 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1048 | ID | numeric_typo | 10-xxx | Field 'Identification 1: Number' has a letter 'O' typed instead of digit '0': '1798O93432' |
| 1049 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1050 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1051 | ID | domain_violation | 10-xxx | Civil Status set to '9', which is not in the valid domain {1,2,3,4} |
| 1052 | CI | valid_optional_blank | *(none — should pass clean)* | Optional field 'New/Used Code' intentionally left blank — should NOT be flagged as an error |
| 1053 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1054 | CI | missing_mandatory | 10-024 | Mandatory field 'Contract Phase' left blank (simulates encoder skipping a required cell) |
| 1055 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1056 | ID | valid_optional_blank | *(none — should pass clean)* | Optional field 'Spouse First Name' intentionally left blank — should NOT be flagged as an error |
| 1057 | ID | contact_missing | 20-104 | Both Contact 1 and Contact 2 Type/Value are blank — at least one Contact:Type must be filled |
| 1058 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1059 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1060 | ID | address_completeness | 20-139 | Address 2: Address Type is filled but neither FullAddress nor the StreetNo+City+Province trio is filled in |
| 1061 | ID | natural_structural | 30-010 | Naturally-occurring malformed record from source data (122 fields instead of 123) — real human data-entry error, not synthetically injected |
| 1062 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1063 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1064 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1065 | CI | formatting | 10-xxx | Field 'Financed Amount' has a trailing '.00' from an Excel-formatted numeric cell ('80000.00' instead of '80000') |
| 1066 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1067 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1068 | CI | valid_optional_blank | *(none — should pass clean)* | Optional field 'Good Type' intentionally left blank — should NOT be flagged as an error |
| 1069 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1070 | ID | paired_field | 10-069 | 'Identification 1: Type' is filled in but 'Identification 1: Number' was left blank — paired fields must be both empty or both filled |
| 1071 | ID | valid_optional_blank | *(none — should pass clean)* | Optional field 'Identification 3: Type' intentionally left blank — should NOT be flagged as an error |
| 1072 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1073 | ID | natural_structural | 30-010 | Naturally-occurring malformed record from source data (122 fields instead of 123) — real human data-entry error, not synthetically injected |
| 1074 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1075 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1076 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1077 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1078 | ID | age_range | 20-137 | Date of Birth changed to '27091920' so computed age is out of the 18-100 valid range |
| 1079 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1080 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1081 | ID | structural_extra_delim | 30-010 | Extra delimiter inserted before 'Middle Name' (position 8) — adds a spurious empty field and shifts everything after right by one |
| 1082 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1083 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1084 | ID | age_range | 20-137 | Date of Birth changed to '17082015' so computed age is out of the 18-100 valid range |
| 1085 | ID | structural_provider_code | 30-003 | Provider Code changed to 'RB001900' — inconsistent with the file's actual submitting provider 'RB001800' |
| 1086 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1087 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1088 | CI | structural_missing_delim | 30-010 | Missing delimiter after 'Contract Status' (position 9) — merges with next field and shifts every subsequent field left by one |
| 1089 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1090 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1091 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1092 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1093 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1094 | ID | formatting | 10-xxx | Field 'Gender' has leading/trailing whitespace padding (copy-paste artifact) |
| 1095 | ID | structural_missing_delim | 30-010 | Missing delimiter after 'Address 1: FullAddress' (position 32) — merges with next field and shifts every subsequent field left by one |
| 1096 | CI | formatting | 10-xxx | Field 'Financed Amount' has a trailing '.00' from an Excel-formatted numeric cell ('6000000.00' instead of '6000000') |
| 1097 | ID | structural_provider_code | 30-003 | Provider Code changed to 'RB001900' — inconsistent with the file's actual submitting provider 'RB001800' |
| 1098 | ID | missing_mandatory | 10-120 | Mandatory field 'Provider Subject No' left blank (simulates encoder skipping a required cell) |
| 1099 | CI | missing_mandatory | 10-030 | Mandatory field 'Installments Number' left blank (simulates encoder skipping a required cell) |
| 1100 | ID | missing_mandatory | 20-001 | Mandatory field 'Gender' left blank (simulates encoder skipping a required cell) |
| 1101 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1102 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1103 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1104 | ID | structural_missing_delim | 30-010 | Missing delimiter after 'Contact 1: Type' (position 77) — merges with next field and shifts every subsequent field left by one |
| 1105 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1106 | ID | valid_optional_blank | *(none — should pass clean)* | Optional field 'Car/s Owned' intentionally left blank — should NOT be flagged as an error |
| 1107 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1108 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1109 | ID | paired_field | 10-069 | 'ID 1: Type' is filled in but 'ID 1: Number' was left blank — paired fields must be both empty or both filled |
| 1110 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1111 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1112 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1113 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1114 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1115 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1116 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1117 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1118 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1119 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1120 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1121 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1122 | ID | natural_structural | 30-010 | Naturally-occurring malformed record from source data (122 fields instead of 123) — real human data-entry error, not synthetically injected |
| 1123 | D | structural_record_type | 30-009 | Record Type typo: 'D' instead of 'ID' (fat-fingered or autocorrected) |
| 1124 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1125 | ID | structural_provider_code | 30-003 | Provider Code changed to 'RB001900' — inconsistent with the file's actual submitting provider 'RB001800' |
| 1126 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1127 | ID | missing_mandatory | unmapped | Mandatory field 'Mother’s Maiden FULL NAME' left blank (simulates encoder skipping a required cell) |
| 1128 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1129 | ID | formatting | 10-xxx | Field 'First Name' has leading/trailing whitespace padding (copy-paste artifact) |
| 1130 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1131 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1132 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1133 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1134 | ID | formatting | 10-xxx | Field 'First Name' has leading/trailing whitespace padding (copy-paste artifact) |
| 1135 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1136 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1137 | ID | structural_extra_delim | 30-010 | Extra delimiter inserted before 'ID 1: Issued By' (position 64) — adds a spurious empty field and shifts everything after right by one |
| 1138 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1139 | CI | missing_mandatory | 10-023 | Mandatory field 'Contract Type' left blank (simulates encoder skipping a required cell) |
| 1140 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1141 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1142 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1143 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1144 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1145 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1146 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1147 | ID | age_range | 20-137 | Date of Birth changed to '23021920' so computed age is out of the 18-100 valid range |
| 1148 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1149 | CI | valid_optional_blank | *(none — should pass clean)* | Optional field 'Board Resolution flag' intentionally left blank — should NOT be flagged as an error |
| 1150 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1151 | ID | date_format | 10-005 | Field 'Date of Birth' entered as ISO date '1982-12-02' instead of DDMMYYYY '02121982' (common spreadsheet auto-format error) |
| 1152 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1153 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1154 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1155 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1156 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1157 | CI | formatting | 10-xxx | Field 'Financed Amount' has a trailing '.00' from an Excel-formatted numeric cell ('119000.00' instead of '119000') |
| 1158 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1159 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1160 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1161 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1162 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1163 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1164 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1165 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1166 | CI | missing_mandatory | 10-023 | Mandatory field 'Contract Type' left blank (simulates encoder skipping a required cell) |
| 1167 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1168 | ID | valid_optional_blank | *(none — should pass clean)* | Optional field 'Number of Dependents' intentionally left blank — should NOT be flagged as an error |
| 1169 | ID | domain_violation | 10-004 | Gender entered as 'Female' instead of domain code M/F |
| 1170 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1171 | ID | missing_mandatory | 20-001 | Mandatory field 'Gender' left blank (simulates encoder skipping a required cell) |
| 1172 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1173 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1174 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1175 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1176 | ID | structural_provider_code | 30-003 | Provider Code changed to 'RB001900' — inconsistent with the file's actual submitting provider 'RB001800' |
| 1177 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1178 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1179 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1180 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1181 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1182 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1183 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1184 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1185 | ID | age_range | 20-137 | Date of Birth changed to '11051920' so computed age is out of the 18-100 valid range |
| 1186 | ID | natural_structural | 30-010 | Naturally-occurring malformed record from source data (122 fields instead of 123) — real human data-entry error, not synthetically injected |
| 1187 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1188 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1189 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1190 | CI | conditional_mandatory | 20-090 | Contract Phase is 'AC' so 'Overdue Days' is conditionally mandatory, but it was left blank |
| 1191 | CI | conditional_mandatory | 20-090 | Contract Phase is 'AC' so 'Overdue Days' is conditionally mandatory, but it was left blank |
| 1192 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1193 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1194 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1195 | ID | address_completeness | 20-139 | Address 2: Address Type is filled but neither FullAddress nor the StreetNo+City+Province trio is filled in |
| 1196 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1197 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1198 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1199 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1200 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1201 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1202 | ID | contact_missing | 20-104 | Both Contact 1 and Contact 2 Type/Value are blank — at least one Contact:Type must be filled |
| 1203 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1204 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1205 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1206 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1207 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1208 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1209 | ID | valid_optional_blank | *(none — should pass clean)* | Optional field 'Car/s Owned' intentionally left blank — should NOT be flagged as an error |
| 1210 | ID | formatting | 10-xxx | Last Name contains a Word-autocorrected curly apostrophe (’) instead of a straight one |
| 1211 | ID | domain_violation | 10-004 | Gender entered as 'Female' instead of domain code M/F |
| 1212 | ID | valid_optional_blank | *(none — should pass clean)* | Optional field 'Nickname' intentionally left blank — should NOT be flagged as an error |
| 1213 | CI | structural_missing_delim | 30-010 | Missing delimiter after 'Contract Status' (position 9) — merges with next field and shifts every subsequent field left by one |
| 1214 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1215 | CI | domain_violation | 10-xxx | Role entered as 'Borrower' (spelled out) instead of domain code 'B' |
| 1216 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1217 | ID | missing_mandatory | unmapped | Mandatory field 'Middle Name' left blank (simulates encoder skipping a required cell) |
| 1218 | CI | valid_optional_blank | *(none — should pass clean)* | Optional field 'New/Used Code' intentionally left blank — should NOT be flagged as an error |
| 1219 | ID | age_range | 20-137 | Date of Birth changed to '02111920' so computed age is out of the 18-100 valid range |
| 1220 | CI | missing_mandatory | 10-027 | Mandatory field 'Currency' left blank (simulates encoder skipping a required cell) |
| 1221 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1222 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1223 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1224 | ID | formatting | 10-xxx | Field 'Gender' value lower-cased ('F' -> 'f'), domain codes are case-sensitive |
| 1225 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1226 | CI | conditional_mandatory | 20-089 | Contract Phase is 'AC' so 'Last payment amount' is conditionally mandatory, but it was left blank |
| 1227 | ID | missing_mandatory | 10-120 | Mandatory field 'Provider Subject No' left blank (simulates encoder skipping a required cell) |
| 1228 | ID | contact_missing | 20-104 | Both Contact 1 and Contact 2 Type/Value are blank — at least one Contact:Type must be filled |
| 1229 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1230 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1231 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1232 | CI | valid_optional_blank | *(none — should pass clean)* | Optional field 'Good Type' intentionally left blank — should NOT be flagged as an error |
| 1233 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1234 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1235 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1236 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1237 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1238 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1239 | CI | missing_mandatory | 10-030 | Mandatory field 'Installments Number' left blank (simulates encoder skipping a required cell) |
| 1240 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1241 | ID | formatting | 10-xxx | Field 'Provider Subject No' has a leading apostrophe left over from Excel 'format as text' trick: "'1190025364" |
| 1242 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1243 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1244 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1245 | ID | natural_structural | 30-010 | Naturally-occurring malformed record from source data (124 fields instead of 123) — real human data-entry error, not synthetically injected |
| 1246 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1247 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1248 | CI | missing_mandatory | 10-152 | Mandatory field 'Role' left blank (simulates encoder skipping a required cell) |
| 1249 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1250 | ID | natural_structural | 30-010 | Naturally-occurring malformed record from source data (124 fields instead of 123) — real human data-entry error, not synthetically injected |
| 1251 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1252 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1253 | ID | missing_mandatory | 10-120 | Mandatory field 'Provider Subject No' left blank (simulates encoder skipping a required cell) |
| 1254 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1255 | CI | missing_mandatory | 10-024 | Mandatory field 'Contract Phase' left blank (simulates encoder skipping a required cell) |
| 1256 | ID | structural_provider_code | 30-003 | Provider Code changed to 'RB001900' — inconsistent with the file's actual submitting provider 'RB001800' |
| 1257 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1258 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1259 | ID | formatting | 10-xxx | Field 'First Name' has leading/trailing whitespace padding (copy-paste artifact) |
| 1260 | ID | domain_violation | 10-004 | Gender entered as 'Male' instead of domain code M/F |
| 1261 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1262 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1263 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1264 | ID | missing_mandatory | 20-002 | Mandatory field 'First Name' left blank (simulates encoder skipping a required cell) |
| 1265 | ID | valid_optional_blank | *(none — should pass clean)* | Optional field 'Father First Name' intentionally left blank — should NOT be flagged as an error |
| 1266 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1267 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1268 | ID | formatting | 10-xxx | Field 'Gender' has leading/trailing whitespace padding (copy-paste artifact) |
| 1269 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1270 | CI | missing_mandatory | 30-024 | Mandatory field 'Provider Contract No' left blank (simulates encoder skipping a required cell) |
| 1271 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1272 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1273 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1274 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1275 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1276 | ID | missing_mandatory | unmapped | Mandatory field 'Mother’s Maiden FULL NAME' left blank (simulates encoder skipping a required cell) |
| 1277 | CI | conditional_mandatory | 20-089 | Contract Phase is 'AC' so 'Last payment amount' is conditionally mandatory, but it was left blank |
| 1278 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1279 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1280 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1281 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1282 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1283 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1284 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1285 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1286 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1287 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1288 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1289 | CI | missing_mandatory | 10-152 | Mandatory field 'Role' left blank (simulates encoder skipping a required cell) |
| 1290 | CI | domain_violation | 10-xxx | Role entered as 'Borrower' (spelled out) instead of domain code 'B' |
| 1291 | CI | structural_missing_delim | 30-010 | Missing delimiter after 'Contract Status' (position 9) — merges with next field and shifts every subsequent field left by one |
| 1292 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1293 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1294 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1295 | ID | missing_mandatory | unmapped | Mandatory field 'Title' left blank (simulates encoder skipping a required cell) |
| 1296 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1297 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1298 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1299 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1300 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1301 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1302 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1303 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1304 | CI | conditional_mandatory | 10-268 | Contract Phase is 'AC' so 'Monthly Payment Amount' is conditionally mandatory, but it was left blank |
| 1305 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1306 | ID | structural_extra_delim | 30-010 | Extra delimiter inserted before 'ID 1: Issued By' (position 64) — adds a spurious empty field and shifts everything after right by one |
| 1307 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1308 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1309 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1310 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1311 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1312 | CI | structural_missing_delim | 30-010 | Missing delimiter after 'Payment Method' (position 24) — merges with next field and shifts every subsequent field left by one |
| 1313 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1314 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1315 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1316 | ID | formatting | 10-xxx | Field 'Gender' has leading/trailing whitespace padding (copy-paste artifact) |
| 1317 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1318 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1319 | ID | valid_optional_blank | *(none — should pass clean)* | Optional field 'Car/s Owned' intentionally left blank — should NOT be flagged as an error |
| 1320 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1321 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1322 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1323 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1324 | CI | domain_violation | 10-xxx | Role entered as 'Borrower' (spelled out) instead of domain code 'B' |
| 1325 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1326 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1327 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1328 | ID | date_format | 10-005 | Field 'Date of Birth' entered as ISO date '1975-05-28' instead of DDMMYYYY '28051975' (common spreadsheet auto-format error) |
| 1329 | XX | structural_record_type | 30-009 | Record Type typo: 'XX' instead of 'ID' (fat-fingered or autocorrected) |
| 1330 | ID | formatting | 10-xxx | Field 'First Name' has leading/trailing whitespace padding (copy-paste artifact) |
| 1331 | ID | structural_extra_delim | 30-010 | Extra delimiter inserted before 'Middle Name' (position 8) — adds a spurious empty field and shifts everything after right by one |
| 1332 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1333 | ID | formatting | 10-xxx | Field 'Gender' has leading/trailing whitespace padding (copy-paste artifact) |
| 1334 | CI | missing_mandatory | 10-030 | Mandatory field 'Installments Number' left blank (simulates encoder skipping a required cell) |
| 1335 | CI | conditional_mandatory | 20-089 | Contract Phase is 'AC' so 'Last payment amount' is conditionally mandatory, but it was left blank |
| 1336 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1337 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1338 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1339 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1340 | CI | missing_mandatory | 10-161 | Mandatory field 'Financed Amount' left blank (simulates encoder skipping a required cell) |
| 1341 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1342 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1343 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1344 | CI | numeric_typo | 10-xxx | Field 'Financed Amount' has a letter 'O' typed instead of digit '0': '98O000' |
| 1345 | ID | missing_mandatory | 20-003 | Mandatory field 'Last Name' left blank (simulates encoder skipping a required cell) |
| 1346 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1347 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1348 | ID | missing_mandatory | 10-109 | Mandatory field 'Subject Reference Date' left blank (simulates encoder skipping a required cell) |
| 1349 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1350 | ID | valid_optional_blank | *(none — should pass clean)* | Optional field 'Father First Name' intentionally left blank — should NOT be flagged as an error |
| 1351 | ID | formatting | 10-xxx | Field 'First Name' has leading/trailing whitespace padding (copy-paste artifact) |
| 1352 | CI | conditional_mandatory | 10-268 | Contract Phase is 'AC' so 'Monthly Payment Amount' is conditionally mandatory, but it was left blank |
| 1353 | CI | missing_mandatory | 30-024 | Mandatory field 'Provider Contract No' left blank (simulates encoder skipping a required cell) |
| 1354 | CI | domain_violation | 10-xxx | Role entered as 'Borrower' (spelled out) instead of domain code 'B' |
| 1355 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1356 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1357 | CI | conditional_mandatory | 10-268 | Contract Phase is 'AC' so 'Monthly Payment Amount' is conditionally mandatory, but it was left blank |
| 1358 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1359 | CI | numeric_typo | 10-xxx | Field 'Financed Amount' has a letter 'O' typed instead of digit '0': '129O0800' |
| 1360 | ID | natural_structural | 30-010 | Naturally-occurring malformed record from source data (124 fields instead of 123) — real human data-entry error, not synthetically injected |
| 1361 | ID | duplicate_psn | 10-090 | Provider Subject No duplicated to '1190025838', which is already used by another subject in this file |
| 1362 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1363 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1364 | ID | domain_violation | 10-004 | Gender entered as 'm' instead of domain code M/F |
| 1365 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1366 | ID | formatting | 10-xxx | Field 'Gender' has leading/trailing whitespace padding (copy-paste artifact) |
| 1367 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1368 | ID | structural_provider_code | 30-003 | Provider Code changed to 'RB001900' — inconsistent with the file's actual submitting provider 'RB001800' |
| 1369 | ID | natural_structural | 30-010 | Naturally-occurring malformed record from source data (122 fields instead of 123) — real human data-entry error, not synthetically injected |
| 1370 | ID | date_format | 10-005 | Field 'Date of Birth' entered as ISO date '1976-04-20' instead of DDMMYYYY '20041976' (common spreadsheet auto-format error) |
| 1371 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1372 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1373 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1374 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1375 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1376 | D | structural_record_type | 30-009 | Record Type typo: 'D' instead of 'ID' (fat-fingered or autocorrected) |
| 1377 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1378 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1379 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1380 | ID | formatting | 10-xxx | Last Name contains a Word-autocorrected curly apostrophe (’) instead of a straight one |
| 1381 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1382 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1383 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1384 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1385 | CI | missing_mandatory | 10-027 | Mandatory field 'Currency' left blank (simulates encoder skipping a required cell) |
| 1386 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1387 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1388 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1389 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1390 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1391 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1392 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1393 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1394 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1395 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1396 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1397 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1398 | ID | domain_violation | 10-xxx | Civil Status set to '9', which is not in the valid domain {1,2,3,4} |
| 1399 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1400 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1401 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1402 | ID | structural_missing_delim | 30-010 | Missing delimiter after 'Middle Name' (position 8) — merges with next field and shifts every subsequent field left by one |
| 1403 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1404 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1405 | ID | paired_field | 10-069 | 'ID 1: Type' is filled in but 'ID 1: Number' was left blank — paired fields must be both empty or both filled |
| 1406 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1407 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1408 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1409 | CI | structural_missing_delim | 30-010 | Missing delimiter after 'Contract Status' (position 9) — merges with next field and shifts every subsequent field left by one |
| 1410 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1411 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1412 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1413 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1414 | ID | date_format | 10-005 | Field 'Date of Birth' entered as ISO date '1986-04-21' instead of DDMMYYYY '21041986' (common spreadsheet auto-format error) |
| 1415 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1416 | ID | domain_violation | 10-xxx | Civil Status set to '9', which is not in the valid domain {1,2,3,4} |
| 1417 | ID | formatting | 10-xxx | Last Name contains a Word-autocorrected curly apostrophe (’) instead of a straight one |
| 1418 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1419 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1420 | ID | formatting | 10-xxx | Last Name contains a Word-autocorrected curly apostrophe (’) instead of a straight one |
| 1421 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1422 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1423 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1424 | ID | valid_optional_blank | *(none — should pass clean)* | Optional field 'Identification 2: Type' intentionally left blank — should NOT be flagged as an error |
| 1425 | ID | natural_structural | 30-010 | Naturally-occurring malformed record from source data (122 fields instead of 123) — real human data-entry error, not synthetically injected |
| 1426 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1427 | ID | structural_extra_delim | 30-010 | Extra delimiter inserted before 'Contact 1: Type' (position 77) — adds a spurious empty field and shifts everything after right by one |
| 1428 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1429 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1430 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1431 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1432 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1433 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1434 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1435 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1436 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1437 | ID | valid_optional_blank | *(none — should pass clean)* | Optional field 'Nickname' intentionally left blank — should NOT be flagged as an error |
| 1438 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1439 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1440 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1441 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1442 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1443 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1444 | CI | date_format | 10-005 | Field 'Contract Start Date' entered as ISO date '2025-04-08' instead of DDMMYYYY '08042025' (common spreadsheet auto-format error) |
| 1445 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1446 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1447 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1448 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1449 | CI | missing_mandatory | 30-024 | Mandatory field 'Provider Contract No' left blank (simulates encoder skipping a required cell) |
| 1450 | CI | date_format | 10-005 | Field 'Contract Start Date' entered as ISO date '2023-09-21' instead of DDMMYYYY '21092023' (common spreadsheet auto-format error) |
| 1451 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1452 | CI | missing_mandatory | 10-023 | Mandatory field 'Contract Type' left blank (simulates encoder skipping a required cell) |
| 1453 | CI | domain_violation | 10-xxx | Contract Status entered as 'ACTIVE' (spelled out) instead of a valid domain code |
| 1454 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1455 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1456 | CI | missing_mandatory | 10-027 | Mandatory field 'Currency' left blank (simulates encoder skipping a required cell) |
| 1457 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1458 | CI | conditional_mandatory | 20-089 | Contract Phase is 'AC' so 'Last payment amount' is conditionally mandatory, but it was left blank |
| 1459 | ID | missing_mandatory | unmapped | Mandatory field 'Title' left blank (simulates encoder skipping a required cell) |
| 1460 | CI | conditional_mandatory | 20-089 | Contract Phase is 'AC' so 'Last payment amount' is conditionally mandatory, but it was left blank |
| 1461 | ID | duplicate_psn | 10-090 | Provider Subject No duplicated to '1190001630', which is already used by another subject in this file |
| 1462 | CI | missing_mandatory | 10-024 | Mandatory field 'Contract Phase' left blank (simulates encoder skipping a required cell) |
| 1463 | ID | domain_violation | 10-xxx | Civil Status set to '9', which is not in the valid domain {1,2,3,4} |
| 1464 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1465 | ID | missing_mandatory | 10-109 | Mandatory field 'Subject Reference Date' left blank (simulates encoder skipping a required cell) |
| 1466 | ID | missing_mandatory | unmapped | Mandatory field 'Mother’s Maiden FULL NAME' left blank (simulates encoder skipping a required cell) |
| 1467 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1468 | CI | conditional_mandatory | 20-089 | Contract Phase is 'AC' so 'Last payment amount' is conditionally mandatory, but it was left blank |
| 1469 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1470 | CI | missing_mandatory | 10-152 | Mandatory field 'Role' left blank (simulates encoder skipping a required cell) |
| 1471 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1472 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1473 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1474 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1475 | ID | formatting | 10-xxx | Last Name contains a Word-autocorrected curly apostrophe (’) instead of a straight one |
| 1476 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1477 | CI | missing_mandatory | 10-030 | Mandatory field 'Installments Number' left blank (simulates encoder skipping a required cell) |
| 1478 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1479 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1480 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1481 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1482 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1483 | CI | structural_missing_delim | 30-010 | Missing delimiter after 'Good Type' (position 35) — merges with next field and shifts every subsequent field left by one |
| 1484 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1485 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1486 | CI | conditional_mandatory | 20-090 | Contract Phase is 'AC' so 'Overdue Days' is conditionally mandatory, but it was left blank |
| 1487 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1488 | ID | contact_missing | 20-104 | Both Contact 1 and Contact 2 Type/Value are blank — at least one Contact:Type must be filled |
| 1489 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1490 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1491 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1492 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1493 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1494 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1495 | ID | valid_optional_blank | *(none — should pass clean)* | Optional field 'Father First Name' intentionally left blank — should NOT be flagged as an error |
| 1496 | ID | age_range | 20-137 | Date of Birth changed to '28112015' so computed age is out of the 18-100 valid range |
| 1497 | CI | formatting | 10-xxx | Field 'Financed Amount' has a trailing '.00' from an Excel-formatted numeric cell ('250000.00' instead of '250000') |
| 1498 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1499 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1500 | ID | formatting | 10-xxx | Field 'Provider Subject No' has a leading apostrophe left over from Excel 'format as text' trick: "'1250002738" |
| 1501 | CI | missing_mandatory | 10-161 | Mandatory field 'Financed Amount' left blank (simulates encoder skipping a required cell) |
| 1502 | ID | valid_optional_blank | *(none — should pass clean)* | Optional field 'Car/s Owned' intentionally left blank — should NOT be flagged as an error |
| 1503 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1504 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1505 | ID | age_range | 20-137 | Date of Birth changed to '04092015' so computed age is out of the 18-100 valid range |
| 1506 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1507 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1508 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1509 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1510 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1511 | ID | missing_mandatory | 10-109 | Mandatory field 'Subject Reference Date' left blank (simulates encoder skipping a required cell) |
| 1512 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1513 | CI | domain_violation | 10-xxx | Contract Status entered as 'ACTIVE' (spelled out) instead of a valid domain code |
| 1514 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1515 | ID | numeric_typo | 10-xxx | Field 'Identification 1: Number' has a letter 'O' typed instead of digit '0': '4321O16375' |
| 1516 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1517 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1518 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1519 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1520 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1521 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1522 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1523 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1524 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1525 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1526 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1527 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1528 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1529 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1530 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1531 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1532 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1533 | ID | missing_mandatory | unmapped | Mandatory field 'Identification 1: Type' left blank (simulates encoder skipping a required cell) |
| 1534 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1535 | ID | valid_optional_blank | *(none — should pass clean)* | Optional field 'Identification 2: Type' intentionally left blank — should NOT be flagged as an error |
| 1536 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1537 | CI | missing_mandatory | 10-152 | Mandatory field 'Role' left blank (simulates encoder skipping a required cell) |
| 1538 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1539 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1540 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1541 | ID | valid_optional_blank | *(none — should pass clean)* | Optional field 'Number of Dependents' intentionally left blank — should NOT be flagged as an error |
| 1542 | CI | numeric_typo | 10-xxx | Field 'Financed Amount' has a letter 'O' typed instead of digit '0': '380O000' |
| 1543 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1544 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1545 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1546 | ID | missing_mandatory | unmapped | Mandatory field 'Mother’s Maiden FULL NAME' left blank (simulates encoder skipping a required cell) |
| 1547 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1548 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1549 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1550 | CI | numeric_typo | 10-xxx | Field 'Financed Amount' has a letter 'O' typed instead of digit '0': '120O0000' |
| 1551 | ID | structural_extra_delim | 30-010 | Extra delimiter inserted before 'Contact 1: Type' (position 77) — adds a spurious empty field and shifts everything after right by one |
| 1552 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1553 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1554 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1555 | ID | formatting | 10-xxx | Field 'Gender' has leading/trailing whitespace padding (copy-paste artifact) |
| 1556 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1557 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1558 | ID | valid_optional_blank | *(none — should pass clean)* | Optional field 'Nickname' intentionally left blank — should NOT be flagged as an error |
| 1559 | ID | age_range | 20-137 | Date of Birth changed to '11012015' so computed age is out of the 18-100 valid range |
| 1560 | CI | domain_violation | 10-xxx | Contract Status entered as 'ACTIVE' (spelled out) instead of a valid domain code |
| 1561 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1562 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1563 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1564 | ID | missing_mandatory | unmapped | Mandatory field 'Title' left blank (simulates encoder skipping a required cell) |
| 1565 | ID | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1566 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1567 | CI | clean | *(none — should pass clean)* | Clean, unmodified real production record — should produce zero errors |
| 1568 | FT | structural_ft_count_mismatch | 30-xxx | FT declares 1559 records but the file actually contains 1566 detail records (HD and FT excluded) — deliberate mismatch, single dedicated test case since only one FT record exists per file |