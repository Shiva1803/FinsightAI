#!/bin/bash

# Futurix AI - Test Runner Script
# Run all tests and verify system is working

echo "================================================================================"
echo "  🚀 FUTURIX AI - RUNNING ALL TESTS"
echo "================================================================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Function to run test
run_test() {
    local test_name=$1
    local test_command=$2
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  Testing: $test_name"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    if eval $test_command; then
        echo -e "${GREEN}✅ PASSED${NC}: $test_name"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}❌ FAILED${NC}: $test_name"
        ((TESTS_FAILED++))
    fi
    echo ""
}

# Test 1: Check Python version
echo "Checking prerequisites..."
run_test "Python 3 Installation" "python3 --version > /dev/null 2>&1"

# Test 2: Check core dependencies (PIL is optional for image OCR)
run_test "Core Dependencies Check" "python3 -c 'import fastapi, dateutil' 2>/dev/null"

# Test 3: Syntax check
run_test "Syntax Check - extractor.py" "python3 -m py_compile app/extractor.py"
run_test "Syntax Check - verification_agent.py" "python3 -m py_compile app/verification_agent.py"
run_test "Syntax Check - main.py" "python3 -m py_compile app/main.py"

# Test 4: Run extraction tests
echo ""
echo "Running extraction tests..."
run_test "Extraction Test Suite" "python3 test_extractor.py > /dev/null 2>&1"

# Test 5: Run verification tests
echo ""
echo "Running verification tests..."
run_test "Verification Test Suite" "python3 test_verification_agent.py > /dev/null 2>&1"

# Test 6: Import tests
echo ""
echo "Testing imports..."
run_test "Import extractor module" "python3 -c 'from app.extractor import parse_document'"
run_test "Import verification module" "python3 -c 'from app.verification_agent import verify_from_text'"

# Summary
echo "================================================================================"
echo "  📊 TEST SUMMARY"
echo "================================================================================"
echo ""
echo -e "  Tests Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "  Tests Failed: ${RED}$TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ ALL TESTS PASSED!${NC}"
    echo ""
    echo "  System Status: 🟢 OPERATIONAL"
    echo ""
    echo "  Next Steps:"
    echo "    1. Start server: uvicorn app.main:app --reload"
    echo "    2. Test API: curl http://localhost:8000/health/"
    echo "    3. Run interactive test: python3 test_interactive.py"
    echo ""
    exit 0
else
    echo -e "${RED}❌ SOME TESTS FAILED${NC}"
    echo ""
    echo "  Please check the errors above and:"
    echo "    1. Install missing dependencies: pip install -r requirements.txt"
    echo "    2. Check Python version (need 3.11+)"
    echo "    3. Review error messages"
    echo ""
    exit 1
fi

echo "================================================================================"
