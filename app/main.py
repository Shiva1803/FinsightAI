from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil, os, io, csv, datetime, json
from . import ocr, extractor, db, email_watcher, utils
from .shivaay_client import send_extraction_request, map_shivaay_to_output
from .verification_agent import VerificationAgent, verify_from_text, verify_from_parsed

app = FastAPI(title="Futurix AI - Invoice/PO Verifier (MVP) - Shivaay")

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload/")
async def upload(file: UploadFile = File(...)):
    content = await file.read()
    # Save file
    filename = os.path.join(UPLOAD_DIR, f"{int(datetime.datetime.utcnow().timestamp())}_{file.filename}")
    with open(filename, "wb") as f:
        f.write(content)
    # Run OCR (MVP)
    text = ocr.run_ocr_bytes(content, filename)
    parsed = extractor.parse_document(text)
    record_id = db.save_record(parsed, source_file=filename)
    return {"id": record_id, "parsed": parsed}

@app.get("/records/")
def list_records():
    return db.list_records()

@app.delete("/records/{record_id}")
def delete_record(record_id: int):
    success = db.delete_record(record_id)
    if success:
        return {"message": "Record deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Record not found")

@app.get("/export/")
def export_csv():
    path = db.export_csv()
    return FileResponse(path, filename="futurix_export.csv")

@app.post("/email/watch/start/")
def start_email_watch(
    imap_host: str = Form(...),
    imap_user: str = Form(...),
    imap_pass: str = Form(...),
    check_interval: int = Form(60)
):
    """Start email watcher to monitor mailbox for new documents"""
    result = email_watcher.start_watcher(imap_host, imap_user, imap_pass, check_interval)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.post("/email/watch/stop/")
def stop_email_watch():
    """Stop the email watcher"""
    result = email_watcher.stop_watcher()
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.get("/email/watch/status/")
def get_email_watch_status():
    """Get email watcher status and statistics"""
    return email_watcher.get_watcher_status()

@app.get("/health/")
def health():
    return {"status":"ok"}

@app.post("/verify/")
async def verify_documents(
    po_file: UploadFile = File(None),
    invoice_file: UploadFile = File(None),
    po_text: str = Form(None),
    invoice_text: str = Form(None)
):
    """
    Verify PO vs Invoice using Futurix AI Verification Agent
    
    Accepts either:
      - Both files (po_file + invoice_file) -> runs OCR -> verifies
      - Both texts (po_text + invoice_text) -> verifies directly
    
    Returns:
      Complete verification JSON with summary, anomalies, and visualization data
    """
    # Get PO data
    if po_file:
        po_content = await po_file.read()
        po_ocr_text = ocr.run_ocr_bytes(po_content, po_file.filename)
        po_filename = po_file.filename
        
        # Check for OCR errors
        if po_ocr_text.startswith("ERROR:"):
            raise HTTPException(status_code=500, detail=f"PO OCR failed: {po_ocr_text}")
    elif po_text:
        po_ocr_text = po_text
        po_filename = "PO.txt"
    else:
        raise HTTPException(status_code=400, detail="Provide either po_file or po_text")
    
    # Get Invoice data
    if invoice_file:
        inv_content = await invoice_file.read()
        inv_ocr_text = ocr.run_ocr_bytes(inv_content, invoice_file.filename)
        inv_filename = invoice_file.filename
        
        # Check for OCR errors
        if inv_ocr_text.startswith("ERROR:"):
            raise HTTPException(status_code=500, detail=f"Invoice OCR failed: {inv_ocr_text}")
    elif invoice_text:
        inv_ocr_text = invoice_text
        inv_filename = "Invoice.txt"
    else:
        raise HTTPException(status_code=400, detail="Provide either invoice_file or invoice_text")
    
    # Run verification
    try:
        result = verify_from_text(po_ocr_text, inv_ocr_text, po_filename, inv_filename)
    except Exception as e:
        print(f"ERROR in verification: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Verification failed: {str(e)}")
    
    # Save complete verification result to database
    try:
        # Create a clean copy for database storage (remove any non-serializable data)
        db_result = {
            "verification_summary": result.get("verification_summary"),
            "anomaly_insights": result.get("anomaly_insights"),
            "visualization_data": result.get("visualization_data"),
            "verified_by": result.get("verified_by"),
            "timestamp": result.get("timestamp"),
            "po_file": result.get("po_file"),
            "invoice_file": result.get("invoice_file")
        }
        record_id = db.save_record(db_result, source_file=f"verification_{po_filename}_{inv_filename}")
        result["record_id"] = record_id
    except Exception as e:
        # Don't fail if DB save fails, just log it
        print(f"Warning: Failed to save verification record: {e}")
        import traceback
        traceback.print_exc()
    
    # Ensure result is JSON serializable before returning
    try:
        json.dumps(result)
    except Exception as e:
        print(f"ERROR: Result is not JSON serializable: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Result serialization failed: {str(e)}")
    
    return JSONResponse(content=result)

