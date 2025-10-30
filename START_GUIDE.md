# 🚀 FinsightAI - Quick Start Guide

## Prerequisites

Before starting, make sure you have:
- **Python 3.8+** installed
- **Node.js 16+** and npm installed
- **Git** (if cloning from repository)

## 📋 First Time Setup

### 1. Backend Setup (Python/FastAPI)

```bash
# Create and activate virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Frontend Setup (React/Vite)

```bash
# Navigate to frontend directory
cd frontend

# Install Node dependencies
npm install

# Go back to root directory
cd ..
```

### 3. Add Your Logo (Optional)

Place your logo image as `logo.png` in the `frontend/public/` folder for it to appear on the homepage and splash screen.

## 🎯 Starting the Project

### Option 1: Using the Start Script (Recommended - macOS/Linux)

```bash
# Make the script executable (first time only)
chmod +x start_dev.sh

# Run the script
./start_dev.sh
```

This will automatically:
- ✅ Check if dependencies are installed
- ✅ Start the backend server (FastAPI) on port 8000
- ✅ Start the frontend server (Vite) on port 5173
- ✅ Display all URLs and status

### Option 2: Manual Start (All Platforms)

**Terminal 1 - Backend:**
```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Start backend
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
# Navigate to frontend
cd frontend

# Start frontend
npm run dev
```

## 🌐 Access Your Application

Once both servers are running:

- **🏠 Homepage**: http://localhost:5173
- **📊 Dashboard**: http://localhost:5173/dashboard
- **📄 API Documentation**: http://localhost:8000/docs
- **💚 Health Check**: http://localhost:8000/health/

## 🎨 Application Flow

1. **Splash Screen** → Click "Get Started"
2. **Preloader** → Animated loading (3 seconds)
3. **Homepage** → Interactive landing page with features
4. **Dashboard** → Main application interface

## 🛠️ Development Commands

### Backend Commands
```bash
# Run backend with auto-reload
uvicorn app.main:app --reload

# Run on different port
uvicorn app.main:app --reload --port 8080

# Run tests
pytest

# Check API health
curl http://localhost:8000/health/
```

### Frontend Commands
```bash
cd frontend

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run linter
npm run lint
```

## 📁 Project Structure

```
futurix_mvp_shivaay/
├── app/                    # Backend (FastAPI)
│   ├── main.py            # API entry point
│   ├── ocr.py             # OCR processing
│   └── db.py              # Database operations
├── frontend/              # Frontend (React + Vite)
│   ├── src/
│   │   ├── pages/         # Page components
│   │   ├── components/    # Reusable components
│   │   └── services/      # API services
│   └── public/            # Static assets (put logo.png here)
├── uploads/               # Uploaded documents
├── venv/                  # Python virtual environment
├── requirements.txt       # Python dependencies
└── start_dev.sh          # Startup script
```

## 🎯 Key Features

### Homepage Features
- ✨ Framer Motion animations
- 🌓 Light/Dark mode toggle
- 📱 Fully responsive design
- 🎨 Interactive hover effects
- 📊 Animated statistics
- 🎭 WebGL logo effects

### Dashboard Features
- 📤 Document upload (drag & drop)
- 🔍 Invoice verification
- 📊 Real-time analytics
- 📋 Records management
- 💾 CSV export functionality

## 🐛 Troubleshooting

### Backend Issues

**Port already in use:**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

**Missing dependencies:**
```bash
pip install -r requirements.txt
```

### Frontend Issues

**Port already in use:**
```bash
# Kill process on port 5173
lsof -ti:5173 | xargs kill -9
```

**Missing dependencies:**
```bash
cd frontend
npm install
```

**Build errors:**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

## 🔄 Stopping the Application

### If using start_dev.sh:
Press `Ctrl+C` in the terminal - it will automatically stop both servers

### If running manually:
Press `Ctrl+C` in each terminal window

## 📝 Environment Variables (Optional)

Create a `.env` file in the root directory:

```env
# Backend
DATABASE_URL=sqlite:///./finsight.db
UPLOAD_DIR=./uploads

# Frontend (create frontend/.env)
VITE_API_URL=http://localhost:8000
```

## 🎉 You're All Set!

Your FinsightAI application should now be running with:
- Beautiful animated homepage
- Interactive dashboard
- AI-powered document processing
- Real-time verification

Enjoy building with FinsightAI! 🚀
