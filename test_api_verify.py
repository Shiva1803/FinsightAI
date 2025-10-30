#!/usr/bin/env python3
"""
Test the exact flow that happens in the API endpoint
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from app import ocr, db
from app.verification_agent import verify_from_text

def test_api_flow():
    print("=" * 60)
    print("Testing Complete API Verification Flow")
    print("=" * 60)
    
    # Use actual uploaded files
    po_file = "uploads/1761820667_invoice 1.pdf"
    invoice_file = "uploads/1761820642_invoice 2.pdf"
    
    try:
        # Step 1: Read files
        print("\n1. Reading PO file...")
        with open(po_file, 'rb') as f:
            po_content = f.read()
        print(f"   ✅ Read {len(po_content)} bytes")
        
        # Step 2: OCR on PO
        print("\n2. Running OCR on PO...")
        po_ocr_text = ocr.run_ocr_bytes(po_content, po_file)
        if po_ocr_text.startswith("ERROR:"):
            print(f"   ❌ OCR failed: {po_ocr_text}")
            return False
        print(f"   ✅ OCR successful ({len(po_ocr_text)} chars)")
        
        # Step 3: Read invoice
        print("\n3. Reading Invoice file...")
        with open(invoice_file, 'rb') as f:
            inv_content = f.read()
        print(f"   ✅ Read {len(inv_content)} bytes")
        
        # Step 4: OCR on Invoice
        print("\n4. Running OCR on Invoice...")
        inv_ocr_text = ocr.run_ocr_bytes(inv_content, invoice_file)
        if inv_ocr_text.startswith("ERROR:"):
            print(f"   ❌ OCR failed: {inv_ocr_text}")
            return False
        print(f"   ✅ OCR successful ({len(inv_ocr_text)} chars)")
        
        # Step 5: Run verification
        print("\n5. Running verification...")
        result = verify_from_text(po_ocr_text, inv_ocr_text, po_file, invoice_file)
        print("   ✅ Verification successful!")
        
        # Step 6: Save to database
        print("\n6. Saving to database...")
        record_id = db.save_record(result, source_file=f"verification_{po_file}_{invoice_file}")
        print(f"   ✅ Saved with ID: {record_id}")
        
        # Step 7: Verify it can be retrieved
        print("\n7. Retrieving from database...")
        records = db.list_records()
        saved_record = next((r for r in records if r['id'] == record_id), None)
        if saved_record:
            print(f"   ✅ Retrieved successfully")
            print(f"   Record has keys: {list(saved_record['parsed'].keys())[:5]}...")
        else:
            print(f"   ❌ Could not retrieve record")
            return False
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED - Verification flow works correctly!")
        print("=" * 60)
        print("\nVerification Summary:")
        print(f"  Risk Score: {result['anomaly_insights']['risk_score']}")
        print(f"  Discrepancy Level: {result['verification_summary']['discrepancy_level']}")
        print(f"  Needs Review: {result['verification_summary']['needs_review']}")
        print(f"  Vendor Match: {result['verification_summary']['vendor_match']}")
        print(f"  Amount Match: {result['verification_summary']['total_match']}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error at some step:")
        print(f"   {type(e).__name__}: {e}")
        import traceback
        print("\nFull traceback:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_api_flow()
    sys.exit(0 if success else 1)
