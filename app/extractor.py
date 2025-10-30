import re
from dateutil import parser
import datetime
from typing import Dict, List, Optional, Tuple, Any
from . import utils

def _first(regexes, text, flags=re.IGNORECASE):
    """Try multiple regexes and return first match with confidence"""
    for idx, r in enumerate(regexes):
        m = re.search(r, text, flags=flags)
        if m:
            # Higher confidence for earlier patterns (more specific)
            confidence = 0.95 - (idx * 0.05)
            return m, max(confidence, 0.6)
    return None, 0.0

def _extract_number(text: str) -> Optional[float]:
    """Extract numeric value handling various formats"""
    if not text:
        return None
    # Remove currency symbols and whitespace
    text = re.sub(r'[₹$€£¥\s]', '', text)
    # Handle both comma and dot as separators
    text = text.replace(',', '')
    try:
        return float(text)
    except:
        return None

def _normalize_date(date_str: str) -> Optional[str]:
    """Parse and normalize date to ISO format"""
    if not date_str:
        return None
    try:
        # Try multiple date formats
        dt = parser.parse(date_str, dayfirst=False, fuzzy=True)
        return dt.date().isoformat()
    except:
        return None

def _detect_document_type(text: str) -> Tuple[str, float, str]:
    """Detect document type with confidence and debug info"""
    text_lower = text.lower()
    
    # Check for explicit headings (highest confidence)
    if re.search(r'^[\s\*]*(?:tax\s+)?invoice[\s\*]*$', text, flags=re.IGNORECASE | re.MULTILINE):
        return "invoice", 0.95, "explicit_heading:invoice"
    if re.search(r'^[\s\*]*purchase\s+order[\s\*]*$', text, flags=re.IGNORECASE | re.MULTILINE):
        return "purchase_order", 0.95, "explicit_heading:po"
    
    # Count keywords
    invoice_keywords = len(re.findall(r'\binvoice\b|tax invoice|invoice number|bill to', text_lower))
    po_keywords = len(re.findall(r'purchase order|po number|order no\b|p\.o\.|order date', text_lower))
    
    if invoice_keywords > po_keywords and invoice_keywords > 0:
        return "invoice", 0.8, f"keyword_count:invoice={invoice_keywords}"
    elif po_keywords > invoice_keywords and po_keywords > 0:
        return "purchase_order", 0.8, f"keyword_count:po={po_keywords}"
    elif invoice_keywords > 0:
        return "invoice", 0.6, "keyword_present:invoice"
    elif po_keywords > 0:
        return "purchase_order", 0.6, "keyword_present:po"
    
    return "unknown", 0.3, "no_clear_indicators"

def _extract_vendor_info(text: str) -> Tuple[Optional[str], Optional[str], float, str]:
    """Extract vendor name and tax ID"""
    vendor_name = None
    vendor_tax_id = None
    confidence = 0.0
    debug = ""
    
    # Try labeled patterns first
    patterns = [
        r'(?:From|Vendor|Supplier|Seller)[\s:]+([^\n]+)',
        r'Bill\s+From[\s:]+([^\n]+)',
        r'GSTIN[\s:]+(\w+).*?([^\n]+)',  # Tax ID with name
    ]
    
    m, conf = _first(patterns, text)
    if m:
        vendor_name = m.group(1).strip()
        confidence = conf
        debug = f"labeled_pattern:{m.re.pattern[:30]}"
    else:
        # Fallback: first non-empty line (low confidence)
        lines = [l.strip() for l in text.splitlines() if l.strip() and len(l.strip()) > 3]
        if lines:
            vendor_name = lines[0]
            confidence = 0.4
            debug = "fallback:first_line"
    
    # Extract tax ID (GST, VAT, TIN, etc.)
    tax_patterns = [
        r'(?:GSTIN|GST\s+No\.?|GST)[\s:#\-]*([A-Z0-9]{15})',
        r'(?:VAT\s+No\.?|VAT)[\s:#\-]*([A-Z0-9]+)',
        r'(?:TIN|Tax\s+ID)[\s:#\-]*([A-Z0-9]+)',
        r'(?:PAN)[\s:#\-]*([A-Z]{5}[0-9]{4}[A-Z])',
    ]
    
    m, _ = _first(tax_patterns, text)
    if m:
        vendor_tax_id = m.group(1).strip()
        debug += f"|tax_id_found"
    
    return vendor_name, vendor_tax_id, confidence, debug

