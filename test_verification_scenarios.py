"""
Comprehensive test for different verification scenarios
"""
from app.verification_agent import verify_from_text

print("=" * 70)
print("FUTURIX AI - VERIFICATION LOGIC TESTS")
print("=" * 70)

# Test 1: Same document uploaded twice
print("\n📋 TEST 1: Same Document Uploaded Twice")
print("-" * 70)

same_doc = """
INVOICE
ABC Corporation
Invoice Number: INV-001
Date: 2024-01-15
Total: $1,000.00
"""

result1 = verify_from_text(same_doc, same_doc, "doc.pdf", "doc.pdf")
print(f"✓ Discrepancy Level: {result1['verification_summary']['discrepancy_level']}")
print(f"✓ Risk Score: {result1['anomaly_insights']['risk_score']}/10")
print(f"✓ Needs Review: {result1['verification_summary']['needs_review']}")
print(f"✓ Pattern: {result1['anomaly_insights']['pattern']}")
assert result1['verification_summary']['discrepancy_level'] == 'none', "FAIL: Should show no discrepancies"
assert result1['anomaly_insights']['risk_score'] == 0.0, "FAIL: Risk score should be 0"
assert result1['verification_summary']['needs_review'] == False, "FAIL: Should not need review"
print("✅ PASS: Same document correctly identified")

# Test 2: Matching PO and Invoice
print("\n📋 TEST 2: Matching PO and Invoice")
print("-" * 70)

po_doc = """
PURCHASE ORDER
ABC Corporation
PO Number: PO-001
Date: 2024-01-10
Total: $1,000.00
"""

invoice_doc = """
INVOICE
ABC Corporation
Invoice Number: INV-001
PO Number: PO-001
Date: 2024-01-15
Total: $1,000.00
"""

result2 = verify_from_text(po_doc, invoice_doc, "po.pdf", "invoice.pdf")
print(f"✓ Discrepancy Level: {result2['verification_summary']['discrepancy_level']}")
print(f"✓ Risk Score: {result2['anomaly_insights']['risk_score']}/10")
print(f"✓ Total Match: {result2['verification_summary']['total_match']}")
print(f"✓ Amount Difference: ${result2['verification_summary']['amount_difference']}")
assert result2['verification_summary']['total_match'] == True, "FAIL: Totals should match"
assert result2['verification_summary']['amount_difference'] == 0.0, "FAIL: No amount difference"
print("✅ PASS: Matching documents verified correctly")

# Test 3: Overbilling scenario
print("\n📋 TEST 3: Overbilling Detection")
print("-" * 70)

po_doc_low = """
PURCHASE ORDER
ABC Corporation
PO Number: PO-002
Date: 2024-01-10
Total: $1,000.00
"""

invoice_doc_high = """
INVOICE
ABC Corporation
Invoice Number: INV-002
PO Number: PO-002
Date: 2024-01-15
Total: $1,500.00
"""

result3 = verify_from_text(po_doc_low, invoice_doc_high, "po.pdf", "invoice.pdf")
print(f"✓ Discrepancy Level: {result3['verification_summary']['discrepancy_level']}")
print(f"✓ Risk Score: {result3['anomaly_insights']['risk_score']}/10")
print(f"✓ Amount Difference: ${result3['verification_summary']['amount_difference']}")
print(f"✓ Pattern: {result3['anomaly_insights']['pattern']}")
assert result3['verification_summary']['amount_difference'] == 500.0, "FAIL: Should detect $500 difference"
assert result3['anomaly_insights']['risk_score'] > 0, "FAIL: Should have risk score > 0"
print("✅ PASS: Overbilling detected correctly")

# Test 4: Small difference (within tolerance)
print("\n📋 TEST 4: Small Difference (Within Tolerance)")
print("-" * 70)

po_doc_1000 = """
PURCHASE ORDER
ABC Corporation
PO Number: PO-003
Date: 2024-01-10
Total: $1,000.00
"""

invoice_doc_1010 = """
INVOICE
ABC Corporation
Invoice Number: INV-003
PO Number: PO-003
Date: 2024-01-15
Total: $1,010.00
"""

result4 = verify_from_text(po_doc_1000, invoice_doc_1010, "po.pdf", "invoice.pdf")
print(f"✓ Discrepancy Level: {result4['verification_summary']['discrepancy_level']}")
print(f"✓ Risk Score: {result4['anomaly_insights']['risk_score']}/10")
print(f"✓ Amount Difference: ${result4['verification_summary']['amount_difference']}")
print(f"✓ Total Match: {result4['verification_summary']['total_match']}")
# $10 difference on $1000 is 1%, within 2% tolerance
assert result4['verification_summary']['total_match'] == True, "FAIL: Should match within tolerance"
print("✅ PASS: Small difference handled correctly")

print("\n" + "=" * 70)
print("ALL TESTS PASSED! ✅")
print("=" * 70)
print("\nSummary:")
print("  ✓ Same document detection works")
print("  ✓ Matching documents verified correctly")
print("  ✓ Overbilling detection works")
print("  ✓ Tolerance handling works")
print("\nThe verification logic is now working correctly!")
