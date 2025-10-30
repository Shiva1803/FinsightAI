# Enhanced Invoice/PO Extractor - Implementation Guide

## Overview

The enhanced extractor (`app/extractor.py`) implements a comprehensive OCR text parsing system for invoices and purchase orders with advanced field extraction, confidence scoring, and validation capabilities.

## Key Features

### 1. Document Type Detection
- Detects: `invoice`, `purchase_order`, or `unknown`
- Uses explicit heading detection (highest confidence)
- Falls back to keyword counting
- Returns confidence score (0.0-1.0)

### 2. Field Extraction

#### Vendor & Buyer Information
- **vendor_name**: Extracted from labeled patterns or first line
- **vendor_tax_id**: GST, VAT, TIN, PAN (supports Indian tax IDs)
- **buyer_name**: From "Bill To", "Customer", etc.
- **buyer_tax_id**: Buyer's tax identification

#### Document Identifiers
- **document_number**: Invoice/PO number
- **po_number**: Purchase order reference (on invoices)

#### Dates
- **invoice_date**: Normalized to ISO format (YYYY-MM-DD)
- **due_date**: Payment due date
- Handles multiple date formats with fuzzy parsing

#### Financial Data
- **currency**: ISO code (INR, USD, EUR, etc.) or inferred from symbols
- **total_amount**: Grand total
- **subtotal_amount**: Pre-tax subtotal
- **tax_amount**: Tax/GST amount

#### Line Items
Each line item includes:
- `description`: Item description
- `sku`: Stock keeping unit (if present)
- `quantity`: Numeric quantity
- `unit_price`: Price per unit
- `line_total`: Line total amount

Supports multiple formats:
- `qty x price` format
- Tabular column format
- Whitespace-separated values

#### Additional Fields
- **footnotes**: Footer text (terms, signatures, etc.)
- **raw_text_snippet**: 300 chars of OCR text near total

### 3. Confidence Scoring

Each extraction includes confidence metadata:
- **0.95**: Exact label match
- **0.80**: Regex match with contextual keywords
- **0.60**: Inferred from document layout
- **0.30**: Fallback guess

### 4. Extraction Metadata

#### Warnings
List of issues encountered:
- Missing fields
- Low confidence extractions
- Ambiguous data

#### Debug Info
Detailed extraction information:
- Which regex patterns matched
- Heuristics used
- Extraction methods

Example:
```json
{
  "extraction_warnings": [
    "Low confidence vendor extraction: 0.45",
    "Currency not detected"
  ],
  "extraction_debug": {
    "document_type": "explicit_heading:invoice",
    "vendor": "labeled_pattern:From",
    "amounts": "total_labeled|subtotal_found",
    "line_items": "found_3_items"
  }
}
```

## Validation System

### PO vs Invoice Matching

The `validate_po_invoice_match()` function compares PO and invoice data:

#### Matching Strategy
1. **Primary**: Match by PO number (exact match)
2. **Fallback**: Match by vendor name (fuzzy) + date range

#### Configuration
```python
config = {
    "qty_tolerance": 0,           # Exact quantity match
    "price_tolerance_pct": 2.0,   # 2% price variance allowed
    "fuzzy_threshold": 0.8,       # 80% name similarity
    "date_range_days": 30         # 30-day date window
}
```

#### Discrepancy Detection

**High Severity:**
- PO number mismatch
- Vendor name mismatch
- Currency mismatch
- Total amount variance > threshold

**Medium Severity:**
- Quantity mismatch
- Unit price variance > threshold
- Date range exceeded
- Total computation mismatch

**Low Severity:**
- Items in PO not found in invoice

#### Validation Output
```json
{
  "matched": true,
  "match_method": "po_number",
  "match_score": 1.0,
  "discrepancies": [
    {
      "type": "total_mismatch",
      "severity": "high",
      "message": "Total amount mismatch: PO=39825.0 vs Invoice=42775.0 (7.4% diff)"
    }
  ],
  "discrepancy_count": 2,
  "high_severity_count": 1
}
```