def _extract_buyer_info(text: str) -> Tuple[Optional[str], Optional[str], float, str]:
    """Extract buyer name and tax ID"""
    buyer_name = None
    buyer_tax_id = None
    confidence = 0.0
    debug = ""
    
    patterns = [
        r'(?:To|Bill\s+To|Buyer|Customer)[\s:]+([^\n]+)',
        r'Ship\s+To[\s:]+([^\n]+)',
    ]
    
    m, conf = _first(patterns, text)
    if m:
        buyer_name = m.group(1).strip()
        confidence = conf
        debug = f"labeled_pattern"
    
    # Buyer tax ID (usually after buyer name section)
    if buyer_name:
        # Search in next few lines after buyer name
        buyer_section = text[text.find(buyer_name):text.find(buyer_name)+500] if buyer_name in text else ""
        tax_patterns = [
            r'(?:GSTIN|GST)[\s:#\-]*([A-Z0-9]{15})',
            r'(?:VAT)[\s:#\-]*([A-Z0-9]+)',
        ]
        m, _ = _first(tax_patterns, buyer_section)
        if m:
            buyer_tax_id = m.group(1).strip()
    
    return buyer_name, buyer_tax_id, confidence, debug

def _extract_document_number(text: str, doc_type: str) -> Tuple[Optional[str], float, str]:
    """Extract document number based on type"""
    if doc_type == "invoice":
        patterns = [
            r'Invoice\s+(?:No\.?|Number|#)[\s:#\-]*(\S+)',
            r'Bill\s+(?:No\.?|Number)[\s:#\-]*(\S+)',
            r'Document\s+(?:No\.?|Number)[\s:#\-]*(\S+)',
        ]
    elif doc_type == "purchase_order":
        patterns = [
            r'(?:Purchase\s+)?Order\s+(?:No\.?|Number|#)[\s:#\-]*(\S+)',
            r'PO\s+(?:No\.?|Number|#)[\s:#\-]*(\S+)',
        ]
    else:
        patterns = [
            r'(?:Invoice|Document|Order)\s+(?:No\.?|Number|#)[\s:#\-]*(\S+)',
        ]
    
    m, conf = _first(patterns, text)
    if m:
        return m.group(1).strip(), conf, f"pattern_match"
    return None, 0.0, "not_found"

def _extract_po_number(text: str) -> Tuple[Optional[str], float, str]:
    """Extract PO number from invoice"""
    patterns = [
        r'PO\s+(?:No\.?|Number|#)[\s:#\-]*(\S+)',
        r'Purchase\s+Order[\s:#\-]*(\S+)',
        r'P\.O\.[\s:#\-]*(\S+)',
        r'Ref(?:erence)?[\s:#\-]*PO[\s:#\-]*(\S+)',
    ]
    
    m, conf = _first(patterns, text)
    if m:
        return m.group(1).strip(), conf, "pattern_match"
    return None, 0.0, "not_found"

def _extract_dates(text: str) -> Dict[str, Any]:
    """Extract invoice and due dates"""
    result = {
        "invoice_date": None,
        "due_date": None,
        "invoice_date_confidence": 0.0,
        "due_date_confidence": 0.0,
        "debug": ""
    }
    
    # Invoice date
    patterns = [
        r'Invoice\s+Date[\s:#\-]*([\d\-/\.\s]+)',
        r'Bill\s+Date[\s:#\-]*([\d\-/\.\s]+)',
        r'Date[\s:#\-]*([\d\-/\.\s]+)',
        r'Dated[\s:#\-]*([\d\-/\.\s]+)',
    ]
    
    m, conf = _first(patterns, text)
    if m:
        result["invoice_date"] = _normalize_date(m.group(1))
        result["invoice_date_confidence"] = conf if result["invoice_date"] else 0.0
        result["debug"] = "invoice_date_found"
    
    # Due date
    due_patterns = [
        r'Due\s+Date[\s:#\-]*([\d\-/\.\s]+)',
        r'Payment\s+Due[\s:#\-]*([\d\-/\.\s]+)',
        r'Due\s+By[\s:#\-]*([\d\-/\.\s]+)',
    ]
    
    m, conf = _first(due_patterns, text)
    if m:
        result["due_date"] = _normalize_date(m.group(1))
        result["due_date_confidence"] = conf if result["due_date"] else 0.0
        result["debug"] += "|due_date_found"
    
    return result

