#!/usr/bin/env python3
"""
Test script for the enhanced extractor
"""
from app.extractor import parse_document, validate_po_invoice_match
import json

# Sample invoice OCR text
sample_invoice = """
TAX INVOICE

Acme Corporation Pvt Ltd
GSTIN: 29ABCDE1234F1Z5
123 Business Park, Mumbai
Phone: +91-22-12345678

Bill To:
XYZ Industries Ltd
GSTIN: 27XYZAB5678G2W4
456 Industrial Area, Delhi

Invoice Number: INV-2025-001
PO Number: PO-2025-456
Invoice Date: 2025-10-15
Due Date: 2025-11-15

Description                    SKU        Qty    Unit Price    Total
Widget A Premium              W-A-01      10     1,250.00     12,500.00
Widget B Standard             W-B-02      25       850.00     21,250.00
Service Charge                SVC-01       1     2,500.00      2,500.00

                                          Subtotal:    36,250.00
                                          GST (18%):    6,525.00
                                          Grand Total: 42,775.00

Currency: INR

Terms & Conditions:
Payment due within 30 days.
Thank you for your business!

Authorized Signatory
"""

# Sample PO OCR text
sample_po = """
PURCHASE ORDER

XYZ Industries Ltd
Order No: PO-2025-456
Order Date: 2025-10-10

Vendor:
Acme Corporation Pvt Ltd
GSTIN: 29ABCDE1234F1Z5

Item                          Qty    Unit Price    Total
Widget A Premium              10     1,250.00     12,500.00
Widget B Standard             25       850.00     21,250.00

Subtotal:                                         33,750.00
Tax (18%):                                         6,075.00
Total Amount:                                     39,825.00

Currency: INR
"""

def test_invoice_extraction():
    print("=" * 80)
    print("TESTING INVOICE EXTRACTION")
    print("=" * 80)
    
    result = parse_document(sample_invoice)
    
    print("\n📄 Extracted Invoice Data:")
    print(json.dumps(result, indent=2, default=str))
    
    print("\n⚠️  Extraction Warnings:")
    for warning in result.get("extraction_warnings", []):
        print(f"  - {warning}")
    
    print("\n🔍 Debug Info:")
    for key, value in result.get("extraction_debug", {}).items():
        print(f"  {key}: {value}")

def test_po_extraction():
    print("\n" + "=" * 80)
    print("TESTING PURCHASE ORDER EXTRACTION")
    print("=" * 80)
    
    result = parse_document(sample_po)
    
    print("\n📄 Extracted PO Data:")
    print(json.dumps(result, indent=2, default=str))

def test_validation():
    print("\n" + "=" * 80)
    print("TESTING PO vs INVOICE VALIDATION")
    print("=" * 80)
    
    po_data = parse_document(sample_po)
    invoice_data = parse_document(sample_invoice)
    
    validation_result = validate_po_invoice_match(po_data, invoice_data)
    
    print("\n✅ Validation Result:")
    print(f"  Matched: {validation_result['matched']}")
    print(f"  Match Method: {validation_result['match_method']}")
    print(f"  Match Score: {validation_result['match_score']:.2f}")
    print(f"  Total Discrepancies: {validation_result['discrepancy_count']}")
    print(f"  High Severity: {validation_result['high_severity_count']}")
    
    if validation_result['discrepancies']:
        print("\n⚠️  Discrepancies Found:")
        for disc in validation_result['discrepancies']:
            severity_icon = "🔴" if disc['severity'] == 'high' else "🟡" if disc['severity'] == 'medium' else "🟢"
            print(f"  {severity_icon} [{disc['type']}] {disc['message']}")

if __name__ == "__main__":
    test_invoice_extraction()
    test_po_extraction()
    test_validation()
    
    print("\n" + "=" * 80)
    print("✨ All tests completed!")
    print("=" * 80)
