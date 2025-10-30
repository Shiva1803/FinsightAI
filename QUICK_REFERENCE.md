# Futurix AI - Quick Reference Card

## 🚀 Quick Start

### Run Tests
```bash
# Test extractor
python3 test_extractor.py

# Test verification agent
python3 test_verification_agent.py
```

### Start Server
```bash
uvicorn app.main:app --reload
```

## 📡 API Endpoints

### 1. Extract Document
```bash
POST /upload/
# Upload PDF/image, get extracted data
curl -X POST "http://localhost:8000/upload/" -F "file=@invoice.pdf"
```

### 2. Verify PO vs Invoice
```bash
POST /verify/
# Compare PO and Invoice
curl -X POST "http://localhost:8000/verify/" \
  -F "po_file=@PO.pdf" \
  -F "invoice_file=@Invoice.pdf"
```

### 3. Export Data
```bash
GET /export/
# Download CSV of all records
curl "http://localhost:8000/export/" -o export.csv
```

## 🔍 Key Features

### Extraction (app/extractor.py)
- ✅ Document type detection (invoice/PO/unknown)
- ✅ Vendor & buyer info (names + tax IDs)
- ✅ Document numbers & dates (ISO format)
- ✅ Currency detection (INR, USD, EUR, etc.)
- ✅ Amounts (total, subtotal, tax)
- ✅ Line items (description, qty, price, total)
- ✅ Confidence scoring (0-1)
- ✅ Warnings & debug info

### Verification (app/verification_agent.py)
- ✅ Entity matching (vendor, PO number, dates)
- ✅ Numerical verification (qty, price, totals)
- ✅ Anomaly detection (8 types)
- ✅ Risk scoring (0-10 Naughty List)
- ✅ Fraud indicators
- ✅ Dashboard visualization data

## 📊 Output Structure

### Extraction Output
```json
{
  "document_type": "invoice",
  "vendor_name": "Acme Corp",
  "total_amount": 42775.0,
  "line_items": [...],
  "extraction_warnings": [],
  "extraction_debug": {...}
}
```

### Verification Output
```json
{
  "verification_summary": {
    "vendor_match": true,
    "total_match": false,
    "amount_difference": 2950.0,
    "discrepancy_level": "medium",
    "needs_review": true
  },
  "anomaly_insights": {
    "risk_score": 6.5,
    "fraud_indicators": [...]
  },
  "visualization_data": {
    "bar_chart": {...},
    "naughty_list_score": 6.5
  }
}
```

## 🎯 Risk Levels

| Score | Level | Action |
|-------|-------|--------|
| 0-2 | 🟢 Low | Auto-approve |
| 3-5 | 🟡 Medium | Review recommended |
| 6-8 | 🟠 High | Requires review |
| 9-10 | 🔴 Critical | Reject/escalate |

## 🔧 Python Usage

### Extract
```python
from app.extractor import parse_document

result = parse_document(ocr_text)
print(result["total_amount"])
```

### Verify
```python
from app.verification_agent import verify_from_text

result = verify_from_text(po_text, invoice_text)
if result["verification_summary"]["needs_review"]:
    print(f"Risk: {result['anomaly_insights']['risk_score']}/10")
```

## 📁 Project Structure

```
futurix/
├── app/
│   ├── extractor.py           # Enhanced extraction (641 lines)
│   ├── verification_agent.py  # Verification engine (600+ lines)
│   ├── main.py                # FastAPI endpoints
│   ├── ocr.py                 # OCR processing
│   └── db.py                  # Database operations
├── test_extractor.py          # Extraction tests
├── test_verification_agent.py # Verification tests
├── EXTRACTOR_GUIDE.md         # Extraction docs
├── VERIFICATION_AGENT_GUIDE.md # Verification docs
└── requirements.txt           # Dependencies
```

## 🎨 Dashboard Data

### Available Visualizations
1. **Bar Chart** - PO vs Invoice totals
2. **Pie Chart** - Discrepancy breakdown
3. **Line Items Table** - Item-by-item comparison
4. **Timeline** - PO → Invoice → Due Date
5. **Risk Gauge** - Naughty List Score (0-10)
6. **Status Badge** - Approval status

### Access Visualization Data
```javascript
const viz = result.visualization_data;

// Bar chart
const barData = viz.bar_chart;
// {labels: ["PO Total", "Invoice Total"], values: [39825, 42775]}

// Naughty list score
const score = viz.naughty_list_score; // 0-10

// Line items comparison
const items = viz.line_items_comparison;
// [{description, po_qty, invoice_qty, qty_match, ...}]
```

## ⚠️ Common Issues

### Low Confidence
```python
if result["extraction_warnings"]:
    print("⚠️ Issues:", result["extraction_warnings"])
```

### Fraud Detected
```python
if result["anomaly_insights"]["fraud_indicators"]:
    print("🚨 Fraud indicators:")
    for indicator in result["anomaly_insights"]["fraud_indicators"]:
        print(f"  - {indicator}")
```

## 📚 Documentation

- **EXTRACTOR_GUIDE.md** - Complete extraction reference
- **VERIFICATION_AGENT_GUIDE.md** - Complete verification reference
- **IMPLEMENTATION_SUMMARY.md** - What was built (extraction)
- **VERIFICATION_AGENT_SUMMARY.md** - What was built (verification)

## 🧪 Test Commands

```bash
# Test extraction
python3 test_extractor.py

# Test verification
python3 test_verification_agent.py

# Start server
uvicorn app.main:app --reload

# Check health
curl http://localhost:8000/health/
```

## 🔑 Key Thresholds

### Extraction
- Confidence threshold: 0.6
- High confidence: >0.8
- Low confidence: <0.5

### Verification
- Total match tolerance: 2%
- Tax match tolerance: 5%
- Price tolerance: 2% (configurable)
- Fuzzy name match: 80%
- Date range: 30 days (configurable)

## 💡 Pro Tips

1. **Always check `needs_review` flag** before auto-approval
2. **Monitor risk scores** - escalate >7
3. **Review fraud indicators** - investigate all flagged
4. **Check confidence scores** - manual review if <0.6
5. **Track vendor history** - identify repeat offenders
6. **Tune thresholds** - adjust for your business needs

## 🎉 Status

✅ **Extraction System**: Operational
✅ **Verification Agent**: Operational
✅ **API Endpoints**: Integrated
✅ **Tests**: All passing
✅ **Documentation**: Complete

**Ready for production deployment!**