def _extract_currency(text: str) -> Tuple[Optional[str], float, str]:
    """Extract currency code"""
    # Look for ISO codes
    iso_patterns = [
        r'\b(INR|USD|EUR|GBP|JPY|AUD|CAD|CHF|CNY|SGD)\b',
        r'Currency[\s:#\-]*([A-Z]{3})',
    ]
    
    m, conf = _first(iso_patterns, text)
    if m:
        return m.group(1).upper(), conf, "iso_code_found"
    
    # Infer from symbols
    if '₹' in text or 'Rs.' in text or 'INR' in text:
        return "INR", 0.7, "symbol_inferred:INR"
    elif '$' in text:
        return "USD", 0.5, "symbol_inferred:USD"
    elif '€' in text:
        return "EUR", 0.7, "symbol_inferred:EUR"
    elif '£' in text:
        return "GBP", 0.7, "symbol_inferred:GBP"
    
    return None, 0.0, "not_found"

def _extract_amounts(text: str) -> Dict[str, Any]:
    """Extract total, subtotal, and tax amounts"""
    result = {
        "total_amount": None,
        "subtotal_amount": None,
        "tax_amount": None,
        "total_confidence": 0.0,
        "debug": ""
    }
    
    # Total amount (prefer labeled, then bottom-right position)
    total_patterns = [
        r'(?:Grand\s+)?Total\s+Amount[\s:#\-]*[₹$€£¥]?\s*([\d,]+\.?\d*)',
        r'Grand\s+Total[\s:#\-]*[₹$€£¥]?\s*([\d,]+\.?\d*)',
        r'Total[\s:#\-]*[₹$€£¥]?\s*([\d,]+\.?\d*)',
        r'Amount\s+Payable[\s:#\-]*[₹$€£¥]?\s*([\d,]+\.?\d*)',
        r'Net\s+Amount[\s:#\-]*[₹$€£¥]?\s*([\d,]+\.?\d*)',
    ]
    
    m, conf = _first(total_patterns, text)
    if m:
        result["total_amount"] = _extract_number(m.group(1))
        result["total_confidence"] = conf if result["total_amount"] else 0.0
        result["debug"] = "total_labeled"
    
    # Subtotal
    subtotal_patterns = [
        r'Sub[\s\-]?Total[\s:#\-]*[₹$€£¥]?\s*([\d,]+\.?\d*)',
        r'Subtotal[\s:#\-]*[₹$€£¥]?\s*([\d,]+\.?\d*)',
    ]
    
    m, conf = _first(subtotal_patterns, text)
    if m:
        result["subtotal_amount"] = _extract_number(m.group(1))
        result["debug"] += "|subtotal_found"
    
    # Tax amount
    tax_patterns = [
        r'(?:GST|VAT|Tax)\s+Amount[\s:#\-]*[₹$€£¥]?\s*([\d,]+\.?\d*)',
        r'Total\s+Tax[\s:#\-]*[₹$€£¥]?\s*([\d,]+\.?\d*)',
        r'Tax[\s:#\-]*[₹$€£¥]?\s*([\d,]+\.?\d*)',
    ]
    
    m, conf = _first(tax_patterns, text)
    if m:
        result["tax_amount"] = _extract_number(m.group(1))
        result["debug"] += "|tax_found"
    
    return result

