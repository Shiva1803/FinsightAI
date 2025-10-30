# 🚀 FinsightAI - Intelligent Invoice & Purchase Order Verification System

<div align="center">

![FinsightAI Banner](https://img.shields.io/badge/FinsightAI-AI%20Powered%20Document%20Verification-blue?style=for-the-badge)

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)

**AI-powered document verification system that detects fraud, identifies discrepancies, and automates invoice-PO matching with advanced anomaly detection.**

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Usage](#-usage) • [API](#-api-documentation) • [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Demo](#-demo)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

---

## 🎯 Overview

**FinsightAI** is a comprehensive full-stack application designed to revolutionize financial document verification. It leverages AI and machine learning to automatically compare Purchase Orders (POs) with Invoices, detect anomalies, identify potential fraud, and provide actionable insights through an intuitive dashboard.

### Why FinsightAI?

- **🔍 Automated Verification**: Eliminate manual document comparison
- **🛡️ Fraud Detection**: AI-powered anomaly detection with risk scoring
- **📊 Visual Analytics**: Interactive charts and detailed breakdowns
- **⚡ Fast Processing**: OCR-powered text extraction from PDFs and images
- **💾 Data Management**: Store, retrieve, and export verification records
- **🎨 Modern UI**: Beautiful, responsive interface with dark mode support

---

## ✨ Features

### Core Functionality

#### 🔐 Document Verification
- **Smart Comparison**: Automatically compare PO and Invoice documents
- **Field Matching**: Verify vendor names, amounts, quantities, prices, and dates
- **Discrepancy Detection**: Identify mismatches with severity levels (Low, Medium, High)
- **Risk Scoring**: Calculate risk scores (0-10) based on anomaly patterns

#### 🤖 AI-Powered Anomaly Detection
- **Overbilling Detection**: Identify when invoice amounts exceed PO amounts
- **Price Manipulation**: Detect altered unit prices
- **Vendor Fraud**: Flag vendor name mismatches
- **Quantity Discrepancies**: Spot quantity differences in line items
- **Tax Anomalies**: Identify tax calculation errors
- **Historical Patterns**: Track vendor anomaly history

#### 📄 OCR & Document Processing
- **Multi-Format Support**: Process PDF, PNG, JPG, JPEG files
- **Tesseract OCR**: Extract text from scanned documents
- **Smart Parsing**: Automatically extract vendor, amounts, dates, line items
- **Confidence Scoring**: Assess extraction quality

#### 📊 Visual Analytics
- **Bar Charts**: Compare PO vs Invoice totals
- **Pie Charts**: Discrepancy breakdown by category
- **Line Item Tables**: Detailed item-by-item comparison
- **Timeline Views**: Track document lifecycle
- **Risk Indicators**: Visual risk score displays

#### 💼 Data Management
- **Record Storage**: SQLite database for all verifications
- **CSV Export**: Export records for external analysis
- **Search & Filter**: Find specific verifications quickly
- **Bulk Operations**: Process multiple documents

### User Interface

- **🎨 Modern Design**: Clean, professional interface with Tailwind CSS
- **🌓 Dark Mode**: Full dark mode support
- **📱 Responsive**: Works on desktop, tablet, and mobile
- **🎭 Animations**: Smooth transitions with Framer Motion
- **🎯 Intuitive Navigation**: Easy-to-use multi-page layout

---

## 🎬 Demo

### Dashboard Overview
View key metrics, recent verifications, and system health at a glance.

### Document Upload
Drag-and-drop interface for uploading PO and Invoice documents.

### Verification Results
Comprehensive verification report with:
- Risk score and discrepancy level
- Vendor, amount, and quantity matching
- Anomaly insights and fraud indicators
- Interactive charts and visualizations
- Detailed line item comparison

### Records Management
Browse all verification records, view details, and export to CSV.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (React)                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Dashboard │  │  Upload  │  │  Verify  │  │ Records  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                         │                                    │
│                    Axios API Client                          │
└─────────────────────────┬───────────────────────────────────┘
                          │ HTTP/REST
┌─────────────────────────▼───────────────────────────────────┐
│                    Backend (FastAPI)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ OCR Engine   │  │  Extractor   │  │ Verification │     │
│  │ (Tesseract)  │  │   Parser     │  │    Agent     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                         │                                    │
│                    ┌────▼─────┐                             │
│                    │ Database │                             │
│                    │ (SQLite) │                             │
│                    └──────────┘                             │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Upload**: User uploads PO and Invoice files
2. **OCR**: Tesseract extracts text from documents
3. **Parse**: Extractor parses structured data (vendor, amounts, items)
4. **Verify**: Verification Agent compares documents and detects anomalies
5. **Analyze**: Risk scoring and fraud pattern detection
6. **Visualize**: Generate charts and comparison tables
7. **Store**: Save results to database
8. **Display**: Present results in interactive dashboard

---

## 🛠️ Tech Stack

### Frontend
- **React 18** - UI library
- **TypeScript** - Type-safe JavaScript
- **Vite** - Fast build tool
- **Tailwind CSS** - Utility-first CSS framework
- **Framer Motion** - Animation library
- **Recharts** - Chart library
- **React Router** - Client-side routing
- **Axios** - HTTP client
- **Lucide React** - Icon library

### Backend
- **FastAPI** - Modern Python web framework
- **Python 3.11+** - Programming language
- **Tesseract OCR** - Text extraction engine
- **SQLModel** - SQL database ORM
- **SQLite** - Embedded database
- **Pillow** - Image processing
- **PyPDF2** - PDF manipulation
- **Pandas** - Data analysis
- **Uvicorn** - ASGI server

### Development Tools
- **ESLint** - JavaScript linter
- **TypeScript Compiler** - Type checking
- **Autoprefixer** - CSS vendor prefixes
- **PostCSS** - CSS transformation

---

## 📦 Installation

### Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** (v18 or higher) - [Download](https://nodejs.org/)
- **Python** (v3.11 or higher) - [Download](https://www.python.org/)
- **Tesseract OCR** - [Installation Guide](https://github.com/tesseract-ocr/tesseract)
- **Git** - [Download](https://git-scm.com/)

#### Install Tesseract OCR

**macOS:**
```bash
brew install tesseract
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

**Windows:**
Download installer from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

### Clone Repository

```bash
git clone https://github.com/Shiva1803/FinsightAI.git
cd FinsightAI
```

### Backend Setup

1. **Create Virtual Environment**
```bash
python -m venv venv
```

2. **Activate Virtual Environment**

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Verify Installation**
```bash
python -c "import pytesseract; print('Tesseract OK')"
```

### Frontend Setup

1. **Navigate to Frontend**
```bash
cd frontend
```

2. **Install Dependencies**
```bash
npm install
```

3. **Return to Root**
```bash
cd ..
```

---

## 🚀 Usage

### Quick Start (Recommended)

Use the provided startup script to launch both frontend and backend:

```bash
./start_dev.sh
```

This will:
- Start the backend server on `http://localhost:8000`
- Start the frontend dev server on `http://localhost:5173`
- Open your browser automatically

### Manual Start

#### Start Backend
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

#### Start Frontend (in another terminal)
```bash
cd frontend
npm run dev
```

### Access Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health/

---

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Upload Document
```http
POST /upload/
```
Upload and extract data from a single document.

**Request:**
- Content-Type: `multipart/form-data`
- Body: `file` (PDF/Image)

**Response:**
```json
{
  "id": 1,
  "parsed": {
    "vendor_name": "AlphaTech Supplies Ltd.",
    "document_number": "PO-2045",
    "total_amount": 613010,
    "line_items": [...]
  }
}
```

#### 2. Verify Documents
```http
POST /verify/
```
Compare PO and Invoice for discrepancies.

**Request:**
- Content-Type: `multipart/form-data`
- Body: 
  - `po_file` (PDF/Image)
  - `invoice_file` (PDF/Image)

**Response:**
```json
{
  "verification_summary": {
    "vendor_match": false,
    "total_match": true,
    "amount_difference": 0,
    "discrepancy_level": "high",
    "risk_score": 6.5,
    "needs_review": true
  },
  "anomaly_insights": {
    "anomaly_detected": true,
    "anomaly_types": ["vendor_mismatch"],
    "risk_score": 6.5,
    "fraud_indicators": [...]
  },
  "visualization_data": {
    "bar_chart": {...},
    "pie_chart": {...},
    "line_items_comparison": [...]
  }
}
```

#### 3. List Records
```http
GET /records/
```
Retrieve all verification records.

**Response:**
```json
[
  {
    "id": 1,
    "source_file": "verification_PO-2045_INV-4719",
    "parsed": {...}
  }
]
```

#### 4. Delete Record
```http
DELETE /records/{record_id}
```
Delete a specific record.

**Response:**
```json
{
  "message": "Record deleted successfully"
}
```

#### 5. Export CSV
```http
GET /export/
```
Export all records to CSV file.

**Response:** CSV file download

#### 6. Health Check
```http
GET /health/
```
Check API health status.

**Response:**
```json
{
  "status": "ok"
}
```

### Interactive API Documentation

FastAPI provides automatic interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📁 Project Structure

```
FinsightAI/
├── app/                          # Backend application
│   ├── __init__.py
│   ├── main.py                   # FastAPI app & routes
│   ├── ocr.py                    # OCR processing
│   ├── extractor.py              # Document parsing
│   ├── verification_agent.py     # Verification logic
│   ├── db.py                     # Database operations
│   ├── utils.py                  # Utility functions
│   ├── email_watcher.py          # Email monitoring
│   └── shivaay_client.py         # External API client
│
├── frontend/                     # Frontend application
│   ├── public/                   # Static assets
│   ├── src/
│   │   ├── components/           # React components
│   │   │   ├── FileUpload.tsx
│   │   │   ├── Layout.tsx
│   │   │   ├── Preloader.tsx
│   │   │   ├── SplashScreen.tsx
│   │   │   └── ThemeToggle.tsx
│   │   ├── hooks/                # Custom React hooks
│   │   │   └── useDistortionEffect.ts
│   │   ├── pages/                # Page components
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Home.tsx
│   │   │   ├── Records.tsx
│   │   │   ├── UploadDocument.tsx
│   │   │   └── VerifyDocuments.tsx
│   │   ├── services/             # API services
│   │   │   └── api.ts
│   │   ├── types/                # TypeScript types
│   │   │   └── index.ts
│   │   ├── App.tsx               # Main app component
│   │   ├── main.tsx              # Entry point
│   │   └── index.css             # Global styles
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── tailwind.config.js
│
├── uploads/                      # Uploaded files storage
├── venv/                         # Python virtual environment
├── tests/                        # Test files
│   ├── test_api_verify.py
│   ├── test_verification_agent.py
│   └── ...
│
├── futurix.db                    # SQLite database
├── requirements.txt              # Python dependencies
├── start_dev.sh                  # Startup script
├── restart_backend.sh            # Backend restart script
├── README.md                     # This file
├── SETUP.md                      # Detailed setup guide
└── VERIFICATION_500_FIX.md       # Troubleshooting guide
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

```bash
# Optional: External API Configuration
SHIVAAY_API_KEY=your-api-key-here
SHIVAAY_API_URL=https://api.shivaay.com/extract

# Optional: Database Configuration
DATABASE_URL=sqlite:///./futurix.db

# Optional: CORS Origins
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Frontend Configuration

Edit `frontend/vite.config.ts` to configure the development server:

```typescript
export default defineConfig({
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})
```

### Backend Configuration

Edit `app/main.py` to configure CORS and other settings:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🧪 Testing

### Run All Tests

```bash
source venv/bin/activate
python -m pytest
```

### Run Specific Tests

**Verification Tests:**
```bash
python test_api_verify.py
```

**OCR Tests:**
```bash
python test_pdf_extraction.py
```

**Verification Agent Tests:**
```bash
python test_verification_agent.py
```

### Test Coverage

The project includes comprehensive tests for:
- ✅ OCR text extraction
- ✅ Document parsing
- ✅ Verification logic
- ✅ Anomaly detection
- ✅ Database operations
- ✅ API endpoints

---

## 🚢 Deployment

### Backend Deployment

#### Using Docker (Recommended)

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y tesseract-ocr

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t finsightai-backend .
docker run -p 8000:8000 finsightai-backend
```

#### Using Heroku

```bash
heroku create finsightai-backend
git push heroku main
```

### Frontend Deployment

#### Build for Production

```bash
cd frontend
npm run build
```

#### Deploy to Vercel

```bash
npm install -g vercel
vercel --prod
```

#### Deploy to Netlify

```bash
npm install -g netlify-cli
netlify deploy --prod
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Tesseract Not Found
**Error:** `TesseractNotFoundError`

**Solution:**
```bash
# macOS
brew install tesseract

# Ubuntu
sudo apt-get install tesseract-ocr

# Verify installation
tesseract --version
```

#### 2. Port Already in Use
**Error:** `Address already in use`

**Solution:**
```bash
# Find and kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn app.main:app --port 8001
```

#### 3. Module Not Found
**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

#### 4. CORS Errors
**Error:** `Access-Control-Allow-Origin`

**Solution:** Check `app/main.py` CORS configuration matches your frontend URL.

#### 5. 500 Internal Server Error
**Solution:** Check backend logs for detailed error messages. See `VERIFICATION_500_FIX.md` for specific verification errors.

### Getting Help

- 📖 Check [SETUP.md](SETUP.md) for detailed setup instructions
- 🐛 Check [Issues](https://github.com/Shiva1803/FinsightAI/issues) for known problems
- 💬 Open a new issue if you need help

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### How to Contribute

1. **Fork the Repository**
```bash
git clone https://github.com/Shiva1803/FinsightAI.git
```

2. **Create a Branch**
```bash
git checkout -b feature/amazing-feature
```

3. **Make Changes**
- Write clean, documented code
- Follow existing code style
- Add tests for new features

4. **Commit Changes**
```bash
git commit -m "Add amazing feature"
```

5. **Push to Branch**
```bash
git push origin feature/amazing-feature
```

6. **Open Pull Request**
- Describe your changes
- Reference any related issues

### Development Guidelines

- **Code Style**: Follow PEP 8 for Python, ESLint rules for TypeScript
- **Documentation**: Update README and inline comments
- **Testing**: Add tests for new features
- **Commits**: Use clear, descriptive commit messages

### Areas for Contribution

- 🐛 Bug fixes
- ✨ New features
- 📝 Documentation improvements
- 🎨 UI/UX enhancements
- 🧪 Additional tests
- 🌐 Internationalization

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Contact

**Shresth Panigrahi**

- GitHub: [@Shiva1803](https://github.com/Shiva1803)
- Project Link: [https://github.com/Shiva1803/FinsightAI](https://github.com/Shiva1803/FinsightAI)

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [React](https://reactjs.org/) - UI library
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) - OCR engine
- [Tailwind CSS](https://tailwindcss.com/) - CSS framework
- [Recharts](https://recharts.org/) - Chart library

---

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/Shiva1803/FinsightAI?style=social)
![GitHub forks](https://img.shields.io/github/forks/Shiva1803/FinsightAI?style=social)
![GitHub issues](https://img.shields.io/github/issues/Shiva1803/FinsightAI)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Shiva1803/FinsightAI)

---

<div align="center">

**Made with ❤️ by Shresth Panigrahi**

⭐ Star this repo if you find it helpful!

</div>
