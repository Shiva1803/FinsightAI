#!/usr/bin/env python3
"""
Test verification with actual PDF files
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from app import ocr
from app.verification_agent import verify_from_text

def test_with_pdfs():
    print("=" * 60)
    print("Testing Verification with PDF Files")
    print("=" * 60)
    
    # Use existing files from uploads
    po_file = "uploads/1761820667_invoice 1.pdf"
    invoice_file = "uploads/1761820642_invoice 2.pdf"
    
    if not os.path.exists(po_file):
        print(f"❌ PO file not found: {po_file}")
        return False
    
    if not os.path.exists(invoice_file):
        print(f"❌ Invoice file not found: {invoice_file}")
        return False
    
    try:
        print(f"\n1. Reading PO file: {po_file}")
        with open(po_file, 'rb') as f:
            po_content = f.read()
        
        print(f"2. Running OCR on PO...")
        po_text = ocr.run_ocr_bytes(po_content, po_file)
        
        if po_text.startswith("ERROR:"):
            print(f"❌ PO OCR failed: {po_text}")
            return False
        
        print(f"✅ PO OCR successful ({len(po_text)} chars)")
        print(f"   Preview: {po_text[:200]}...")
        
        print(f"\n3. Reading Invoice file: {invoice_file}")
        with open(invoice_file, 'rb') as f:
            inv_content = f.read()
        
        print(f"4. Running OCR on Invoice...")
        inv_text = ocr.run_ocr_bytes(inv_content, invoice_file)
        
        if inv_text.startswith("ERROR:"):
            print(f"❌ Invoice OCR failed: {inv_text}")
            return False
        
        print(f"✅ Invoice OCR successful ({len(inv_text)} chars)")
        print(f"   Preview: {inv_text[:200]}...")
        
        print(f"\n5. Running verification...")
        result = verify_from_text(po_text, inv_text, po_file, invoice_file)
        
        print("✅ Verification successful!")
        print(f"   Risk Score: {result['anomaly_insights']['risk_score']}")
        print(f"   Discrepancy Level: {result['verification_summary']['discrepancy_level']}")
        print(f"   Needs Review: {result['verification_summary']['needs_review']}")
        print(f"   Vendor Match: {result['verification_summary']['vendor_match']}")
        print(f"   Amount Match: {result['verification_summary']['total_match']}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error occurred:")
        print(f"   {type(e).__name__}: {e}")
        import traceback
        print("\nFull traceback:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_with_pdfs()
    sys.exit(0 if success else 1)
