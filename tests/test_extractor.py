from extractor import extract_invoice_fields

def test_extracts_common_invoice_fields():
    text = (
        "ACME OFFICE SUPPLIES\n"
        "Invoice Number: INV-2041\n"
        "Invoice Date: 2026-03-18\n"
        "Vendor: Acme Office Supplies\n"
        "Total Due: $1,245.50\n"
    )
    result = extract_invoice_fields(text, source_file="sample.pdf")
    assert result["invoice_number"] == "INV-2041"
    assert result["invoice_date"] == "2026-03-18"
    assert result["vendor"] == "Acme Office Supplies"
    assert result["total"] == 1245.50
    assert result["needs_review"] is False

def test_missing_fields_are_flagged():
    result = extract_invoice_fields("Invoice Number: INV-1")
    assert result["needs_review"] is True
    assert "total" in result["missing_fields"]
