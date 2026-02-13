import re
import pandas as pd
from ingestion.parser import extract_tables_with_page_info
from config.canonical_mapping import CANONICAL_LINE_ITEMS
from utils.currency_detector import detect_currency_and_unit
from extraction.confidence_engine import calculate_confidence


def normalize_label(label):
    for canonical, variations in CANONICAL_LINE_ITEMS.items():
        for variant in variations:
            if variant.lower() == label.lower():
                return canonical, True, False
            elif variant.lower() in label.lower():
                return canonical, False, True
    return None, False, False


def extract_numeric_values(row):
    pattern = r"\(?\d{1,3}(?:,\d{3})*(?:\.\d+)?\)?"
    values = re.findall(pattern, " ".join(row))
    cleaned = []

    for v in values:
        original = v
        v = v.replace(",", "")
        if "(" in v and ")" in v:
            v = "-" + v.replace("(", "").replace(")", "")
        try:
            cleaned.append(float(v))
        except:
            continue

    return cleaned


def extract_income_statement(file):
    tables = extract_tables_with_page_info(file)
    metadata_text = ""
    extracted_rows = []

    for entry in tables:
        page = entry["page"]
        table = entry["table"]

        for row in table:
            if not row or not row[0]:
                continue

            label = row[0]
            canonical, exact_match, synonym_match = normalize_label(label)

            if canonical:
                numbers = extract_numeric_values(row)
                confidence = calculate_confidence(
                    exact_match,
                    synonym_match,
                    len(numbers)
                )

                extracted_rows.append({
                    "Line Item": canonical,
                    "Original Label": label,
                    "Page Number": page,
                    "Values": numbers,
                    "Confidence": confidence
                })

    if not extracted_rows:
        return pd.DataFrame(), {}

    # Expand years dynamically
    max_years = max(len(row["Values"]) for row in extracted_rows)

    structured_data = []
    for row in extracted_rows:
        values = row["Values"] + [None] * (max_years - len(row["Values"]))
        structured_data.append(
            [row["Line Item"]] +
            values +
            [row["Original Label"], row["Page Number"], row["Confidence"]]
        )

    columns = (
        ["Line Item"] +
        [f"Year_{i+1}" for i in range(max_years)] +
        ["Original Label", "Page Number", "Confidence"]
    )

    df = pd.DataFrame(structured_data, columns=columns)

    return df, detect_currency_and_unit(metadata_text)
