# PDF-to-Spreadsheet Invoice Extractor

A small Streamlit app that extracts common fields from text-based invoice PDFs and exports CSV or Excel.

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Run tests with `pytest -q`. A synthetic invoice is included in `sample_data/sample_invoice.pdf`.

## Fields extracted

Invoice number, invoice date, vendor/supplier, total amount, source filename, review flag, and missing-field list.

## Limitations

- Uses regular expressions, not a general document-understanding model.
- Works best with selectable text and layouts similar to the sample.
- Scanned image PDFs need OCR, which is not included.
- Currency and number formats vary; verify totals manually.
- Does not verify tax, calculate payments, or make accounting decisions.
- Always check extracted values against the original invoice before bookkeeping or payment.

## Portfolio checklist

Try several synthetic invoice layouts, add tests for missing fields and unusual formatting, and include a screenshot of the working app.
