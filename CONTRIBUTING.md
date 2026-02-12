# Contributing to AI Enterprise Operating System

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help create a welcoming environment

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported
2. Use the bug report template
3. Include detailed steps to reproduce
4. Include system information and logs

### Suggesting Features

1. Check existing feature requests
2. Describe the feature and use case
3. Explain why it would be valuable
4. Provide examples if possible

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Write/update tests
5. Ensure all tests pass
6. Update documentation
7. Commit with clear messages
8. Push to your fork
9. Open a pull request

### Coding Standards

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to functions
- Write unit tests for new features
- Keep functions focused and small
- Use type hints where appropriate

### Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and PRs where appropriate

Example:
```
Add fraud detection to finance module

- Implement IsolationForest model
- Add transaction analysis endpoint
- Include unit tests
- Update documentation

Closes #123
```

### Testing

```bash
# Run tests
pytest backend/tests/

# Run with coverage
pytest --cov=backend backend/tests/

# Run specific test
pytest backend/tests/test_hr.py::test_resume_screening
```

### Documentation

- Update README.md for major features
- Add docstrings to all functions
- Update API documentation
- Include examples in docs/

## Development Setup

1. Clone the repository
```bash
git clone https://github.com/ravigohel142996/AI-Enterprise-Command-System.git
cd AI-Enterprise-Command-System
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies
```

4. Set up pre-commit hooks
```bash
pre-commit install
```

5. Run tests
```bash
pytest
```

## Project Structure

```
backend/
├── app/
│   ├── api/          # API endpoints
│   ├── core/         # Core configuration
│   ├── models/       # Database models
│   ├── schemas/      # Pydantic schemas
│   ├── services/     # Business logic
│   └── ml/           # ML utilities
└── tests/            # Test files
```

## Questions?

Feel free to:
- Open an issue for questions
- Join our Discord community
- Email: dev@ai-enterprise-os.com

Thank you for contributing! 🎉
