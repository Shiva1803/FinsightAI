#!/usr/bin/env python3
"""
Test if verification result can be JSON serialized
"""
import sys
import os
import json

sys.path.insert(0, os.path.dirname(__file__))

from app.verification_agent import verify_from_text

def test_json_serialization():
    print("Testing JSON serialization of verification result...")
    
    po_text = "PO Number: PO-123\nVendor: Test\nTotal: 1000"
    inv_text = "Invoice: INV-123\nVendor: Test\nTotal: 1000"
    
    try:
        result = verify_from_text(po_text, inv_text, "po.txt", "inv.txt")
        print("✅ Verification completed")
        
        # Try to serialize to JSON
        json_str = json.dumps(result)
        print(f"✅ JSON serialization successful ({len(json_str)} chars)")
        
        # Try to parse it back
        parsed = json.loads(json_str)
        print("✅ JSON parsing successful")
        
        return True
        
    except TypeError as e:
        print(f"❌ JSON serialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_json_serialization()
    sys.exit(0 if success else 1)
