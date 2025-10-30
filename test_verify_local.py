#!/usr/bin/env python3
"""
Test verification locally to debug the 500 error
"""
import sys
import os

# Add app directory to path
sys.path.insert(0, os.path.dirname(__file__))

from app import ocr
from app.verification_agent import verify_from_text

def test_verification():
    print("=" * 60)
    print("Testing Verification Locally")
    print("=" * 60)
    
    # Test with sample PO text
    po_text = """
    Purchase Order (PO)
    PO Number: PO-2045
    Date: 30-Oct-2025
    Buyer: Innoventix Solutions Pvt. Ltd.
    Vendor: AlphaTech Supplies Ltd.
    
    Item 1: HP ProBook 450 G10 Laptop - Qty: 5 - Price: ₹82,500 - Total: ₹4,12,500
    Item 2: Logitech MX Master 3S Mouse - Qty: 5 - Price: ₹7,200 - Total: ₹36,000
    
    Subtotal: ₹5,19,500
    GST (18%): ₹93,510
    Grand Total: ₹6,13,010
    """
    
    invoice_text = """
    Invoice
    Invoice Number: INV-2045
    Date: 05-Nov-2025
    Vendor: AlphaTech Supplies Ltd.
    Buyer: Innoventix Solutions Pvt. Ltd.
    
    Item 1: HP ProBook 450 G10 Laptop - Qty: 5 - Price: ₹82,500 - Total: ₹4,12,500
    Item 2: Logitech MX Master 3S Mouse - Qty: 5 - Price: ₹7,200 - Total: ₹36,000
    
    Subtotal: ₹5,19,500
    GST (18%): ₹93,510
    Grand Total: ₹6,13,010
    """
    
    try:
        print("\n1. Testing verification with sample text...")
        result = verify_from_text(po_text, invoice_text, "test_po.txt", "test_invoice.txt")
        print("✅ Verification successful!")
        print(f"   Risk Score: {result['anomaly_insights']['risk_score']}")
        print(f"   Discrepancy Level: {result['verification_summary']['discrepancy_level']}")
        print(f"   Needs Review: {result['verification_summary']['needs_review']}")
        return True
        
    except Exception as e:
        print(f"❌ Verification failed with error:")
        print(f"   {type(e).__name__}: {e}")
        import traceback
        print("\nFull traceback:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_verification()
    sys.exit(0 if success else 1)
