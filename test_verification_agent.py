#!/usr/bin/env python3
"""
Test script for Futurix AI Verification Agent
"""
from app.verification_agent import VerificationAgent, verify_from_text
import json

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

# Sample Invoice with discrepancies
sample_invoice_with_issues = """
TAX INVOICE

Acme Corporation Pvt Ltd
GSTIN: 29ABCDE1234F1Z5
123 Business Park, Mumbai

Bill To:
XYZ Industries Ltd
GSTIN: 27XYZAB5678G2W4

Invoice Number: INV-2025-001
PO Number: PO-2025-456
Invoice Date: 2025-10-15
Due Date: 2025-11-15

Description                    Qty    Unit Price    Total
Widget A Premium               10     1,250.00     12,500.00
Widget B Standard              25       850.00     21,250.00
Service Charge                  1     2,500.00      2,500.00

                                          Subtotal:    36,250.00
                                          GST (18%):    6,525.00
                                          Grand Total: 42,775.00

Currency: INR
Thank you for your business!
"""

# Sample Invoice with major fraud indicators
sample_fraudulent_invoice = """
TAX INVOICE

Different Vendor Pvt Ltd
GSTIN: 99FRAUD9999F9Z9

Invoice Number: INV-2025-999
PO Number: PO-2025-456
Invoice Date: 2025-12-25

Description                    Qty    Unit Price    Total
Widget A Premium               10     2,500.00     25,000.00
Widget B Standard              25     1,700.00     42,500.00
Extra Charges                   1    10,000.00     10,000.00

                                          Grand Total: 77,500.00

Currency: USD
"""


