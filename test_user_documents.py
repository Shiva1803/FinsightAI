"""
Test the user's PO and Invoice documents
"""
from app.verification_agent import verify_from_text

# Purchase Order
po_text = """
PURCHASE ORDER

PO Number: PO-1001
Issue Date: October 20, 2025

Vendor:
TechVendor Inc.
123 Circuit Lane
Techville, CA 90210

Ship To:
Futurix AI
456 Data Drive
New York, NY 10001

-------------------------------------------------------
Item            Quantity    Unit Price      Total
-------------------------------------------------------
Laptop          10          $800.00         $8000.00
Mouse           10          $25.00          $250.00
-------------------------------------------------------

SUBTOTAL: $8250.00
TAX (8%): $660.00
TOTAL: $8910.00
"""

# Invoice
invoice_text = """
INVOICE

Invoice Number: INV-734
Invoice Date: October 28, 2025
Purchase Order: PO-1001

From:
TechVendor Inc.
123 Circuit Lane
Techville, CA 90210

Bill To:
Futurix AI
456 Data Drive
New York, NY 10001

-------------------------------------------------------
Item            Quantity    Unit Price      Total
-------------------------------------------------------
Laptop          10          $800.00         $8000.00
Mouse           10          $25.00          $250.00
-------------------------------------------------------

SUBTOTAL: $8250.00
TAX (8%): $660.00
TOTAL: $8910.00

Payment Due: November 27, 2025
"""

print("=" * 80)
print("FUTURIX AI - DOCUMENT VERIFICATION TEST")
print("=" * 80)
print("\n📄 Testing User's Documents:")
print("   PO: PO-1001 (October 20, 2025)")
print("   Invoice: INV-734 (October 28, 2025)")
print("\n" + "=" * 80)

# Run verification
result = verify_from_text(po_text, invoice_text, "PO-1001.pdf", "INV-734.pdf")

print("\n✅ VERIFICATION RESULTS")
print("=" * 80)

# Summary
summary = result['verification_summary']
print("\n📊 VERIFICATION SUMMARY:")
print(f"   Vendor Match:        {'✓ YES' if summary['vendor_match'] else '✗ NO'}")
print(f"   PO Number Match:     {'✓ YES' if summary['po_number_match'] else '✗ NO'}")
print(f"   Total Match:         {'✓ YES' if summary['total_match'] else '✗ NO'}")
print(f"   Amount Difference:   ${summary['amount_difference']}")
print(f"   Tax Match:           {'✓ YES' if summary['tax_match'] else '✗ NO'}")
print(f"   Currency Match:      {'✓ YES' if summary['currency_match'] else '✗ NO'}")
print(f"   Date Difference:     {summary['date_difference_days']} days")
print(f"   Discrepancy Level:   {summary['discrepancy_level'].upper()}")
print(f"   Needs Review:        {'YES' if summary['needs_review'] else 'NO'}")

# Anomaly Insights
anomalies = result['anomaly_insights']
print(f"\n🔍 ANOMALY DETECTION:")
print(f"   Anomaly Detected:    {'YES' if anomalies['anomaly_detected'] else 'NO'}")
print(f"   Risk Score:          {anomalies['risk_score']}/10")
print(f"   Pattern:             {anomalies['pattern']}")
print(f"   Reason:              {anomalies['anomaly_reason']}")

if anomalies['fraud_indicators']:
    print(f"\n⚠️  FRAUD INDICATORS:")
    for indicator in anomalies['fraud_indicators']:
        print(f"   • {indicator}")
else:
    print(f"\n✅ No fraud indicators detected")

# Visualization Data
viz = result['visualization_data']
print(f"\n📈 FINANCIAL COMPARISON:")
print(f"   PO Total:            ${viz['bar_chart']['values'][0]:,.2f}")
print(f"   Invoice Total:       ${viz['bar_chart']['values'][1]:,.2f}")
print(f"   Currency:            {viz['bar_chart']['currency']}")

# Line Items
print(f"\n📦 LINE ITEMS COMPARISON:")
if viz['line_items_comparison']:
    print(f"   {'Item':<20} {'PO Qty':<10} {'Inv Qty':<10} {'PO Price':<12} {'Inv Price':<12} {'Match'}")
    print(f"   {'-'*20} {'-'*10} {'-'*10} {'-'*12} {'-'*12} {'-'*5}")
    for item in viz['line_items_comparison']:
        match_symbol = '✓' if (item['qty_match'] and item['price_match']) else '✗'
        print(f"   {item['description']:<20} {str(item['po_qty']):<10} {str(item['invoice_qty']):<10} "
              f"${item['po_price']:<11.2f} ${item['invoice_price']:<11.2f} {match_symbol}")
else:
    print("   No line items found")

# Final Verdict
print("\n" + "=" * 80)
print("🎯 FINAL VERDICT:")
print("=" * 80)

if summary['discrepancy_level'] == 'none':
    print("✅ APPROVED - Documents match perfectly!")
    print("   No discrepancies found. Invoice matches the Purchase Order.")
elif summary['discrepancy_level'] == 'low':
    print("⚠️  MINOR ISSUES - Review recommended")
    print("   Small discrepancies found but within acceptable tolerance.")
elif summary['discrepancy_level'] == 'medium':
    print("⚠️  MODERATE ISSUES - Review required")
    print("   Notable discrepancies found. Manual review needed.")
else:
    print("🚨 HIGH RISK - Immediate review required!")
    print("   Significant discrepancies or fraud indicators detected.")

print("\n" + "=" * 80)
print("Test completed successfully!")
print("=" * 80)
