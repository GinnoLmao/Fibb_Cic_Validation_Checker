"""Annotate the canonical record-type field schema with mandatory/conditional flags,
domain references, data types, and max-length hints based on the CIC reference docs.

Run from the project root:
    .venv\\Scripts\\python.exe -m cic_validator.tools.annotate_schema

This script is idempotent and writes the annotated schema back to
schema/record_type_field_schema.json.
"""
from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "cic_validator" / "schema" / "record_type_field_schema.json"


def normalize(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", name.lower())


# ---------------------------------------------------------------------------
# Domain mapping
# ---------------------------------------------------------------------------

DOMAIN_MAP = {
    "ID": {
        "Title": "ID - Individual :: TITLE DOMAIN",
        "Gender": "ID - Individual :: GENDER DOMAIN",
        "Civil Status": "ID - Individual :: CivilStatusDomain",
        "Country of Birth (Code)": "ID - Individual :: COUNTRY",
        "Nationality": "ID - Individual :: COUNTRY",
        "Resident": "ID - Individual :: YesNoDomain",
        "Address Type": "ID - Individual :: Address Type",
        "House Owner/Lessee": "ID - Individual :: HouseOwnerLesseeType",
        "Identification Type": "ID - Individual :: IdentificationTypeDomain",
        "ID Type": "ID - Individual :: IDTypeDomain",
        "Contact Type": "ID - Individual :: ContactTypeDomain",
        "PSIC": "ID - Individual :: PSICDomain",
        "Occupation": "ID - Individual :: PSOCDomain",
        "OccupationStatus": "ID - Individual :: OccupationStatusDomain",
        "Annual/Monthly Indicator": "ID - Individual :: AnnualMonthlyDomain",
        "Currency": "ID - Individual :: CurrencyDomain",
    },
    "BD": {
        "Legal Form": "BD - Business Data :: LegalFormDomain",
        "Firm Size": "BD - Business Data :: Firm Size",
        "Address Type": "BD - Business Data :: Address Type",
        "House Owner/Lessee": "ID - Individual :: HouseOwnerLesseeType",
        "Identification Type": "ID - Individual :: IdentificationTypeDomain",
        "Contact Type": "ID - Individual :: ContactTypeDomain",
        "Currency": "ID - Individual :: CurrencyDomain",
    },
    "CI": {
        "Role": "CI - Installment Contract :: RoleDomain",
        "Contract Type": "CI - Installment Contract :: ContractTypeDomain (CorrectedFull)",
        "Contract Phase": "CI - Installment Contract :: ContractPhaseDomain",
        "Contract Status": "CI - Installment Contract :: ContractStatusDomain",
        "Currency": "ID - Individual :: CurrencyDomain",
        "Original Currency": "ID - Individual :: CurrencyDomain",
        "Transaction Type / Sub-facility": "CI - Installment Contract :: TransactionTypeDomain",
        "Payment Periodicity": "CI - Installment Contract :: PaymentPeriodicityDomain",
        "Payment Method": "CI - Installment Contract :: PaymentMethodDomain",
        "Good Type": "CI - Installment Contract :: GoodTypeDomain",
        "New/Used Code": "CI - Installment Contract :: NewUsedDomain",
        "Reorganized Credit Code": "CI - Installment Contract :: ReorganizedCreditDomain",
        "Overdue Days": "CI - Installment Contract :: OverdueDaysDomain",
        "Installment Type": "CI - Installment Contract :: InstallmentTypeDomain",
    },
    "CN": {
        "Role": "CI - Installment Contract :: RoleDomain",
        "Contract Type": "CN - Non-Installment :: ContractTypeDomain (CorrectedFull)",
        "Contract Phase": "CI - Installment Contract :: ContractPhaseDomain",
        "Contract Status": "CN - Non-Installment :: ContractStatusDomain",
        "Currency": "ID - Individual :: CurrencyDomain",
        "Original Currency": "ID - Individual :: CurrencyDomain",
        "Transaction Type / Sub-facility": "CI - Installment Contract :: TransactionTypeDomain",
        "Payment Periodicity": "CI - Installment Contract :: PaymentPeriodicityDomain",
        "Payment Method": "CI - Installment Contract :: PaymentMethodDomain",
        "Purpose of credit": "CN - Non-Installment :: CreditPurposeDomain",
        "Guarantee Type": "CN - Non-Installment :: GuaranteesDomain",
        "Customer Type": "CN - Non-Installment :: GuaranteeCustomerTypeDomain",
    },
    "CC": {
        "Role": "CI - Installment Contract :: RoleDomain",
        "Contract Type": "CC- Credit Card :: ContractTypeDomain",
        "Contract Phase": "CI - Installment Contract :: ContractPhaseDomain",
        "Contract Status": "CC- Credit Card :: ContractStatusDomain",
        "Currency": "ID - Individual :: CurrencyDomain",
        "Original Currency": "ID - Individual :: CurrencyDomain",
        "Transaction Type / Sub-facility": "CI - Installment Contract :: TransactionTypeDomain",
        "Payment Periodicity": "CI - Installment Contract :: PaymentPeriodicityDomain",
        "Payment Method": "CI - Installment Contract :: PaymentMethodDomain",
        "Installment Type": "CI - Installment Contract :: InstallmentTypeDomain",
        "Premium Card": "CC- Credit Card :: CardPremiumDomain",
        "Guarantee Type": "CN - Non-Installment :: GuaranteesDomain",
        "Customer Type": "CN - Non-Installment :: GuaranteeCustomerTypeDomain",
    },
    "CS": {
        "Role": "CI - Installment Contract :: RoleDomain",
        "Contract Type": "UT- Utilities :: ContractTypeDomain",
        "Contract Phase": "CI - Installment Contract :: ContractPhaseDomain",
        "Contract Status": "UT- Utilities :: ContractStatusDomain",
        "Currency": "ID - Individual :: CurrencyDomain",
        "Original Currency": "ID - Individual :: CurrencyDomain",
        "Payment Periodicity": "CI - Installment Contract :: PaymentPeriodicityDomain",
        "Payment Method": "CI - Installment Contract :: PaymentMethodDomain",
        "Installment Type": "CI - Installment Contract :: InstallmentTypeDomain",
    },
    "NE": {
        "Event Status": "NE - Negative Events :: EventStatusDomain",
        "Event Code": "NE - Negative Events :: SubjectInfoTypeDomain",
    },
    "SL": {
        "Role of the Parent": "SL - Subject Link :: CompanyRoleDomain",
    },
    "HD": {},
    "FT": {},
}

# Generic domain names that apply to any record type when not overridden above.
FALLBACK_DOMAINS = {
    "Currency": "ID - Individual :: CurrencyDomain",
    "Original Currency": "ID - Individual :: CurrencyDomain",
    "Contact Type": "ID - Individual :: ContactTypeDomain",
    "Identification Type": "ID - Individual :: IdentificationTypeDomain",
    "ID Type": "ID - Individual :: IDTypeDomain",
    "House Owner/Lessee": "ID - Individual :: HouseOwnerLesseeType",
}

# ---------------------------------------------------------------------------
# Mandatory flags (updated reference §3)
# ---------------------------------------------------------------------------

UNCONDITIONAL_MANDATORY = {
    "HD": [
        "Provider Code",
        "File Reference Date",
        "Version",
        "Submission Type",
    ],
    "ID": [
        "Provider Code",
        "Subject Reference Date",
        "Provider Subject No",
        "First Name",
        "Last Name",
        "Gender",
        "Date of Birth",
        "Civil Status",
        "Address 1: Address Type",
        "Address 2: Address Type",
        "Contact 1: Type",
    ],
    "BD": [
        "Provider Code",
        "Subject Reference Date",
        "Provider Subject No",
        "Trade Name",
        "Address 1: Address Type",
        "Identification 1: Type",
        "Contact 1: Type",
    ],
    "CI": [
        "Provider Code",
        "Contract Reference Date",
        "Provider Subject No",
        "Provider Contract No",
        "Role",
        "Contract Type",
        "Contract Phase",
        "Currency",
        "Original Currency",
        "Financed Amount",
        "Installments Number",
        "Payment Periodicity",
    ],
    "CN": [
        "Provider Code",
        "Contract Reference Date",
        "Provider Subject No",
        "Provider Contract No",
        "Role",
        "Contract Type",
        "Contract Phase",
        "Currency",
        "Original Currency",
        "Credit Limit",
    ],
    "CC": [
        "Provider Code",
        "Contract Reference Date",
        "Provider Subject No",
        "Provider Contract No",
        "Role",
        "Contract Type",
        "Contract Phase",
        "Currency",
        "Original Currency",
        "Credit limit",
        "Outstanding Balance - Unbilled",
        "Payment Periodicity",
    ],
    "CS": [
        "Provider Code",
        "Contract Reference Date",
        "Provider Subject No",
        "Provider Contract No",
        "Role",
        "Contract Type",
        "Contract Phase",
        "Currency",
        "Original Currency",
        "Payment Periodicity",
        "Billed Amount",
        "Outstanding Balance",
        "Overdue Payments Number",
        "Overdue Payments Amount",
        "Overdue Days",
    ],
    "NE": [
        "Provider Code",
        "Negative Event Reference Date",
        "Provider Subject No",
        "Event Code",
    ],
    "SL": [
        "Provider Code",
        "Subject Link Reference Date",
        "Provider Subject No (Parent)",
        "Role of the Parent",
        "Provider Subject No (Child)",
    ],
    "FT": [
        "Provider Code",
        "File Reference Date",
        "No. of records",
    ],
}

# ---------------------------------------------------------------------------
# Conditional mandatory flags (updated reference §4)
# ---------------------------------------------------------------------------

CONDITIONAL_MANDATORY = {
    "CI": [
        {
            "field": "Last Payment Amount",
            "condition": {"field": "Contract Phase", "values": ["AC", "CL", "CA"]},
        },
        {
            "field": "Overdue Payments Number",
            "condition": {"field": "Contract Phase", "values": ["AC", "CL", "CA"]},
        },
        {
            "field": "Overdue Payments Amount",
            "condition": {"field": "Contract Phase", "values": ["AC", "CL", "CA"]},
        },
        {
            "field": "Overdue Days",
            "condition": {"field": "Contract Phase", "values": ["AC", "CL", "CA"]},
        },
        {
            "field": "Utilisation / Outstanding Balance",
            "condition": {"field": "Contract Phase", "values": ["AC", "CL", "CA"]},
        },
        {
            "field": "Next Payment / Minimum Payment Due",
            "condition": {"field": "Contract Phase", "values": ["AC"]},
        },
        {
            "field": "Contract End Actual Date",
            "condition": {"field": "Contract Phase", "values": ["CL", "CA"]},
        },
        {
            "field": "Monthly Payment Amount",
            "condition": {"field": "Contract Phase", "values": ["AC", "CL", "CA"]},
        },
    ],
    "CC": [
        {
            "field": "Outstanding Balance",
            "condition": {"field": "Contract Phase", "values": ["AC"]},
        },
    ],
}

# ---------------------------------------------------------------------------
# Data type / max-length helpers
# ---------------------------------------------------------------------------

DATE_FIELDS = {
    "File Reference Date",
    "Subject Reference Date",
    "Date of Birth",
    "Contract Reference Date",
    "Contract Start Date",
    "Contract Request Date",
    "Contract End Planned Date",
    "Contract End Actual Date",
    "Last Payment Date",
    "First Payment Date",
    "Next Payment Date",
    "Last Charge Date",
    "Cancellation Date",
    "Validity Start Date",
    "Validity End Date",
    "Event Date",
    "Event Status Date",
    "Subject Link Reference Date",
    "Negative Event Reference Date",
    "Address 1: Occupied Since",
    "Address 2: Occupied Since",
    "Sole Trader 1: Occupied Since",
    "Sole Trader 2: Occupied Since",
    "ID 1: IssueDate",
    "ID 2: IssueDate",
    "ID 3: IssueDate",
    "ID 1: ExpiryDate",
    "ID 2: ExpiryDate",
    "ID 3: ExpiryDate",
    "Employment: DateHiredFrom",
    "Employment: DateHiredTo",
    "Term of Existence",
    "Registration Date",
    "Manufacturing Date",
}

YES_NO_FIELDS = {
    "Resident",
    "Board Resolution Flag",
    "Flag Card Used",
    "Min Payment Indicator",
    "Holder Liability",
}

LENGTH_OVERRIDES = {
    "Provider Subject No": 38,
    "Provider Contract No": 38,
    "Provider Code": 8,
    "Provider Subject No (Parent)": 38,
    "Provider Subject No (Child)": 38,
    "Provider Subject No (Guarantor 1)": 38,
    "Provider Subject No (Guarantor 2)": 38,
    "Provider Subject No (Guarantor 3)": 38,
    "Provider Subject No (Guarantor 4)": 38,
    "Provider Subject No (Guarantor 5)": 38,
    "Provider Subject No (Guarantor 6)": 38,
    "Provider Subject No (Linked Subject 1)": 38,
    "Provider Subject No (Linked Subject 2)": 38,
    "Provider Subject No (Linked Subject 3)": 38,
    "Provider Subject No (Linked Subject 4)": 38,
    "Provider Subject No (Linked Subject 5)": 38,
    "Provider Subject No (Linked Subject 6)": 38,
    "Provider Guarantee No 1": 38,
    "Provider Guarantee No 2": 38,
    "Provider Guarantee No 3": 38,
    "Provider Guarantee No 4": 38,
    "Provider Guarantee No 5": 38,
    "Provider Guarantee No 6": 38,
    "FullAddress": 400,
    "Sole Trader 1: FullAddress": 400,
    "Sole Trader 2: FullAddress": 400,
    "StreetNo": 100,
    "Sole Trader 1: StreetNo": 100,
    "Sole Trader 2: StreetNo": 100,
    "Subdivision": 100,
    "Sole Trader 1: Subdivision": 100,
    "Sole Trader 2: Subdivision": 100,
    "Barangay": 60,
    "Sole Trader 1: Barangay": 60,
    "Sole Trader 2: Barangay": 60,
    "City": 50,
    "Sole Trader 1: City": 50,
    "Sole Trader 2: City": 50,
    "Province": 50,
    "Sole Trader 1: Province": 50,
    "Sole Trader 2: Province": 50,
    "PostalCode": 4,
    "Sole Trader 1: PostalCode": 4,
    "Sole Trader 2: PostalCode": 4,
    "First Name": 70,
    "Last Name": 70,
    "Middle Name": 70,
    "Suffix": 70,
    "Spouse First Name": 70,
    "Spouse Last Name": 70,
    "Spouse Middle Name": 70,
    "Mother's Maiden First Name": 70,
    "Mother's Maiden Last Name": 70,
    "Mother's Maiden Middle Name": 70,
    "Father First Name": 70,
    "Father Last Name": 70,
    "Father Middle Name": 70,
    "Father Suffix": 40,
    "Nickname": 40,
    "Previous Last Name": 70,
    "Place of Birth": 100,
    "Country of Birth (Code)": 2,
    "Nationality": 2,
    "Address 1: Country": 2,
    "Address 2: Country": 2,
    "Sole Trader 1: Country": 2,
    "Sole Trader 2: Country": 2,
    "Identification 1: Number": 20,
    "Identification 2: Number": 20,
    "Identification 3: Number": 20,
    "Sole Trader 1: Identification Number": 20,
    "Sole Trader 2: Identification Number": 20,
    "ID 1: Number": 40,
    "ID 2: Number": 40,
    "ID 3: Number": 40,
    "ID 1: Issued By": 250,
    "ID 2: Issued By": 250,
    "ID 3: Issued By": 250,
    "Contact 1: Value": 100,
    "Contact 2: Value": 100,
    "Sole Trader 1: Contact Value": 100,
    "Sole Trader 2: Contact Value": 100,
    "Phone Number": 100,
    "Employment: Phone Number": 100,
    "Trade Name": 120,
    "Official Registered Trade Name": 120,
    "Sole Trader: TradeName": 120,
    "Employment: Trade Name": 120,
    "Number of Dependents": 2,
    "Car/s Owned": 3,
    "Number of Employees": 9,
    "Gross Income / Annual Turnover": 15,
    "Net Taxable Income": 15,
    "Monthly Expenses": 15,
    "Employment: GrossIncome": 15,
    "Financed Amount": 15,
    "Credit Limit": 15,
    "Credit limit": 15,
    "Outstanding Balance": 15,
    "Outstanding Balance - Unbilled": 15,
    "Overdue Payments Amount": 15,
    "Overdue Payments Number": 15,
    "Billed Amount": 15,
    "Monthly Payment Amount": 15,
    "Last payment amount": 15,
    "Next Payment / Minimum Payment Due": 15,
    "Guaranteed Amount 1": 15,
    "Guaranteed Amount 2": 15,
    "Guaranteed Amount 3": 15,
    "Guaranteed Amount 4": 15,
    "Guaranteed Amount 5": 15,
    "Guaranteed Amount 6": 15,
    "Good Value": 15,
    "Asset Appraised Value 1": 15,
    "Asset Appraised Value 2": 15,
    "Asset Appraised Value 3": 15,
    "Asset Appraised Value 4": 15,
    "Asset Appraised Value 5": 15,
    "Asset Appraised Value 6": 15,
    "Installments Number": 3,
    "Overdue Days": 1,
    "Payment Periodicity": 1,
    "Payment Method": 3,
    "Contract Type": 2,
    "Transaction Type / Sub-facility": 2,
    "Event Code": 1,
    "Event Status": 2,
    "Role": 1,
    "Role of the Parent": 1,
    "Company Role": 1,
    "Title": 2,
    "Gender": 1,
    "Civil Status": 1,
    "Resident": 1,
    "Legal Form": 2,
    "Firm Size": 1,
    "Address Type": 2,
    "House Owner/Lessee": 1,
    "Identification Type": 2,
    "ID Type": 2,
    "Contact Type": 1,
    "PSIC": 4,
    "Occupation": 4,
    "OccupationStatus": 1,
    "Annual/Monthly Indicator": 1,
    "Currency": 3,
    "Original Currency": 3,
    "Reorganized Credit Code": 1,
    "New/Used Code": 1,
    "Installment Type": 1,
    "Good Type": 2,
    "CardPremium": 1,
    "Premium Card": 1,
    "Guarantee Type": 3,
    "Customer Type": 1,
    "SubjectInfoType": 1,
    "CompanyRole": 1,
    "Branch Code": 3,
    "Version": 3,
    "Submission Type": 1,
    "Provider Comments": 100,
    "No. of records": 15,
    "Event Detail": 100,
    "Services/ Lines Number": 10,
    "Holder Liability": 1,
    "Min Payment Percentage": 5,
    "Times Card Used": 10,
    "Flag Card Used": 1,
    "Min Payment Indicator": 1,
    "Charged / Purchases Amount": 15,
    "Manufacturing Date": 8,
    "Registration Number": 20,
    "Asset Code": 20,
    "Asset Description": 100,
    "Asset Location": 100,
    "Asset Registry External Link": 100,
    "Provider Application No": 38,
    "CIC Contract Code": 38,
    "CIC Subject Code": 38,
    "Function Code": 10,
    "Message ID": 38,
    "Enquiry Code": 10,
    "Service Code": 10,
    "Output Type": 1,
    "Cancellation Flag": 1,
    "Flag To Be Merged": 1,
}


def infer_max_length(field_name: str) -> int | None:
    # Strip leading block prefix for grouped fields
    base = field_name
    for prefix in [
        "Address 1: ", "Address 2: ", "Sole Trader 1: ", "Sole Trader 2: ",
        "Identification 1: ", "Identification 2: ", "Identification 3: ",
        "Sole Trader 1: ", "Sole Trader 2: ",
        "ID 1: ", "ID 2: ", "ID 3: ",
        "Contact 1: ", "Contact 2: ",
    ]:
        if base.startswith(prefix):
            base = base[len(prefix):]
            break
    if base in LENGTH_OVERRIDES:
        return LENGTH_OVERRIDES[base]
    return None


def _is_numeric_field(field_name: str) -> bool:
    """Return True for fields that must contain only digits (no decimals/dashes)."""
    lower = field_name.lower()
    if "contact" in lower or "phone" in lower:
        return False
    if "id " in lower and "number" in lower:
        return False
    if "identification" in lower and "number" in lower:
        return False
    if "postalcode" in lower:
        return False
    if "providersubjectno" in re.sub(r"[^a-z0-9]", "", lower):
        return False
    if "providercontractno" in re.sub(r"[^a-z0-9]", "", lower):
        return False
    if "amount" in lower or "income" in lower or "balance" in lower or "limit" in lower or "billed" in lower:
        return True
    if "number" in lower:
        return True
    if "payment" in lower and "periodicity" not in lower:
        return True
    if "value" in lower and "good" in lower:
        return True
    if "appraised value" in lower or "guaranteed amount" in lower:
        return True
    if "holder liability" in lower:
        return True
    return False


def infer_data_type(field_name: str, domain: str | None) -> str:
    if field_name in DATE_FIELDS:
        return "date"
    if field_name in YES_NO_FIELDS:
        return "yesno"
    if domain:
        return "domain"
    if _is_numeric_field(field_name):
        return "numeric"
    return "string"


def annotate() -> dict:
    with SCHEMA_PATH.open("r", encoding="utf-8") as f:
        schema = json.load(f)

    for rt, spec in schema.items():
        mandatory_set = {normalize(n) for n in UNCONDITIONAL_MANDATORY.get(rt, [])}
        conditional_map = {
            normalize(item["field"]): item["condition"]
            for item in CONDITIONAL_MANDATORY.get(rt, [])
        }

        for field in spec["fields"]:
            name = field["name"]
            norm = normalize(name)

            # Domain lookup
            domain = None
            for fragment in [name, name.split(": ")[-1], name.split(" 1: ")[-1], name.split(" 2: ")[-1], name.split(" 3: ")[-1]]:
                if fragment in DOMAIN_MAP.get(rt, {}):
                    domain = DOMAIN_MAP[rt][fragment]
                    break
                if fragment in FALLBACK_DOMAINS:
                    domain = FALLBACK_DOMAINS[fragment]
                    break
            field["domain"] = domain

            # Data type
            field["data_type"] = infer_data_type(name, domain)
            field["max_length"] = infer_max_length(name)

            # Mandatory
            if norm in mandatory_set:
                field["mandatory"] = True
                field["mandatory_type"] = "unconditional"
                field["mandatory_condition"] = None
            elif norm in conditional_map:
                field["mandatory"] = True
                field["mandatory_type"] = "conditional"
                field["mandatory_condition"] = conditional_map[norm]
            else:
                field["mandatory"] = False
                field["mandatory_type"] = None
                field["mandatory_condition"] = None

            # Block / group metadata used by business-rule validators
            field["block"] = None
            field["block_index"] = None
            field["address_group"] = None
            if name.startswith("Address 1:"):
                field["address_group"] = "address1"
            elif name.startswith("Address 2:"):
                field["address_group"] = "address2"
            elif name.startswith("Sole Trader 1:"):
                field["address_group"] = "sole_trader1"
            elif name.startswith("Sole Trader 2:"):
                field["address_group"] = "sole_trader2"
            elif re.match(r"Identification [123]:", name):
                field["block"] = "identification"
                field["block_index"] = int(re.search(r"Identification (\d):", name).group(1))
            elif re.match(r"ID [123]:", name):
                field["block"] = "id"
                field["block_index"] = int(re.search(r"ID (\d):", name).group(1))
            elif re.match(r"Contact [12]:", name):
                field["block"] = "contact"
                field["block_index"] = int(re.search(r"Contact (\d):", name).group(1))
            elif re.match(r"Sole Trader [12]:", name):
                if "Identification" in name:
                    field["block"] = "sole_trader_identification"
                    field["block_index"] = int(re.search(r"Sole Trader (\d):", name).group(1))
                elif "Contact" in name:
                    field["block"] = "sole_trader_contact"
                    field["block_index"] = int(re.search(r"Sole Trader (\d):", name).group(1))
                else:
                    field["block"] = "sole_trader_address"
                    field["block_index"] = int(re.search(r"Sole Trader (\d):", name).group(1))
            elif re.match(r"Provider Guarantee No \d", name):
                field["block"] = "guarantee"
                field["block_index"] = int(re.search(r"Provider Guarantee No (\d)", name).group(1))
            elif re.match(r"Provider Subject No \(Linked Subject \d\)", name):
                field["block"] = "linked_subject"
                field["block_index"] = int(re.search(r"Linked Subject (\d)", name).group(1))
            elif re.match(r"Provider Subject No \(Guarantor \d\)", name) or re.match(r"Guarantor Name \d", name) or re.match(r"Guaranteed Amount \d", name):
                field["block"] = "guarantee"
                m = re.search(r"(\d)", name)
                field["block_index"] = int(m.group(1)) if m else None

    # Add group rules for address completeness and other business rules.
    group_rules = build_group_rules()
    for rt, rules in group_rules.items():
        schema[rt]["group_rules"] = rules

    return schema


def build_group_rules() -> dict:
    """Return group/completeness rules keyed by record type."""
    rules = {}

    # ID addresses
    rules["ID"] = [
        {
            "rule_type": "address_completeness",
            "address_group": "address1",
            "message": "Either FullAddress or (StreetNo + City + Province) must be filled for Address 1",
            "error_code": "2-139",
            "alternatives": [
                ["Address 1: FullAddress"],
                ["Address 1: StreetNo", "Address 1: City", "Address 1: Province"],
            ],
        },
        {
            "rule_type": "address_type_if_any",
            "address_groups": ["address1", "address2"],
            "message": "If any address field is supplied, the corresponding Address Type must be supplied",
            "error_code": "2-138",
        },
        {
            "rule_type": "paired_fields",
            "pairs": [
                ["Identification 1: Type", "Identification 1: Number"],
                ["Identification 2: Type", "Identification 2: Number"],
                ["Identification 3: Type", "Identification 3: Number"],
                ["ID 1: Type", "ID 1: Number"],
                ["ID 2: Type", "ID 2: Number"],
                ["ID 3: Type", "ID 3: Number"],
                ["Contact 1: Type", "Contact 1: Value"],
                ["Contact 2: Type", "Contact 2: Value"],
            ],
            "message": "Type and value fields must be both empty or both filled",
            "error_code": "1-069",
        },
        {
            "rule_type": "at_least_one_of",
            "fields": ["Contact 1: Type", "Contact 2: Type"],
            "message": "At least one Contact Type must be filled",
            "error_code": "2-104",
        },
    ]

    # BD addresses
    rules["BD"] = [
        {
            "rule_type": "address_completeness",
            "address_group": "address1",
            "message": "Either FullAddress or (Subdivision + City + Province) must be filled for Address 1",
            "error_code": "2-145",
            "alternatives": [
                ["Address 1: FullAddress"],
                ["Address 1: Subdivision", "Address 1: City", "Address 1: Province"],
            ],
        },
        {
            "rule_type": "address_completeness",
            "address_group": "address2",
            "message": "Either FullAddress or (Subdivision + City + Province) must be filled for Address 2",
            "error_code": "2-145",
            "alternatives": [
                ["Address 2: FullAddress"],
                ["Address 2: Subdivision", "Address 2: City", "Address 2: Province"],
            ],
        },
        {
            "rule_type": "address_type_if_any",
            "address_groups": ["address1", "address2"],
            "message": "If any address field is supplied, the corresponding Address Type must be supplied",
            "error_code": "2-138",
        },
        {
            "rule_type": "paired_fields",
            "pairs": [
                ["Identification 1: Type", "Identification 1: Number"],
                ["Identification 2: Type", "Identification 2: Number"],
                ["Contact 1: Type", "Contact 1: Value"],
                ["Contact 2: Type", "Contact 2: Value"],
            ],
            "message": "Type and value fields must be both empty or both filled",
            "error_code": "1-069",
        },
        {
            "rule_type": "at_least_one_of_values",
            "fields": ["Identification 1: Type", "Identification 2: Type"],
            "allowed_values": ["10"],
            "message": "At least one Identification Type must be TIN",
            "error_code": "2-130",
        },
    ]

    # Sole-trader address (within ID record)
    for parent_rt in ["ID"]:
        for idx, suffix in [(1, "Sole Trader 1:"), (2, "Sole Trader 2:")]:
            rules.setdefault(parent_rt, []).append(
                {
                    "rule_type": "address_completeness",
                    "address_group": f"sole_trader{idx}",
                    "message": f"Either FullAddress or (StreetNo + City + Province) must be filled for {suffix}",
                    "error_code": "2-141",
                    "alternatives": [
                        [f"{suffix} FullAddress"],
                        [f"{suffix} StreetNo", f"{suffix} City", f"{suffix} Province"],
                    ],
                }
            )

    # Guarantor conditional (if any guarantor block field is filled, Guarantor Subject No is required)
    for rt in ["CI", "CN", "CC"]:
        rules.setdefault(rt, []).append(
            {
                "rule_type": "guarantor_block",
                "message": "If a guarantor block is reported, Guarantor Subject No and Guaranteed Amount are required",
                "error_code": "20-294",
            }
        )

    return rules


def main() -> None:
    schema = annotate()
    with SCHEMA_PATH.open("w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2, ensure_ascii=False)
    print(f"Annotated schema written to {SCHEMA_PATH}")


if __name__ == "__main__":
    main()
