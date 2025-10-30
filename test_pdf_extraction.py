"""
Test PDF text extraction to debug OCR issues
"""
from app import ocr

# Test with sample text (simulating what OCR should extract)
print("=" * 80)
print("PDF TEXT EXTRACTION TEST")
print("=" * 80)

# Simulate PDF content
sample_pdf_text = """
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

Item            Quantity    Unit Price      Total
Laptop          10          $800.00         $8000.00
Mouse           10          $25.00          $250.00

SUBTOTAL: $8250.00
TAX (8%): $660.00
TOTAL: $8910.00
"""

print("\n📄 Sample Text (what should be extracted):")
print("-" * 80)
print(sample_pdf_text)

# Test extraction
from app.extractor import parse_document

print("\n🔍 Parsing extracted text...")
print("-" * 80)

parsed = parse_document(sample_pdf_text)

print(f"\nDocument Type: {parsed['document_type']}")
print(f"Vendor Name: {parsed['vendor_name']}")
print(f"Document Number: {parsed['document_number']}")
print(f"Total Amount: ${parsed['total_amount']}")
print(f"Currency: {parsed['currency']}")
print(f"Line Items: {len(parsed['line_items'])} items")

if parsed['line_items']:
    print("\nLine Items:")
    for item in parsed['line_items']:
        print(f"  - {item['description']}: {item['quantity']} x ${item['unit_price']} = ${item['line_total']}")

if parsed['extraction_warnings']:
    print("\n⚠️  Warnings:")
    for warning in parsed['extraction_warnings']:
        print(f"  - {warning}")

print("\n" + "=" * 80)
print("✅ If you see proper extraction above, the logic is working.")
print("   The issue is likely with PDF OCR quality or file format.")
print("=" * 80)

# Provide recommendations
print("\n💡 RECOMMENDATIONS:")
print("-" * 80)
print("1. Ensure PDFs are text-based (not scanned images)")
print("2. If PDFs are scanned, ensure high quality (300+ DPI)")
print("3. Check that poppler-utils is installed for pdf2image:")
print("   macOS: brew install poppler")
print("   Linux: sudo apt-get install poppler-utils")
print("4. Try uploading as PNG/JPG images instead of PDF")
print("5. Check the OCR output in the backend logs")
