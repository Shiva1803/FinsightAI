import os
import httpx
from typing import Any, Dict, Optional

SHIVAAY_API_KEY = os.getenv("SHIVAAY_API_KEY", "6903c3fe3bb9326d4656659b")
# Note: Update this URL with the correct Shivaay API endpoint when available
SHIVAAY_API_URL = os.getenv("SHIVAAY_API_URL", "https://api.shivaay.futurixai.com/v1/extract")

DEFAULT_PROMPT = """You are an expert AI system specialized in extracting structured data from invoice and purchase order documents.

Extract the following information from the provided OCR text and return it as a JSON object:

{
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
    {
      "description": "Item description",
      "sku": "Item code/SKU if available",
      "quantity": numeric quantity,
      "unit_price": numeric price per unit,
      "line_total": numeric total for this line
    }
  ]
}

Instructions:
1. Extract all available fields from the OCR text
2. Use null for missing fields
3. Convert all amounts to numeric values (remove currency symbols and commas)
4. Format dates as YYYY-MM-DD
5. Be precise and accurate
6. If uncertain about a field, set it to null rather than guessing

Return ONLY the JSON object, no additional text."""

HEADERS = {
    "Authorization": f"Bearer {SHIVAAY_API_KEY}" if SHIVAAY_API_KEY else "",
    "Content-Type": "application/json",
}

async def send_extraction_request(ocr_text: str, prompt: Optional[str] = None, timeout: int = 30) -> Dict[str, Any]:
    payload = {
        "prompt": prompt or DEFAULT_PROMPT,
        "input_text": ocr_text,
        "response_format": "json"
    }

    async with httpx.AsyncClient(timeout=timeout) as client:
        resp = await client.post(SHIVAAY_API_URL, headers=HEADERS, json=payload)
        try:
            resp.raise_for_status()
        except httpx.HTTPStatusError:
            return {"error": True, "status_code": resp.status_code, "text": resp.text}

        try:
            return resp.json()
        except Exception:
            return {"error": True, "status_code": resp.status_code, "text": resp.text}

def _safe_float(v):
    if v is None: return None
    try:
        s = str(v).replace(",", "").strip()
        return float(s)
    except Exception:
        return None

def map_shivaay_to_output(shivaay_resp: dict, ocr_text: str) -> dict:
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
        "extraction_debug": {"shivaay_raw": shivaay_resp}
    }

    src = None
    if isinstance(shivaay_resp, dict):
        for candidate in ("result", "data", "output", "parsed"):
            if candidate in shivaay_resp:
                src = shivaay_resp[candidate]
                break
        if src is None:
            src = shivaay_resp

    def get(k):
        if not isinstance(src, dict):
            return None
        return src.get(k) or src.get(k.lower()) or src.get(k.upper())

    out["document_type"] = get("document_type") or get("doc_type") or None
    out["vendor_name"] = get("vendor_name") or get("supplier") or get("vendor")
    out["vendor_tax_id"] = get("vendor_tax_id") or get("gst") or get("tax_id")
    out["buyer_name"] = get("buyer_name") or get("bill_to") or get("buyer")
    out["buyer_tax_id"] = get("buyer_tax_id") or get("buyer_tax")
    out["document_number"] = get("document_number") or get("invoice_number") or get("doc_number")
    out["po_number"] = get("po_number") or get("po")
    out["invoice_date"] = get("invoice_date") or get("date")
    out["due_date"] = get("due_date")
    out["currency"] = get("currency")
    out["total_amount"] = _safe_float(get("total_amount") or get("grand_total") or get("total"))
    out["subtotal_amount"] = _safe_float(get("subtotal_amount") or get("subtotal") or get("sub_total"))
    out["tax_amount"] = _safe_float(get("tax_amount") or get("vat") or get("tax"))

    items = get("line_items") or get("items") or get("lines") or []
    if isinstance(items, list) and items:
        mapped = []
        for it in items[:50]:
            if not isinstance(it, dict):
                continue
            mapped.append({
                "description": it.get("description") or it.get("desc") or None,
                "sku": it.get("sku") or it.get("item_code") or None,
                "unit_price": _safe_float(it.get("unit_price") or it.get("price")),
                "quantity": _safe_float(it.get("quantity") or it.get("qty")),
                "line_total": _safe_float(it.get("line_total") or it.get("total"))
            })
        out["line_items"] = mapped
    else:
        out["line_items"] = []

    out["raw_text_snippet"] = (ocr_text or "")[:300]

    for k in ("vendor_name", "document_number", "total_amount"):
        if not out.get(k):
            out["extraction_warnings"].append(f"Missing or low-confidence field: {k}")

    return out
