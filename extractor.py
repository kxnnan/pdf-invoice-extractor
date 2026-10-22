from pathlib import Path
import re
import pandas as pd
from pypdf import PdfReader

PATTERNS = {
    "invoice_number": [r"(?:invoice\s*(?:number|no\.?|#))\s*[:\-]?\s*([A-Z0-9][A-Z0-9\-/]+)"],
    "invoice_date": [r"(?:invoice\s*date|date)\s*[:\-]?\s*(\d{4}-\d{2}-\d{2}|\d{1,2}[/-]\d{1,2}[/-]\d{2,4})"],
    "vendor": [r"(?:vendor|supplier|from)\s*[:\-]\s*(.+)"],
    "total": [r"(?:grand\s*total|total\s*due|amount\s*due|total)\s*[:\-]?\s*(?:USD\s*)?[$€£]?\s*([0-9,]+(?:\.[0-9]{2})?)"],
}

def extract_pdf_text(pdf_path):
    reader = PdfReader(str(pdf_path))
    return "\n".join(page.extract_text() or "" for page in reader.pages).strip()

def first_match(text, patterns):
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE)
        if match:
            return match.group(1).strip()
    return None

def extract_invoice_fields(text, source_file=""):
    values = {field: first_match(text, patterns) for field, patterns in PATTERNS.items()}
    if values["total"] is not None:
        try:
            values["total"] = float(values["total"].replace(",", ""))
        except ValueError:
            values["total"] = None
    missing = [field for field, value in values.items() if value is None]
    values["source_file"] = source_file
    values["needs_review"] = bool(missing)
    values["missing_fields"] = ", ".join(missing)
    return values

def extract_invoice(pdf_path):
    path = Path(pdf_path)
    text = extract_pdf_text(path)
    if not text:
        return {
            "invoice_number": None, "invoice_date": None, "vendor": None, "total": None,
            "source_file": path.name, "needs_review": True,
            "missing_fields": "invoice_number, invoice_date, vendor, total",
            "error": "No selectable text found. This may be a scanned PDF and need OCR."
        }
    return extract_invoice_fields(text, source_file=path.name)

def save_results(rows, output_path):
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(rows)
    if path.suffix.lower() == ".csv":
        df.to_csv(path, index=False)
    elif path.suffix.lower() == ".xlsx":
        df.to_excel(path, index=False)
    else:
        raise ValueError("Output filename must end in .csv or .xlsx.")
