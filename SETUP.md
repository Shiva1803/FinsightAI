# Futurix AI - Setup Guide

## Quick Start

### 1. Install System Dependencies

**macOS:**
```bash
brew install poppler tesseract
```

**Ubuntu/Linux:**
```bash
sudo apt-get update
sudo apt-get install poppler-utils tesseract-ocr
```

**Windows:**
- Install poppler from: https://github.com/oschwartz10612/poppler-windows/releases
- Install Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki

### 2. Install Python & Node Dependencies

```bash
# Backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend
cd frontend
npm install
cd ..
```

### 2. Start Application

```bash
# Make script executable (first time only)
chmod +x start_dev.sh

# Start both servers
./start_dev.sh
```

### 3. Access Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Manual Start (Alternative)

**Terminal 1 - Backend:**
```bash
source venv/bin/activate
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## Supported File Formats

Upload invoices and purchase orders in:
- **PDF (.pdf)** - Requires poppler-utils installed
- **Images**: PNG, JPG, JPEG, GIF, BMP, TIFF

**Important:** For PDF support, you must install poppler-utils:
```bash
brew install poppler  # macOS
sudo apt-get install poppler-utils  # Linux
```

See **PDF_UPLOAD_FIX.md** for detailed PDF setup instructions.

## Features

- **Dashboard** - System overview and statistics
- **Verify Documents** - Compare PO vs Invoice with risk scoring
- **Upload Document** - Extract data from single document
- **Records** - Browse and export all processed documents

## Troubleshooting

**Port already in use:**
```bash
lsof -ti:3000 | xargs kill -9  # Frontend
lsof -ti:8000 | xargs kill -9  # Backend
```

**Frontend won't start:**
```bash
cd frontend
rm -rf node_modules
npm install
```

## Documentation

- **README.md** - Original backend documentation
- **VERIFICATION_FIX.md** - Recent verification logic fix
- **QUICK_REFERENCE.md** - Backend API reference
- **frontend/README.md** - Frontend documentation
