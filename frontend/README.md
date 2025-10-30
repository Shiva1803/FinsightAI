# Futurix AI - Frontend

Modern, professional React + TypeScript frontend for the Futurix AI Invoice & Purchase Order Verification System.

## Features

- **Dashboard**: Overview of system status and recent activity
- **Document Verification**: Compare PO and Invoice with visual analytics
- **Document Upload**: Extract data from invoices and purchase orders
- **Records Management**: View and export all processed documents
- **Real-time Visualizations**: Charts and graphs for verification insights
- **Responsive Design**: Works seamlessly on desktop and mobile

## Tech Stack

- **React 18** - Modern UI library
- **TypeScript** - Type-safe development
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first styling
- **Recharts** - Data visualization
- **React Router** - Client-side routing
- **Axios** - HTTP client
- **Lucide React** - Beautiful icons

## Prerequisites

- Node.js 18+ and npm/yarn
- Backend server running on `http://localhost:8000`

## Installation

```bash
cd frontend
npm install
```

## Development

Start the development server:

```bash
npm run dev
```

The app will be available at `http://localhost:3000`

The dev server is configured to proxy API requests to `http://localhost:8000`

## Build for Production

```bash
npm run build
```

The production build will be in the `dist/` directory.

## Preview Production Build

```bash
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/       # Reusable UI components
│   │   ├── Layout.tsx
│   │   └── FileUpload.tsx
│   ├── pages/           # Page components
│   │   ├── Dashboard.tsx
│   │   ├── VerifyDocuments.tsx
│   │   ├── UploadDocument.tsx
│   │   └── Records.tsx
│   ├── services/        # API integration
│   │   └── api.ts
│   ├── types/           # TypeScript types
│   │   └── index.ts
│   ├── App.tsx          # Main app component
│   ├── main.tsx         # Entry point
│   └── index.css        # Global styles
├── public/              # Static assets
├── index.html           # HTML template
├── package.json
├── tsconfig.json
├── vite.config.ts
└── tailwind.config.js
```

## API Integration

The frontend connects to the following backend endpoints:

- `POST /upload/` - Upload and extract document data
- `POST /verify/` - Verify PO vs Invoice
- `POST /verify/parsed/` - Verify pre-parsed documents
- `POST /extract/shivaay/` - Extract using Shivaay API
- `GET /records/` - List all records
- `GET /export/` - Export records as CSV
- `GET /health/` - Health check

## Environment Variables

Create a `.env` file if you need to customize the API URL:

```env
VITE_API_URL=http://localhost:8000
```

## Features Overview

### Dashboard
- System health status
- Document statistics
- Recent activity feed
- Quick access to main features

### Verify Documents
- Upload PO and Invoice files
- Real-time verification analysis
- Risk score calculation
- Anomaly detection
- Visual comparison charts
- Line item comparison table
- Fraud indicator alerts

### Upload Document
- Drag & drop file upload
- OCR text extraction
- Structured data display
- Line items table
- Extraction warnings

### Records
- List all processed documents
- Detailed record view
- CSV export functionality
- Search and filter (coming soon)

## Styling

The app uses Tailwind CSS with a custom color scheme:

- Primary: Blue (#0ea5e9)
- Success: Green
- Warning: Yellow
- Error: Red

Custom utility classes are defined in `src/index.css`

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

## License

Proprietary - Futurix AI
