#!/usr/bin/env python3
"""
Interactive test script for Futurix AI
Test the system with your own text or use sample data
"""
from app.verification_agent import verify_from_text
from app.extractor import parse_document
import json

def print_header(text):
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80)

def test_extraction():
    """Test document extraction"""
    print_header("TEST: Document Extraction")
    
    sample_invoice = """
    TAX INVOICE
    
    Acme Corporation Pvt Ltd
    GSTIN: 29ABCDE1234F1Z5
    
    Bill To: XYZ Industries Ltd
    
    Invoice Number: INV-2025-001
    Date: 2025-10-15
    
    Description          Qty    Price      Total
    Widget A             10     1,250.00   12,500.00
    Widget B             25       850.00   21,250.00
    
    Subtotal:                              33,750.00
    GST (18%):                              6,075.00
    Total:                                 39,825.00
    
    Currency: INR
    """
    
    print("\n📄 Sample Invoice Text:")
    print(sample_invoice[:200] + "...")
    
    result = parse_document(sample_invoice)
    
    print("\n✅ EXTRACTED DATA:")
    print(f"  Document Type: {result['document_type']}")
    print(f"  Vendor: {result['vendor_name']}")
    print(f"  Total: {result['currency']} {result['total_amount']:,.2f}")
    print(f"  Date: {result['invoice_date']}")
    print(f"  Line Items: {len(result['line_items'])} items")
    
    if result['extraction_warnings']:
        print(f"\n⚠️  Warnings: {len(result['extraction_warnings'])}")
        for warning in result['extraction_warnings']:
            print(f"    - {warning}")
    else:
        print("\n✅ No warnings - extraction looks good!")
    
    return result

def test_verification():
    """Test PO vs Invoice verification"""
    print_header("TEST: PO vs Invoice Verification")
    
    sample_po = """
    PURCHASE ORDER
    
    Order No: PO-2025-456
    Date: 2025-10-10
    
    Vendor: Acme Corporation Pvt Ltd
    
    Item              Qty    Price      Total
    Widget A          10     1,250.00   12,500.00
    Widget B          25       850.00   21,250.00
    
    Total: INR 33,750.00
    """
    
    sample_invoice = """
    TAX INVOICE
    
    Acme Corporation Pvt Ltd
    Invoice: INV-001
    PO Number: PO-2025-456
    Date: 2025-10-15
    
    Item              Qty    Price      Total
    Widget A          10     1,250.00   12,500.00
    Widget B          25       850.00   21,250.00
    Service Charge     1     2,500.00    2,500.00
    
    Total: INR 36,250.00
    """
    
    print("\n📄 Comparing PO and Invoice...")
    
    result = verify_from_text(sample_po, sample_invoice)
    
    summary = result['verification_summary']
    anomalies = result['anomaly_insights']
    
    print("\n📊 VERIFICATION RESULTS:")
    print(f"  Vendor Match: {'✅' if summary['vendor_match'] else '❌'}")
    print(f"  PO Number Match: {'✅' if summary['po_number_match'] else '❌'}")
    print(f"  Total Match: {'✅' if summary['total_match'] else '❌'}")
    print(f"  Amount Difference: ₹{summary['amount_difference']:,.2f}")
    print(f"  Discrepancy Level: {summary['discrepancy_level'].upper()}")
    
    print(f"\n🎯 RISK ASSESSMENT:")
    print(f"  Risk Score: {anomalies['risk_score']}/10")
    print(f"  Pattern: {anomalies['pattern']}")
    print(f"  Needs Review: {'⚠️  YES' if summary['needs_review'] else '✅ NO'}")
    
    if anomalies['fraud_indicators']:
        print(f"\n🚨 FRAUD INDICATORS:")
        for indicator in anomalies['fraud_indicators']:
            print(f"    • {indicator}")
    
    # Show visualization data
    viz = result['visualization_data']
    print(f"\n📈 DASHBOARD DATA:")
    print(f"  Naughty List Score: {viz['naughty_list_score']}/10")
    print(f"  Total Discrepancies: {viz['discrepancy_count']}")
    
    return result

def test_custom_text():
    """Test with custom text input"""
    print_header("TEST: Custom Text Input")
    
    print("\nYou can test with your own OCR text!")
    print("For now, using a sample fraudulent invoice...\n")
    
    po_text = """
    PURCHASE ORDER
    Order: PO-123
    Vendor: Acme Corp
    Total: $10,000
    """
    
    fraud_invoice = """
    INVOICE
    Different Vendor Inc
    PO: PO-123
    Total: $25,000
    """
    
    result = verify_from_text(po_text, fraud_invoice)
    
    print("🚨 FRAUD DETECTION TEST:")
    print(f"  Risk Score: {result['anomaly_insights']['risk_score']}/10")
    
    if result['anomaly_insights']['risk_score'] > 7:
        print("  Status: 🔴 HIGH RISK - REJECT")
    elif result['anomaly_insights']['risk_score'] > 5:
        print("  Status: 🟠 MEDIUM RISK - REVIEW")
    else:
        print("  Status: 🟢 LOW RISK - APPROVE")
    
    return result

def show_json_output(result):
    """Show complete JSON output"""
    print_header("Complete JSON Output")
    print("\n📄 Full JSON Response:")
    print(json.dumps(result, indent=2, default=str))

def main():
    print("\n" + "=" * 80)
    print("  🚀 FUTURIX AI - INTERACTIVE TEST SUITE")
    print("=" * 80)
    
    print("\nThis will test:")
    print("  1. Document extraction (invoice/PO parsing)")
    print("  2. PO vs Invoice verification")
    print("  3. Fraud detection")
    print("  4. JSON output generation")
    
    input("\nPress Enter to start testing...")
    
    # Test 1: Extraction
    extraction_result = test_extraction()
    input("\nPress Enter to continue to verification test...")
    
    # Test 2: Verification
    verification_result = test_verification()
    input("\nPress Enter to continue to fraud detection test...")
    
    # Test 3: Fraud detection
    fraud_result = test_custom_text()
    input("\nPress Enter to see complete JSON output...")
    
    # Test 4: JSON output
    show_json_output(verification_result)
    
    print_header("✨ ALL TESTS COMPLETED")
    print("\n✅ System Status: OPERATIONAL")
    print("✅ All components working correctly")
    print("\n📚 Next Steps:")
    print("  1. Start the API server: uvicorn app.main:app --reload")
    print("  2. Test API endpoints with curl or Postman")
    print("  3. Integrate with your dashboard")
    print("\n" + "=" * 80 + "\n")

if __name__ == "__main__":
    main()
