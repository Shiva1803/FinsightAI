"""
Test to verify that uploading the same document twice should show no discrepancies
"""
from app.verification_agent import verify_from_text

# Sample invoice text
sample_invoice = """
INVOICE

ABC Corporation
123 Business St
Tax ID: 12-3456789

Bill To:
XYZ Company
456 Client Ave
Tax ID: 98-7654321

Invoice Number: INV-2024-001
Date: January 15, 2024
PO Number: PO-2024-100

Items:
Description          Qty    Unit Price    Total
Widget A             10     $100.00       $1,000.00
Widget B             5      $200.00       $1,000.00

Subtotal:                                 $2,000.00
Tax (10%):                                $200.00
Total:                                    $2,200.00
"""

print("Testing: Same document uploaded as both PO and Invoice")
print("=" * 60)

# Verify the same document against itself
result = verify_from_text(
    po_text=sample_invoice,
    invoice_text=sample_invoice,
    po_filename="test_doc.pdf",
    invoice_filename="test_doc.pdf"
)

print("\nVerification Summary:")
print(f"  Vendor Match: {result['verification_summary']['vendor_match']}")
print(f"  Total Match: {result['verification_summary']['total_match']}")
print(f"  Amount Difference: ${result['verification_summary']['amount_difference']}")
print(f"  Discrepancy Level: {result['verification_summary']['discrepancy_level']}")
print(f"  Needs Review: {result['verification_summary']['needs_review']}")

print("\nAnomaly Insights:")
print(f"  Anomaly Detected: {result['anomaly_insights']['anomaly_detected']}")
print(f"  Risk Score: {result['anomaly_insights']['risk_score']}/10")
print(f"  Pattern: {result['anomaly_insights']['pattern']}")

print("\nDiscrepancies Found:")
if result['verification_summary']['discrepancy_level'] != 'none':
    print("  ⚠️  ISSUE: Same document shows discrepancies!")
    print(f"  This should not happen when comparing identical documents.")
else:
    print("  ✅ PASS: No discrepancies found (as expected)")

print("\n" + "=" * 60)
