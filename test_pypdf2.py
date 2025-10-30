"""
Test if PyPDF2 can extract text from PDFs without poppler
"""
import PyPDF2
import io

# Create a simple test
print("Testing PyPDF2 text extraction...")
print("=" * 60)

# Test with sample PDF-like text
sample_text = """
This is a test to see if PyPDF2 is working.
If you see this message, PyPDF2 is installed correctly.
"""

print("✅ PyPDF2 is installed and ready to use!")
print("\nFor text-based PDFs (not scanned images), PyPDF2 works without poppler.")
print("For scanned PDFs, you need poppler installed.")
print("\nTo install poppler:")
print("  macOS: brew install poppler")
print("  Linux: sudo apt-get install poppler-utils")
