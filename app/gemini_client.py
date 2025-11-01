"""
Google Gemini AI Integration for Document Extraction
"""
import os
import json
import google.generativeai as genai
from typing import Dict, Any

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
genai.configure(api_key=GEMINI_API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel('gemini-2.5-flash')

EXTRACTION_PROMPT = """You are an expert AI system specialized in extracting structured data from invoice and purchase order documents.

Extract the following information from the provided OCR text and return it as a JSON object:

{{
  "document_type": "invoice" or "purchase_order",
  "vendor_name": "Company name of the seller/supplier",
  "vendor_tax_id": "GST/VAT/Tax ID of vendor",
  "buyer_name": "Company name of the buyer",
  "buyer_tax_id": "GST/VAT/Tax ID of buyer",
  "document_number": "Invoice number or PO number",
  "po_number": "Referenced PO number (if this is an invoice)",
  "invoice_date": "Date in YYYY-MM-DD format",
  "due_date": "Payment due date in YYYY-MM-DD format",
  "currency": "Currency code (INR, USD, EUR, etc.)",
  "total_amount": numeric value without currency symbols,
  "subtotal_amount": numeric value before tax,
  "tax_amount": numeric tax amount,
  "line_items": [
    {{
      "description": "Item description",
      "sku": "Item code/SKU if available",
      "quantity": numeric quantity,
      "unit_price": numeric price per unit,
      "line_total": numeric total for this line
    }}
  ]
}}

Instructions:
1. Extract all available fields from the OCR text
2. Use null for missing fields
3. Convert all amounts to numeric values (remove currency symbols and commas)
4. Format dates as YYYY-MM-DD
5. Be precise and accurate
6. Return ONLY valid JSON, no markdown, no explanations

OCR Text:
{ocr_text}"""


def extract_with_gemini(ocr_text: str) -> Dict[str, Any]:
    """
    Extract structured data from OCR text using Google Gemini AI
    
    Args:
        ocr_text: Raw OCR text from document
        
    Returns:
        Dict with extraction results
    """
    try:
        # Generate prompt
        prompt = EXTRACTION_PROMPT.format(ocr_text=ocr_text)
        
        # Call Gemini API
        response = model.generate_content(prompt)
        
        # Get response text
        result_text = response.text.strip()
        
        # Remove markdown code blocks if present
        if result_text.startswith("```json"):
            result_text = result_text[7:]
        if result_text.startswith("```"):
            result_text = result_text[3:]
        if result_text.endswith("```"):
            result_text = result_text[:-3]
        
        result_text = result_text.strip()
        
        # Find JSON object in the response
        start_idx = result_text.find('{')
        end_idx = result_text.rfind('}')
        
        if start_idx != -1 and end_idx != -1:
            json_text = result_text[start_idx:end_idx+1]
        else:
            json_text = result_text
        
        # Parse JSON
        result = json.loads(json_text)
        
        return {
            "success": True,
            "data": result,
            "provider": "gemini",
            "model": "gemini-pro"
        }
        
    except json.JSONDecodeError as e:
        print(f"DEBUG: JSON parse error: {str(e)}")
        if 'json_text' in locals():
            print(f"DEBUG: Attempted to parse: {json_text[:500]}")
        return {
            "success": False,
            "error": f"JSON parsing error: {str(e)}",
            "provider": "gemini",
            "raw_response": json_text if 'json_text' in locals() else None
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "provider": "gemini"
        }


def _safe_float(v):
    """Convert value to float safely"""
    if v is None:
        return None
    try:
        s = str(v).replace(",", "").strip()
        return float(s)
    except Exception:
        return None


def map_gemini_to_output(gemini_resp: dict, ocr_text: str) -> dict:
    """
    Map Gemini response to standard output format
    
    Args:
        gemini_resp: Response from Gemini API
        ocr_text: Original OCR text
        
    Returns:
        Standardized document data
    """
    out = {
        "document_type": None,
        "vendor_name": None,
        "vendor_tax_id": None,
        "buyer_name": None,
        "buyer_tax_id": None,
        "document_number": None,
        "po_number": None,
        "invoice_date": None,
        "due_date": None,
        "currency": None,
        "total_amount": None,
        "subtotal_amount": None,
        "tax_amount": None,
        "line_items": [],
        "footnotes": None,
        "raw_text_snippet": None,
        "extraction_warnings": [],
        "extraction_debug": {"gemini_raw": gemini_resp}
    }
    
    if not gemini_resp.get("success"):
        out["extraction_warnings"].append(f"Gemini extraction failed: {gemini_resp.get('error')}")
        return out
    
    data = gemini_resp.get("data", {})
    
    # Map fields
    out["document_type"] = data.get("document_type")
    out["vendor_name"] = data.get("vendor_name")
    out["vendor_tax_id"] = data.get("vendor_tax_id")
    out["buyer_name"] = data.get("buyer_name")
    out["buyer_tax_id"] = data.get("buyer_tax_id")
    out["document_number"] = data.get("document_number")
    out["po_number"] = data.get("po_number")
    out["invoice_date"] = data.get("invoice_date")
    out["due_date"] = data.get("due_date")
    out["currency"] = data.get("currency")
    out["total_amount"] = _safe_float(data.get("total_amount"))
    out["subtotal_amount"] = _safe_float(data.get("subtotal_amount"))
    out["tax_amount"] = _safe_float(data.get("tax_amount"))
    
    # Map line items
    items = data.get("line_items", [])
    if isinstance(items, list):
        mapped_items = []
        for item in items[:50]:  # Limit to 50 items
            if isinstance(item, dict):
                mapped_items.append({
                    "description": item.get("description"),
                    "sku": item.get("sku"),
                    "unit_price": _safe_float(item.get("unit_price")),
                    "quantity": _safe_float(item.get("quantity")),
                    "line_total": _safe_float(item.get("line_total"))
                })
        out["line_items"] = mapped_items
    
    out["raw_text_snippet"] = (ocr_text or "")[:300]
    
    # Add warnings for missing critical fields
    for field in ("vendor_name", "document_number", "total_amount"):
        if not out.get(field):
            out["extraction_warnings"].append(f"Missing field: {field}")
    
    return out