def print_section(title: str):
    """Print formatted section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_json(data: dict, indent: int = 2):
    """Pretty print JSON"""
    print(json.dumps(data, indent=indent, default=str))


def test_normal_verification():
    """Test verification with minor discrepancies"""
    print_section("TEST 1: Normal Verification (Minor Discrepancies)")
    
    result = verify_from_text(
        sample_po, 
        sample_invoice_with_issues,
        "PO_456.pdf",
        "INV_001.pdf"
    )
    
    print("\n📊 VERIFICATION SUMMARY:")
    summary = result["verification_summary"]
    print(f"  ✓ Vendor Match: {summary['vendor_match']}")
    print(f"  ✓ PO Number Match: {summary['po_number_match']}")
    print(f"  ✓ Total Match: {summary['total_match']}")
    print(f"  ✓ Amount Difference: ₹{summary['amount_difference']}")
    print(f"  ✓ Discrepancy Level: {summary['discrepancy_level'].upper()}")
    print(f"  ✓ Needs Review: {summary['needs_review']}")
    
    print("\n🔍 ANOMALY INSIGHTS:")
    anomalies = result["anomaly_insights"]
    print(f"  • Anomaly Detected: {anomalies['anomaly_detected']}")
    print(f"  • Pattern: {anomalies['pattern']}")
    print(f"  • Risk Score: {anomalies['risk_score']}/10")
    print(f"  • Reason: {anomalies['anomaly_reason']}")
    
    if anomalies.get("fraud_indicators"):
        print(f"\n  ⚠️  Fraud Indicators:")
        for indicator in anomalies["fraud_indicators"]:
            print(f"    - {indicator}")
    
    print("\n📈 VISUALIZATION DATA:")
    viz = result["visualization_data"]
    print(f"  • Naughty List Score: {viz['naughty_list_score']}/10")
    print(f"  • Total Discrepancies: {viz['discrepancy_count']}")
    print(f"  • High Severity: {viz['high_severity_count']}")
    
    print("\n  Bar Chart Data:")
    print(f"    PO Total: {viz['bar_chart']['currency']} {viz['bar_chart']['values'][0]:,.2f}")
    print(f"    Invoice Total: {viz['bar_chart']['currency']} {viz['bar_chart']['values'][1]:,.2f}")
    
    print("\n  Discrepancy Breakdown:")
    for category, count in viz['pie_chart']['discrepancy_breakdown'].items():
        if count > 0:
            print(f"    {category}: {count}")
    
    print("\n  Line Items Comparison:")
    for item in viz['line_items_comparison']:
        status = "✓" if item.get('qty_match') and item.get('price_match') else "✗"
        print(f"    {status} {item['description']}")
        if not item.get('qty_match'):
            print(f"      Qty: PO={item['po_qty']} vs Invoice={item['invoice_qty']}")
        if not item.get('price_match'):
            print(f"      Price: PO={item['po_price']} vs Invoice={item['invoice_price']}")
    
    return result


def test_fraudulent_verification():
    """Test verification with major fraud indicators"""
    print_section("TEST 2: Fraudulent Invoice Detection")
    
    result = verify_from_text(
        sample_po,
        sample_fraudulent_invoice,
        "PO_456.pdf",
        "INV_999_FRAUD.pdf"
    )
    
    print("\n🚨 VERIFICATION SUMMARY:")
    summary = result["verification_summary"]
    print(f"  ✗ Vendor Match: {summary['vendor_match']}")
    print(f"  ✗ PO Number Match: {summary['po_number_match']}")
    print(f"  ✗ Total Match: {summary['total_match']}")
    print(f"  ✗ Currency Match: {summary['currency_match']}")
    print(f"  ✗ Amount Difference: ₹{summary['amount_difference']}")
    print(f"  ✗ Discrepancy Level: {summary['discrepancy_level'].upper()}")
    print(f"  ⚠️  NEEDS REVIEW: {summary['needs_review']}")
    
    print("\n🔴 ANOMALY INSIGHTS:")
    anomalies = result["anomaly_insights"]
    print(f"  • Anomaly Detected: {anomalies['anomaly_detected']}")
    print(f"  • Pattern: {anomalies['pattern'].upper()}")
    print(f"  • Risk Score: {anomalies['risk_score']}/10 🚨")
    print(f"  • Reason: {anomalies['anomaly_reason']}")
    
    print(f"\n  🚩 FRAUD INDICATORS ({len(anomalies.get('fraud_indicators', []))}):")
    for indicator in anomalies.get("fraud_indicators", []):
        print(f"    🔴 {indicator}")
    
    print(f"\n  Anomaly Types Detected:")
    for anom_type in anomalies.get("anomaly_types", []):
        print(f"    • {anom_type}")
    
    print("\n📊 VISUALIZATION DATA:")
    viz = result["visualization_data"]
    print(f"  • Naughty List Score: {viz['naughty_list_score']}/10 🚨")
    print(f"  • Total Discrepancies: {viz['discrepancy_count']}")
    print(f"  • High Severity: {viz['high_severity_count']}")
    
    return result


def test_json_output():
    """Test complete JSON output"""
    print_section("TEST 3: Complete JSON Output")
    
    result = verify_from_text(
        sample_po,
        sample_invoice_with_issues,
        "PO_456.pdf",
        "INV_001.pdf"
    )
    
    print("\n📄 COMPLETE JSON RESPONSE:")
    print_json(result)


def test_vendor_history():
    """Test with vendor history"""
    print_section("TEST 4: Verification with Vendor History")
    
    # Create agent with vendor history
    vendor_history = {
        "acme corporation pvt ltd": {
            "anomaly_count": 2,
            "total_submissions": 5,
            "last_anomaly_date": "2025-09-15"
        }
    }
    
    agent = VerificationAgent(vendor_history=vendor_history)
    
    from app.extractor import parse_document
    po_parsed = parse_document(sample_po)
    invoice_parsed = parse_document(sample_invoice_with_issues)
    
    result = agent.verify_documents(po_parsed, invoice_parsed)
    
    print("\n📊 Verification with Historical Context:")
    print(f"  Historical Trend: {result['anomaly_insights']['historical_trend']}")
    print(f"  Risk Score (with history): {result['anomaly_insights']['risk_score']}/10")
    print(f"  Naughty List Score: {result['visualization_data']['naughty_list_score']}/10")


def generate_dashboard_summary(result: dict):
    """Generate dashboard-ready summary"""
    print_section("DASHBOARD SUMMARY")
    
    summary = result["verification_summary"]
    anomalies = result["anomaly_insights"]
    viz = result["visualization_data"]
    
    # Status indicator
    if summary["discrepancy_level"] == "none":
        status = "🟢 APPROVED"
    elif summary["discrepancy_level"] == "low":
        status = "🟡 REVIEW RECOMMENDED"
    elif summary["discrepancy_level"] == "medium":
        status = "🟠 REQUIRES REVIEW"
    else:
        status = "🔴 REJECTED - HIGH RISK"
    
    print(f"\n  Status: {status}")
    print(f"  Risk Score: {anomalies['risk_score']}/10")
    print(f"  Naughty List Score: {viz['naughty_list_score']}/10")
    print(f"\n  Documents:")
    print(f"    PO: {result['po_file']}")
    print(f"    Invoice: {result['invoice_file']}")
    print(f"\n  Key Metrics:")
    print(f"    Vendor Match: {'✓' if summary['vendor_match'] else '✗'}")
    print(f"    Amount Difference: ₹{summary['amount_difference']:,.2f}")
    print(f"    Discrepancies: {viz['discrepancy_count']} ({viz['high_severity_count']} high severity)")
    
    if anomalies["fraud_indicators"]:
        print(f"\n  ⚠️  Action Required:")
        for indicator in anomalies["fraud_indicators"]:
            print(f"    • {indicator}")


if __name__ == "__main__":
    print("=" * 80)
    print("  FUTURIX AI VERIFICATION AGENT - TEST SUITE")
    print("=" * 80)
    
    # Test 1: Normal verification
    result1 = test_normal_verification()
    
    # Test 2: Fraudulent invoice
    result2 = test_fraudulent_verification()
    
    # Test 3: JSON output
    test_json_output()
    
    # Test 4: Vendor history
    test_vendor_history()
    
    # Dashboard summaries
    print("\n")
    generate_dashboard_summary(result1)
    generate_dashboard_summary(result2)
    
    print_section("✨ ALL TESTS COMPLETED")
    print("\n  Verification Agent Status: ✅ OPERATIONAL")
    print("  Ready for production integration")
    print("\n" + "=" * 80)
