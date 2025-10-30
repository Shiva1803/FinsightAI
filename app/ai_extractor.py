"""
AI-Powered Document Extraction using Google Gemini
"""
import os
from typing import Dict, Any, Optional

# Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyDuYkbcwNWcw24YlvQTkwsq4KDLuMMLTyw")


async def extract_with_gemini(ocr_text: str) -> Dict[str, Any]:
    """Extract data using Google Gemini AI"""
    from .gemini_client import extract_with_gemini as gemini_extract, map_gemini_to_output
    
    try:
        result = gemini_extract(ocr_text)
        
        if result["success"]:
            # Map to standard format
            mapped_data = map_gemini_to_output(result, ocr_text)
            return {
                "success": True,
                "data": mapped_data,
                "provider": "gemini"
            }
        else:
            return {
                "success": False,
                "error": result.get("error"),
                "provider": "gemini"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "provider": "gemini"
        }


async def extract_with_local(ocr_text: str) -> Dict[str, Any]:
    """Fallback to local rule-based extraction"""
    from .extractor import parse_document
    
    try:
        result = parse_document(ocr_text)
        return {
            "success": True,
            "data": result,
            "provider": "local"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "provider": "local"
        }


async def extract_with_ai(ocr_text: str, provider: Optional[str] = None) -> Dict[str, Any]:
    """
    Main extraction function with Gemini AI and local fallback
    
    Args:
        ocr_text: OCR extracted text from document
        provider: Specific provider to use (optional)
    
    Returns:
        Dict with extraction results
    """
    # Try Gemini AI first
    print("🤖 Using Google Gemini AI for extraction...")
    result = await extract_with_gemini(ocr_text)
    
    if result["success"]:
        print("✅ Gemini AI extraction successful!")
        return result
    
    print(f"⚠️  Gemini extraction failed: {result.get('error')}")
    print("📝 Falling back to local extraction...")
    
    # Fallback to local extraction
    return await extract_with_local(ocr_text)


def get_available_providers() -> list:
    """Get list of available AI providers"""
    return ["gemini", "local"]


def get_provider_status() -> Dict[str, Any]:
    """Get status of all AI providers"""
    return {
        "current_provider": "gemini",
        "available_providers": get_available_providers(),
        "gemini_configured": True,
        "gemini_api_key": GEMINI_API_KEY[:8] + "..." if GEMINI_API_KEY else None,
        "fallback_enabled": True,
        "model": "gemini-2.5-flash"
    }
