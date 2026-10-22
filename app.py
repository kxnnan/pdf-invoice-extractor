from io import BytesIO
from pathlib import Path
import tempfile
import pandas as pd
import streamlit as st
from extractor import extract_invoice

st.set_page_config(page_title="PDF Invoice Extractor", page_icon="📄", layout="wide")
st.title("PDF-to-Spreadsheet Extractor")
st.write("Extract common fields from text-based invoice PDFs. Review every result before using it for accounting or payment.")
uploads = st.file_uploader("Upload invoice PDFs", type=["pdf"], accept_multiple_files=True)

def make_excel(df):
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    return buffer.getvalue()

if uploads:
    rows = []
    with tempfile.TemporaryDirectory() as folder:
        for upload in uploads:
            path = Path(folder) / upload.name
            path.write_bytes(upload.getvalue())
            try:
                rows.append(extract_invoice(path))
            except Exception as exc:
                rows.append({
                    "invoice_number": None, "invoice_date": None, "vendor": None, "total": None,
                    "source_file": upload.name, "needs_review": True,
                    "missing_fields": "all fields", "error": str(exc)
                })
    result = pd.DataFrame(rows)
    st.subheader("Extracted fields")
    st.dataframe(result, use_container_width=True, hide_index=True)
    st.warning("Check all values against the original PDF. This tool does not verify invoices.")
    st.download_button("Download CSV", result.to_csv(index=False).encode(), "invoice_extraction.csv", "text/csv")
    st.download_button("Download Excel", make_excel(result), "invoice_extraction.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
else:
    st.info("Try the synthetic sample invoice at sample_data/sample_invoice.pdf.")
