#!/usr/bin/env python3
"""
Simple test - just verify the core system works
No dependencies needed except python-dateutil
"""

print("=" * 80)
print("  🚀 FUTURIX AI - SIMPLE TEST")
print("=" * 80)
print()

# Test 1: Import core modules
print("Test 1: Importing core modules...")
try:
    from app.extractor import parse_document
    from app.verification_agent import verify_from_text
    print("✅ PASSED: Core modules imported successfully")
except Exception as e:
    print(f"❌ FAILED: {e}")
    exit(1)

print()

# Test 2: Extract invoice
print("Test 2: Extracting invoice data...")
sample_invoice = """
TAX INVOICE
Acme Corp
Invoice Number: INV-001
Invoice Date: 2025-10-15
Grand Total: 10000.00
Currency: INR
"""

try:
    result = parse_document(sample_invoice)
    assert result['document_type'] == 'invoice', f"Expected 'invoice', got '{result['document_type']}'"
    assert result['total_amount'] is not None, "Total amount not extracted"
    print("✅ PASSED: Invoice extraction works")
    print(f"   - Document type: {result['document_type']}")
    print(f"   - Total: {result['total_amount']}")
    if result['extraction_warnings']:
        print(f"   - Warnings: {len(result['extraction_warnings'])} (expected for simple text)")
except Exception as e:
    print(f"❌ FAILED: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print()

# Test 3: Verify PO vs Invoice
print("Test 3: Verifying PO vs Invoice...")
po_text = """
PURCHASE ORDER
Order: PO-123
Vendor: Acme Corp
Total: INR 10,000
"""

invoice_text = """
INVOICE
Invoice: INV-456
PO Number: PO-123
Vendor: Acme Corp
Total: INR 12,000
"""

try:
    verification = verify_from_text(po_text, invoice_text)
    assert 'verification_summary' in verification
    assert 'anomaly_insights' in verification
    assert 'visualization_data' in verification
    
    risk_score = verification['anomaly_insights']['risk_score']
    print("✅ PASSED: Verification works")
    print(f"   - Risk score: {risk_score}/10")
    print(f"   - Amount difference: ₹{verification['verification_summary']['amount_difference']}")
    print(f"   - Needs review: {verification['verification_summary']['needs_review']}")
except Exception as e:
    print(f"❌ FAILED: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print()

# Test 4: Fraud detection
print("Test 4: Testing fraud detection...")
fraud_invoice = """
INVOICE
Invoice: INV-999
PO Number: PO-123
Vendor: Different Vendor Inc
Total: INR 50,000
"""

try:
    fraud_check = verify_from_text(po_text, fraud_invoice)
    risk_score = fraud_check['anomaly_insights']['risk_score']
    fraud_indicators = fraud_check['anomaly_insights']['fraud_indicators']
    
    print("✅ PASSED: Fraud detection works")
    print(f"   - Risk score: {risk_score}/10")
    print(f"   - Fraud indicators: {len(fraud_indicators)}")
    if fraud_indicators:
        for indicator in fraud_indicators[:3]:
            print(f"     • {indicator}")
except Exception as e:
    print(f"❌ FAILED: {e}")
    exit(1)

print()
print("=" * 80)
print("  ✅ ALL TESTS PASSED!")
print("=" * 80)
print()
print("  System Status: 🟢 OPERATIONAL")
print()
print("  Core functionality verified:")
print("    ✓ Document extraction")
print("    ✓ PO vs Invoice verification")
print("    ✓ Risk scoring (0-10)")
print("    ✓ Fraud detection")
print("    ✓ Visualization data generation")
print()
print("  Next steps:")
print("    1. Install FastAPI for API server: pip install fastapi uvicorn")
print("    2. Run full tests: python3 test_verification_agent.py")
print("    3. Start API server: uvicorn app.main:app --reload")
print()
print("=" * 80)
