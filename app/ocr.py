# MVP OCR wrappers. For real OCR, install tesseract on system.
from PIL import Image
import pytesseract
import io, os

def run_ocr_bytes(content: bytes, filename_hint: str = "file"):
    """
    Extract text from image or PDF files using OCR
    """
    # Check if it's a PDF
    if filename_hint.lower().endswith('.pdf') or content[:4] == b'%PDF':
        # Try PyPDF2 first (works without poppler)
        try:
            import PyPDF2
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
            text_parts = []
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text.strip():  # Only add non-empty pages
                    text_parts.append(page_text)
            
            if text_parts:
                return '\n\n'.join(text_parts)
            else:
                # No text extracted, try OCR method
                raise Exception("No text found in PDF, trying OCR")
                
        except Exception as e:
            # PyPDF2 failed or no text, try pdf2image + OCR
            try:
                import pdf2image
                
                # Convert PDF to images
                images = pdf2image.convert_from_bytes(content)
                
                # OCR each page and combine
                text_parts = []
                for img in images:
                    page_text = pytesseract.image_to_string(img)
                    text_parts.append(page_text)
                
                return '\n\n'.join(text_parts)
            except ImportError:
                return "ERROR: PDF processing failed. Install poppler for scanned PDFs: brew install poppler"
            except Exception as e2:
                return f"ERROR: PDF processing failed. Install poppler: brew install poppler. Error: {str(e2)}"
    
    # Try to open as image
    try:
        img = Image.open(io.BytesIO(content))
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        # Fallback: if it's text, try to decode as utf-8
        try:
            return content.decode('utf-8', errors='ignore')
        except Exception:
            return f"ERROR: Failed to process file: {str(e)}"
