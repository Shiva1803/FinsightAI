# Contributing to FinsightAI

First off, thank you for considering contributing to FinsightAI! It's people like you that make FinsightAI such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps to reproduce the problem**
* **Provide specific examples to demonstrate the steps**
* **Describe the behavior you observed after following the steps**
* **Explain which behavior you expected to see instead and why**
* **Include screenshots if possible**
* **Include your environment details** (OS, Python version, Node version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a step-by-step description of the suggested enhancement**
* **Provide specific examples to demonstrate the steps**
* **Describe the current behavior and explain which behavior you expected to see instead**
* **Explain why this enhancement would be useful**

### Pull Requests

* Fill in the required template
* Do not include issue numbers in the PR title
* Follow the Python and TypeScript style guides
* Include thoughtfully-worded, well-structured tests
* Document new code
* End all files with a newline

## Development Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- Tesseract OCR
- Git

### Setup Steps

1. Fork the repo
2. Clone your fork:
```bash
git clone https://github.com/YOUR_USERNAME/FinsightAI.git
cd FinsightAI
```

3. Set up backend:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

4. Set up frontend:
```bash
cd frontend
npm install
cd ..
```

5. Create a branch:
```bash
git checkout -b feature/your-feature-name
```

## Style Guides

### Python Style Guide

* Follow PEP 8
* Use type hints where possible
* Write docstrings for all functions and classes
* Keep functions small and focused
* Use meaningful variable names

Example:
```python
def calculate_risk_score(anomalies: List[str], summary: Dict) -> float:
    """
    Calculate risk score based on anomalies and summary data.
    
    Args:
        anomalies: List of detected anomaly types
        summary: Verification summary dictionary
        
    Returns:
        Risk score between 0.0 and 10.0
    """
    score = 0.0
    # Implementation
    return min(score, 10.0)
```

### TypeScript Style Guide

* Use TypeScript for all new code
* Define interfaces for all data structures
* Use functional components with hooks
* Follow React best practices
* Use meaningful component and variable names

Example:
```typescript
interface VerificationResult {
  verification_summary: VerificationSummary
  anomaly_insights: AnomalyInsights
  visualization_data: VisualizationData
}

export const VerifyDocuments: React.FC = () => {
  const [result, setResult] = useState<VerificationResult | null>(null)
  // Implementation
}
```

### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line

Examples:
```
Add vendor fraud detection algorithm
Fix OCR extraction for rotated images
Update README with deployment instructions
```

## Testing

### Backend Tests

Run all tests:
```bash
python -m pytest
```

Run specific test:
```bash
python test_api_verify.py
```

### Frontend Tests

```bash
cd frontend
npm test
```

### Writing Tests

* Write tests for all new features
* Ensure tests pass before submitting PR
* Aim for high test coverage
* Test edge cases and error conditions

## Project Structure

```
FinsightAI/
├── app/                    # Backend code
│   ├── main.py            # FastAPI routes
│   ├── verification_agent.py  # Core verification logic
│   └── ...
├── frontend/              # Frontend code
│   └── src/
│       ├── components/    # React components
│       ├── pages/         # Page components
│       └── services/      # API services
└── tests/                 # Test files
```

## Documentation

* Update README.md if you change functionality
* Add inline comments for complex logic
* Update API documentation for new endpoints
* Create/update type definitions

## Review Process

1. Create a pull request
2. Ensure all tests pass
3. Wait for review from maintainers
4. Address any feedback
5. Once approved, your PR will be merged

## Community

* Be respectful and inclusive
* Help others when you can
* Share your knowledge
* Have fun!

## Questions?

Feel free to open an issue with your question or reach out to the maintainers.

Thank you for contributing! 🎉