@app.post("/verify/parsed/")
async def verify_parsed_documents(po_data: dict, invoice_data: dict):
    """
    Verify already-parsed PO and Invoice data
    
    Accepts:
      - po_data: Parsed PO document (from /upload/ or /extract/shivaay/)
      - invoice_data: Parsed invoice document
    
    Returns:
      Complete verification JSON
    """
    result = verify_from_parsed(po_data, invoice_data)
    return JSONResponse(content=result)

@app.post("/extract/shivaay/")
async def extract_shivaay(file: UploadFile = File(None), ocr_text: str = Form(None)):
    """
    Accepts either:
      - file upload (image/pdf) -> runs local OCR -> sends OCR text to Shivaay
      - or direct ocr_text (form field) -> sends directly
    """
    if file is not None:
        content = await file.read()
        text = ocr.run_ocr_bytes(content, file.filename)
    elif ocr_text:
        text = ocr_text
    else:
        raise HTTPException(status_code=400, detail="Provide either file or ocr_text")

    sh_resp = await send_extraction_request(text)
    # if Shivaay returned error dict, propagate minimal info
    if isinstance(sh_resp, dict) and sh_resp.get("error"):
        return {"shivaay_error": sh_resp}

    mapped = map_shivaay_to_output(sh_resp, text)
    # save mapped result to DB
    record_id = db.save_record(mapped, source_file="shivaay:live")
    mapped["record_id"] = record_id
    return mapped

@app.post("/extract/ai/")
async def extract_with_ai_endpoint(
    file: UploadFile = File(None),
    ocr_text: str = Form(None),
    provider: str = Form(None)
):
    """
    AI-powered extraction with automatic fallback
    
    Accepts:
      - file: PDF or image file
      - ocr_text: Pre-extracted OCR text
      - provider: Specific AI provider (openai, shivaay, local)
    
    Returns:
      Extracted structured data with provider info
    """
    from .ai_extractor import extract_with_ai
    
    # Get OCR text
    if file is not None:
        content = await file.read()
        text = ocr.run_ocr_bytes(content, file.filename)
        filename = file.filename
    elif ocr_text:
        text = ocr_text
        filename = "text_input"
    else:
        raise HTTPException(status_code=400, detail="Provide either file or ocr_text")
    
    # Check for OCR errors
    if text.startswith("ERROR:"):
        raise HTTPException(status_code=500, detail=f"OCR failed: {text}")
    
    # Extract with AI
    try:
        result = await extract_with_ai(text, provider=provider)
        
        if not result["success"]:
            raise HTTPException(
                status_code=500,
                detail=f"AI extraction failed: {result.get('error')}"
            )
        
        # Save to database
        extracted_data = result["data"]
        record_id = db.save_record(extracted_data, source_file=f"ai:{result['provider']}:{filename}")
        
        return {
            "success": True,
            "provider": result["provider"],
            "record_id": record_id,
            "data": extracted_data
        }
        
    except Exception as e:
        print(f"ERROR in AI extraction: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")

@app.get("/ai/status/")
def get_ai_status():
    """Get status of AI providers"""
    from .ai_extractor import get_provider_status
    return get_provider_status()