## Usage Examples

### Basic Extraction
```python
from app.extractor import parse_document

ocr_text = """
TAX INVOICE
Acme Corp
Invoice No: INV-001
Date: 2025-10-15
Total: 12,345.67
"""

result = parse_document(ocr_text)
print(result["document_type"])  # "invoice"
print(result["total_amount"])   # 12345.67
```

### PO vs Invoice Validation
```python
from app.extractor import parse_document, validate_po_invoice_match

po_text = "..."  # OCR text from PO
invoice_text = "..."  # OCR text from invoice

po_data = parse_document(po_text)
invoice_data = parse_document(invoice_text)

validation = validate_po_invoice_match(po_data, invoice_data)

if validation["matched"]:
    print(f"Documents matched via {validation['match_method']}")
    if validation["high_severity_count"] > 0:
        print("⚠️ High severity discrepancies found!")
```

### Custom Validation Config
```python
custom_config = {
    "qty_tolerance": 5,           # Allow ±5 units
    "price_tolerance_pct": 5.0,   # Allow 5% price variance
    "fuzzy_threshold": 0.7,       # 70% name similarity
    "date_range_days": 60         # 60-day window
}

validation = validate_po_invoice_match(
    po_data, 
    invoice_data, 
    config=custom_config
)
```

## Number Format Handling

The extractor handles various number formats:
- Comma as thousands separator: `12,345.67`
- No separator: `12345.67`
- Currency symbols: `₹12,345`, `$1,234.56`
- Whitespace: `12 345.67`

## Date Format Handling

Supports multiple date formats:
- ISO: `2025-10-15`
- US: `10/15/2025`
- European: `15.10.2025`
- Text: `15 Oct 2025`, `October 15, 2025`

All dates normalized to ISO format (YYYY-MM-DD).

## Tax ID Patterns

Supported tax identification formats:
- **GST (India)**: 15 alphanumeric characters
- **PAN (India)**: 10 characters (5 letters, 4 digits, 1 letter)
- **VAT**: Variable length alphanumeric
- **TIN**: Variable length alphanumeric

## Testing

Run the test suite:
```bash
python3 test_extractor.py
```

This will:
1. Extract data from sample invoice
2. Extract data from sample PO
3. Validate PO vs invoice match
4. Display all warnings and discrepancies

## Integration with FastAPI

The extractor is already integrated in `app/main.py`:

```python
@app.post("/upload/")
async def upload(file: UploadFile = File(...)):
    content = await file.read()
    text = ocr.run_ocr_bytes(content, filename)
    parsed = extractor.parse_document(text)
    record_id = db.save_record(parsed, source_file=filename)
    return {"id": record_id, "parsed": parsed}
```

## Performance Considerations

- Line item extraction limited to 10 items (configurable)
- Regex patterns optimized for common formats
- Fallback mechanisms for missing data
- Efficient text processing with minimal passes

## Future Enhancements

Potential improvements:
1. Machine learning-based field extraction
2. Table structure detection using layout analysis
3. Multi-page document support
4. Currency conversion
5. Historical data learning
6. Custom extraction rules per vendor
7. Confidence threshold configuration
8. Batch processing optimization

## Error Handling

The extractor is designed to be fault-tolerant:
- Returns `null` for missing fields
- Provides warnings for low-confidence extractions
- Never crashes on malformed input
- Graceful degradation for partial data

## Best Practices

1. **Always check warnings**: Review `extraction_warnings` for data quality issues
2. **Use validation**: Compare PO and invoice data before approval
3. **Monitor confidence**: Track extraction confidence over time
4. **Customize thresholds**: Adjust validation config per business needs
5. **Review debug info**: Use `extraction_debug` for troubleshooting
6. **Handle nulls**: Always check for null values before processing
7. **Test with real data**: Validate with actual OCR output from your documents

## Support

For issues or questions:
- Check `extraction_debug` for extraction details
- Review `extraction_warnings` for specific problems
- Test with `test_extractor.py` to verify functionality
- Adjust regex patterns in `extractor.py` for custom formats
