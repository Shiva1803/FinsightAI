# 🧪 Complete Testing Guide - Futurix AI

## Quick Test Options

### Option 1: Run All Tests (Recommended)
```bash
./run_tests.sh
```
This will run all automated tests and show you a summary.

### Option 2: Run Individual Test Suites
```bash
# Test extraction system
python3 test_extractor.py

# Test verification agent
python3 test_verification_agent.py

# Interactive testing
python3 test_interactive.py
```

### Option 3: Test API Endpoints
```bash
# Start server first
uvicorn app.main:app --reload

# In another terminal, test endpoints
curl http://localhost:8000/health/
```

## 📋 Detailed Testing Steps

### Step 1: Prerequisites Check

```bash
# Check Python version (need 3.11+)
python3 --version

# Check dependencies
pip list | grep -E "fastapi|dateutil|Pillow"

# Install if missing
pip install -r requirements.txt
```

### Step 2: Run Automated Tests

#### Test Extraction System
```bash
python3 test_extractor.py
```

**What it tests:**
- ✅ Invoice extraction (all fields)
- ✅ PO extraction (all fields)
- ✅ Line item parsing
- ✅ Confidence scoring
- ✅ Validation logic

**Expected output:**
```
================================================================================
TESTING INVOICE EXTRACTION
================================================================================

📄 Extracted Invoice Data:
{
  "document_type": "invoice",
  "vendor_name": "...",
  "total_amount": 42775.0,
  ...
}

✨ All tests completed!
```

#### Test Verification Agent
```bash
python3 test_verification_agent.py
```

**What it tests:**
- ✅ Normal verification (minor discrepancies)
- ✅ Fraud detection (major issues)
- ✅ Risk scoring (0-10 scale)
- ✅ Visualization data generation
- ✅ Vendor history integration

**Expected output:**
```
================================================================================
TEST 1: Normal Verification (Minor Discrepancies)
================================================================================

📊 VERIFICATION SUMMARY:
  ✓ Risk Score: 6.5/10
  ✓ Discrepancy Level: MEDIUM
  ...

✨ ALL TESTS COMPLETED
Verification Agent Status: ✅ OPERATIONAL
```

### Step 3: Interactive Testing

```bash
python3 test_interactive.py
```

This will guide you through:
1. Document extraction demo
2. PO vs Invoice verification
3. Fraud detection example
4. Complete JSON output

**Interactive prompts:**
- Press Enter to proceed through each test
- See real-time results
- View formatted output

### Step 4: API Testing

#### Start the Server
```bash
uvicorn app.main:app --reload
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

#### Test Health Endpoint
```bash
curl http://localhost:8000/health/
```

**Expected response:**
```json
{"status": "ok"}
```

#### Test Verification Endpoint
```bash
# Create test files
cat > test_po.txt << 'EOF'
PURCHASE ORDER
Order: PO-123
Vendor: Acme Corp
Total: INR 10,000
EOF

cat > test_invoice.txt << 'EOF'
INVOICE
Invoice: INV-456
PO Number: PO-123
Vendor: Acme Corp
Total: INR 10,000
EOF

# Verify documents
curl -X POST "http://localhost:8000/verify/" \
  -F "po_file=@test_po.txt" \
  -F "invoice_file=@test_invoice.txt"
```

**Expected response:**
```json
{
  "verification_summary": {
    "vendor_match": true,
    "po_number_match": true,
    "total_match": true,
    "discrepancy_level": "none",
    "needs_review": false
  },
  "anomaly_insights": {
    "risk_score": 0.0,
    "pattern": "normal"
  },
  ...
}
```

## 🎯 Test Scenarios

### Scenario 1: Perfect Match (Should Pass)
```bash
curl -X POST "http://localhost:8000/verify/" \
  -F "po_text=PO-123, Acme Corp, Total: 10000" \
  -F "invoice_text=INV-456, PO-123, Acme Corp, Total: 10000"
```

**Expected:**
- ✅ vendor_match: true
- ✅ total_match: true
- ✅ risk_score: 0-2
- ✅ discrepancy_level: "none"

### Scenario 2: Minor Overbilling (Should Flag)
```bash
curl -X POST "http://localhost:8000/verify/" \
  -F "po_text=PO-123, Acme Corp, Total: 10000" \
  -F "invoice_text=INV-456, PO-123, Acme Corp, Total: 10700"
```

**Expected:**
- ⚠️ total_match: false
- ⚠️ amount_difference: 700
- ⚠️ risk_score: 3-5
- ⚠️ discrepancy_level: "medium"

### Scenario 3: Major Fraud (Should Reject)
```bash
curl -X POST "http://localhost:8000/verify/" \
  -F "po_text=PO-123, Acme Corp, Total: 10000" \
  -F "invoice_text=INV-456, PO-123, Different Vendor, Total: 25000"
