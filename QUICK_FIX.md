# ⚡ Quick Fix for PDF Upload Issues

## The Problem
PDFs uploaded through the website show discrepancies even when they match.

## The Solution (3 Steps)

### Step 1: Install Poppler
```bash
brew install poppler
```

### Step 2: Install Python Packages
```bash
pip install PyPDF2 pdf2image
```

### Step 3: Restart Application
```bash
./start_dev.sh
```

## That's It!

Your PDF uploads should now work correctly. The system will properly extract text from PDFs and matching documents will show no discrepancies.

## Verify It Worked

```bash
# Check poppler is installed
which pdfinfo

# Should show a path like: /opt/homebrew/bin/pdfinfo
```

## Alternative: Use Images

If you can't install poppler, convert PDFs to PNG/JPG and upload those instead.

---

**See PDF_UPLOAD_FIX.md for detailed troubleshooting.**