def _extract_line_items(text: str) -> Tuple[List[Dict], str]:
    """Extract line items from tabular regions"""
    items = []
    debug = ""
    
    lines = text.splitlines()
    
    # Pattern 1: qty x price format
    for line in lines:
        line = line.strip()
        if not line or len(line) < 10:
            continue
        
        # Pattern: description ... qty x unit_price = total
        m = re.search(r'(.+?)\s+(\d+)\s*[xX×]\s*[₹$€£¥]?\s*([\d,]+\.?\d*)\s*=?\s*[₹$€£¥]?\s*([\d,]+\.?\d*)?', line)
        if m:
            desc = m.group(1).strip()
            qty = int(m.group(2))
            unit_price = _extract_number(m.group(3))
            line_total = _extract_number(m.group(4)) if m.group(4) else (qty * unit_price if unit_price else None)
            
            items.append({
                "description": desc,
                "sku": None,
                "unit_price": unit_price,
                "quantity": qty,
                "line_total": line_total
            })
            continue
        
        # Pattern 2: tabular format with columns
        # desc | sku | qty | price | total
        parts = re.split(r'\s{2,}|\t', line)
        if len(parts) >= 4:
            # Try to identify numeric columns
            numeric_parts = []
            for p in parts:
                num = _extract_number(p)
                if num is not None:
                    numeric_parts.append(num)
            
            if len(numeric_parts) >= 2:
                # Assume: description is first non-numeric, then qty, price, total
                desc = parts[0]
                if len(numeric_parts) >= 3:
                    items.append({
                        "description": desc,
                        "sku": None,
                        "quantity": numeric_parts[0],
                        "unit_price": numeric_parts[1],
                        "line_total": numeric_parts[2]
                    })
                elif len(numeric_parts) == 2:
                    items.append({
                        "description": desc,
                        "sku": None,
                        "quantity": numeric_parts[0],
                        "unit_price": numeric_parts[1],
                        "line_total": None
                    })
    
    # Limit to 5 items if too many found (likely false positives)
    if len(items) > 10:
        items = items[:5]
        debug = "limited_to_5_items"
    elif items:
        debug = f"found_{len(items)}_items"
    else:
        debug = "no_items_found"
    
    return items, debug

def _extract_footnotes(text: str) -> Optional[str]:
    """Extract footer text"""
    lines = text.splitlines()
    # Look for common footer patterns in last 5 lines
    footer_lines = []
    for line in lines[-5:]:
        line = line.strip()
        if re.search(r'thank|regards|terms|conditions|note|authorized|signature', line, re.IGNORECASE):
            footer_lines.append(line)
    
    return ' '.join(footer_lines) if footer_lines else None

def parse_document(text: str) -> Dict[str, Any]:
    """
    Parse OCR text and extract structured invoice/PO data.
    Returns JSON with all fields and metadata.
    """
    text = text or ""
    warnings = []
    debug_info = {}
    
    # Document type
    doc_type, doc_conf, doc_debug = _detect_document_type(text)
    debug_info["document_type"] = doc_debug
    if doc_conf < 0.7:
        warnings.append(f"Low confidence document type detection: {doc_conf:.2f}")
    
    # Vendor info
    vendor_name, vendor_tax_id, vendor_conf, vendor_debug = _extract_vendor_info(text)
    debug_info["vendor"] = vendor_debug
    if not vendor_name:
        warnings.append("Vendor name not found")
    elif vendor_conf < 0.6:
        warnings.append(f"Low confidence vendor extraction: {vendor_conf:.2f}")
    
    # Buyer info
    buyer_name, buyer_tax_id, buyer_conf, buyer_debug = _extract_buyer_info(text)
    debug_info["buyer"] = buyer_debug
    if not buyer_name:
        warnings.append("Buyer name not found")
    
    # Document number
    doc_number, doc_num_conf, doc_num_debug = _extract_document_number(text, doc_type)
    debug_info["document_number"] = doc_num_debug
    if not doc_number:
        warnings.append("Document number not found")
    
    # PO number
    po_number, po_conf, po_debug = _extract_po_number(text)
    debug_info["po_number"] = po_debug
    
    # Dates
    date_info = _extract_dates(text)
    debug_info["dates"] = date_info["debug"]
    if not date_info["invoice_date"]:
        warnings.append("Invoice date not found")
    
    # Currency
    currency, curr_conf, curr_debug = _extract_currency(text)
    debug_info["currency"] = curr_debug
    if not currency:
        warnings.append("Currency not detected")
    
    # Amounts
    amounts = _extract_amounts(text)
    debug_info["amounts"] = amounts["debug"]
    if not amounts["total_amount"]:
        warnings.append("Total amount not found")
    elif amounts["total_confidence"] < 0.6:
        warnings.append(f"Low confidence total amount: {amounts['total_confidence']:.2f}")
    
    # Line items
    line_items, items_debug = _extract_line_items(text)
    debug_info["line_items"] = items_debug
    if not line_items:
        warnings.append("No line items extracted")
    
    # Footnotes
    footnotes = _extract_footnotes(text)
    
    # Raw text snippet near total
    snippet = text[:300]
    if amounts["total_amount"] and "total" in text.lower():
        # Try to get text around the total
        total_pos = text.lower().find("total")
        start = max(0, total_pos - 150)
        end = min(len(text), total_pos + 150)
        snippet = text[start:end]
    
    return {
        "document_type": doc_type,
        "vendor_name": vendor_name,
        "vendor_tax_id": vendor_tax_id,
        "buyer_name": buyer_name,
        "buyer_tax_id": buyer_tax_id,
        "document_number": doc_number,
        "po_number": po_number,
        "invoice_date": date_info["invoice_date"],
        "due_date": date_info["due_date"],
        "currency": currency,
        "total_amount": amounts["total_amount"],
        "subtotal_amount": amounts["subtotal_amount"],
        "tax_amount": amounts["tax_amount"],
        "line_items": line_items,
        "footnotes": footnotes,
        "raw_text_snippet": snippet,
        "extraction_warnings": warnings,
        "extraction_debug": debug_info
    }