```

**Expected:**
- 🚨 vendor_match: false
- 🚨 total_match: false
- 🚨 risk_score: 9-10
- 🚨 discrepancy_level: "high"
- 🚨 fraud_indicators: ["Vendor name does not match PO", ...]

## 📊 Interpreting Test Results

### Extraction Results

**Good Extraction:**
```json
{
  "extraction_warnings": [],
  "vendor_name": "Acme Corp",
  "total_amount": 42775.0,
  "line_items": [...]
}
```

**Needs Review:**
```json
{
  "extraction_warnings": [
    "Low confidence vendor extraction: 0.45",
    "Currency not detected"
  ],
  "vendor_name": null,
  "total_amount": null
}
```

### Verification Results

**Risk Score Guide:**
- **0-2**: 🟢 Low risk → Auto-approve
- **3-5**: 🟡 Medium risk → Review recommended
- **6-8**: 🟠 High risk → Requires review
- **9-10**: 🔴 Critical risk → Reject/escalate

**Discrepancy Levels:**
- **none**: No issues found
- **low**: 1-2 minor discrepancies
- **medium**: Multiple discrepancies or 5-10% variance
- **high**: High severity issues or >10% variance

## 🐛 Troubleshooting

### Tests Fail with Import Errors

```bash
# Install dependencies
pip install -r requirements.txt

# Verify installation
python3 -c "from app.extractor import parse_document"
python3 -c "from app.verification_agent import verify_from_text"
```

### Server Won't Start

```bash
# Check if port is in use
lsof -i :8000

# Kill existing process
kill -9 $(lsof -t -i:8000)

# Or use different port
uvicorn app.main:app --reload --port 8001
```

### OCR Not Working

```bash
# Install Tesseract
# macOS:
brew install tesseract

# Ubuntu/Debian:
sudo apt-get install tesseract-ocr

# Verify
tesseract --version
```

### Low Extraction Accuracy

**Check:**
1. OCR text quality (clear, readable)
2. Document format (standard invoice/PO layout)
3. Extraction warnings in output
4. Debug info for pattern matching

**Improve:**
- Use higher resolution images
- Ensure good lighting/contrast
- Add custom regex patterns for specific vendors
- Tune confidence thresholds

## ✅ Testing Checklist

### Basic Tests
- [ ] Python 3.11+ installed
- [ ] Dependencies installed
- [ ] Syntax check passes
- [ ] Import tests pass

### Extraction Tests
- [ ] Invoice extraction works
- [ ] PO extraction works
- [ ] Line items parsed correctly
- [ ] Dates normalized to ISO
- [ ] Currency detected
- [ ] Confidence scores calculated

### Verification Tests
- [ ] Normal verification works
- [ ] Fraud detection works
- [ ] Risk scoring accurate
- [ ] Visualization data generated
- [ ] JSON output valid

### API Tests
- [ ] Server starts successfully
- [ ] Health endpoint responds
- [ ] Upload endpoint works
- [ ] Verify endpoint works
- [ ] Export endpoint works

### Integration Tests
- [ ] End-to-end flow works
- [ ] Database saves records
- [ ] Error handling works
- [ ] Edge cases handled

## 🚀 Quick Test Commands

```bash
# Run everything
./run_tests.sh

# Just extraction
python3 test_extractor.py

# Just verification
python3 test_verification_agent.py

# Interactive
python3 test_interactive.py

# API (server must be running)
curl http://localhost:8000/health/
curl -X POST http://localhost:8000/verify/ \
  -F "po_text=PO-123" -F "invoice_text=INV-456"
```

## 📈 Performance Testing

### Test Processing Speed
```bash
time python3 -c "
from app.extractor import parse_document
text = 'Invoice INV-001, Total: 10000'
for i in range(100):
    parse_document(text)
"
```

**Expected:** <5 seconds for 100 documents

### Test API Response Time
```bash
time curl -X POST http://localhost:8000/verify/ \
  -F "po_text=PO-123" -F "invoice_text=INV-456"
```

**Expected:** <1 second per request

## 📚 Additional Resources

- **TEST_API.md** - Detailed API testing guide
- **QUICK_REFERENCE.md** - Quick command reference
- **VERIFICATION_AGENT_GUIDE.md** - Complete API documentation
- **README_COMPLETE.md** - Full system documentation

## 🎉 Success Criteria

Your system is working correctly if:

✅ All automated tests pass
✅ Server starts without errors
✅ API endpoints respond correctly
✅ Extraction accuracy >90%
✅ Risk scores are reasonable
✅ Fraud detection works
✅ JSON output is valid

## 💡 Next Steps After Testing

1. ✅ Verify all tests pass
2. ✅ Test with real invoice/PO documents
3. ✅ Integrate with your dashboard
4. ✅ Set up monitoring
5. ✅ Deploy to production

---

**Need Help?**
- Check error messages in test output
- Review extraction_warnings in results
- Examine extraction_debug for details
- See troubleshooting section above
