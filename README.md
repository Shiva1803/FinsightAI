# Futurix AI - Invoice & Purchase Order Verification System

Complete fullstack application for intelligent document verification with AI-powered anomaly detection.

## Features

- **OCR Processing** - Extract text from PDF and image documents
- **Smart Extraction** - Parse vendor, amounts, dates, line items
- **Verification Engine** - Compare PO vs Invoice with risk scoring
- **Anomaly Detection** - Identify fraud patterns and overbilling
- **Visual Analytics** - Interactive charts and comparison tables
- **Data Export** - Export records to CSV

## Tech Stack

**Frontend:** React 18 + TypeScript + Vite + Tailwind CSS  
**Backend:** FastAPI + Python + Tesseract OCR + SQLite

## Quick Start

```bash
# 1. Install dependencies
cd frontend && npm install && cd ..

# 2. Start application
./start_dev.sh

# 3. Open browser
# http://localhost:3000
```

See **SETUP.md** for detailed instructions.

## API Endpoints

- `POST /upload/` - Upload and extract document
- `POST /verify/` - Verify PO vs Invoice
- `POST /extract/shivaay/` - Extract using Shivaay API
- `GET /records/` - List all records
- `GET /export/` - Export CSV
- `GET /health/` - Health check

## Environment Variables

```bash
SHIVAAY_API_KEY=your-api-key
SHIVAAY_API_URL=https://api.shivaay.com/extract
```

## Documentation

- **SETUP.md** - Setup and installation guide
- **VERIFICATION_FIX.md** - Recent verification logic fix
- **QUICK_REFERENCE.md** - API reference
- **frontend/README.md** - Frontend documentation