def validate_po_invoice_match(po_data: Dict[str, Any], invoice_data: Dict[str, Any], 
                               config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Validate and detect discrepancies between PO and Invoice.
    
    Args:
        po_data: Parsed PO document
        invoice_data: Parsed invoice document
        config: Optional config with thresholds (qty_tolerance, price_tolerance_pct, fuzzy_threshold)
    
    Returns:
        Dict with match status and list of discrepancies
    """
    if config is None:
        config = {
            "qty_tolerance": 0,  # Exact match by default
            "price_tolerance_pct": 2.0,  # 2% tolerance
            "fuzzy_threshold": 0.8,  # 80% similarity for vendor names
            "date_range_days": 30  # 30 days for date matching
        }
    
    discrepancies = []
    match_score = 0.0
    match_method = "none"
    
    # 1. Try matching by PO number first
    if invoice_data.get("po_number") and po_data.get("document_number"):
        if invoice_data["po_number"].lower() == po_data["document_number"].lower():
            match_method = "po_number"
            match_score = 1.0
        else:
            discrepancies.append({
                "type": "po_number_mismatch",
                "severity": "high",
                "message": f"PO number mismatch: Invoice references '{invoice_data['po_number']}' but PO is '{po_data['document_number']}'"
            })
    
    # 1.5. Check if both documents have the same document number (same document uploaded twice)
    if po_data.get("document_number") and invoice_data.get("document_number"):
        if po_data["document_number"].lower() == invoice_data["document_number"].lower():
            match_method = "same_document"
            match_score = 1.0
    
    # 2. Fallback: match by vendor name + date range
    if match_method == "none":
        po_vendor = utils.normalize_name(po_data.get("vendor_name", ""))
        inv_vendor = utils.normalize_name(invoice_data.get("vendor_name", ""))
        
        if po_vendor and inv_vendor:
            if utils.fuzzy_match(po_vendor, inv_vendor, config["fuzzy_threshold"]):
                match_method = "vendor_name"
                match_score = 0.7
                
                # Check date range if available
                if po_data.get("invoice_date") and invoice_data.get("invoice_date"):
                    try:
                        po_date = datetime.datetime.fromisoformat(po_data["invoice_date"])
                        inv_date = datetime.datetime.fromisoformat(invoice_data["invoice_date"])
                        days_diff = abs((inv_date - po_date).days)
                        
                        if days_diff <= config["date_range_days"]:
                            match_score = 0.85
                        else:
                            discrepancies.append({
                                "type": "date_range_exceeded",
                                "severity": "medium",
                                "message": f"Invoice date is {days_diff} days from PO date (threshold: {config['date_range_days']})"
                            })
                    except:
                        pass
            else:
                discrepancies.append({
                    "type": "vendor_mismatch",
                    "severity": "high",
                    "message": f"Vendor name mismatch: PO='{po_data.get('vendor_name')}' vs Invoice='{invoice_data.get('vendor_name')}'"
                })
    
    # 3. Currency check
    if po_data.get("currency") and invoice_data.get("currency"):
        if po_data["currency"] != invoice_data["currency"]:
            discrepancies.append({
                "type": "currency_mismatch",
                "severity": "high",
                "message": f"Currency mismatch: PO={po_data['currency']} vs Invoice={invoice_data['currency']}"
            })
    
    # 4. Line item validation
    po_items = po_data.get("line_items", [])
    inv_items = invoice_data.get("line_items", [])
    
    if po_items and inv_items:
        # Try to match line items by description
        for po_item in po_items:
            po_desc = po_item.get("description", "").lower()
            matched = False
            
            for inv_item in inv_items:
                inv_desc = inv_item.get("description", "").lower()
                
                # Fuzzy match descriptions
                if utils.fuzzy_match(po_desc, inv_desc, 0.7):
                    matched = True
                    
                    # Check quantity
                    po_qty = po_item.get("quantity")
                    inv_qty = inv_item.get("quantity")
                    if po_qty is not None and inv_qty is not None:
                        if abs(po_qty - inv_qty) > config["qty_tolerance"]:
                            discrepancies.append({
                                "type": "quantity_mismatch",
                                "severity": "medium",
                                "item": po_desc,
                                "message": f"Quantity mismatch for '{po_desc[:30]}': PO={po_qty} vs Invoice={inv_qty}"
                            })
                    
                    # Check unit price
                    po_price = po_item.get("unit_price")
                    inv_price = inv_item.get("unit_price")
                    if po_price is not None and inv_price is not None:
                        price_diff_pct = abs(po_price - inv_price) / po_price * 100
                        if price_diff_pct > config["price_tolerance_pct"]:
                            discrepancies.append({
                                "type": "price_mismatch",
                                "severity": "medium",
                                "item": po_desc,
                                "message": f"Price mismatch for '{po_desc[:30]}': PO={po_price} vs Invoice={inv_price} ({price_diff_pct:.1f}% diff)"
                            })
                    
                    break
            
            if not matched:
                discrepancies.append({
                    "type": "item_not_in_invoice",
                    "severity": "low",
                    "item": po_desc,
                    "message": f"PO item '{po_desc[:30]}' not found in invoice"
                })
    
    # 5. Total amount validation
    po_total = po_data.get("total_amount")
    inv_total = invoice_data.get("total_amount")
    
    if po_total is not None and inv_total is not None:
        total_diff_pct = abs(po_total - inv_total) / po_total * 100
        if total_diff_pct > config["price_tolerance_pct"]:
            discrepancies.append({
                "type": "total_mismatch",
                "severity": "high",
                "message": f"Total amount mismatch: PO={po_total} vs Invoice={inv_total} ({total_diff_pct:.1f}% diff)"
            })
    
    # 6. Check invoice total vs computed sum
    if inv_items and invoice_data.get("total_amount"):
        computed_subtotal = sum(item.get("line_total", 0) or 0 for item in inv_items)
        inv_tax = invoice_data.get("tax_amount", 0) or 0
        computed_total = computed_subtotal + inv_tax
        
        if computed_total > 0:
            diff_pct = abs(computed_total - invoice_data["total_amount"]) / invoice_data["total_amount"] * 100
            if diff_pct > 5:  # 5% tolerance for rounding
                discrepancies.append({
                    "type": "total_computation_mismatch",
                    "severity": "medium",
                    "message": f"Invoice total ({invoice_data['total_amount']}) doesn't match computed sum ({computed_total:.2f})"
                })
    
    return {
        "matched": match_score > 0.5,
        "match_method": match_method,
        "match_score": match_score,
        "discrepancies": discrepancies,
        "discrepancy_count": len(discrepancies),
        "high_severity_count": len([d for d in discrepancies if d.get("severity") == "high"]),
        "config_used": config
    }
