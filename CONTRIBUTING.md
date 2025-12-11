# Contributing Guidelines

Thank you for your interest in contributing to the Prompt Engineering Research project!

## Table of Contents
- [Code Style](#code-style)
- [Development Setup](#development-setup)
- [Development Workflow](#development-workflow)
- [Testing](#testing)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)

## Code Style

### Python Standards
- Follow [PEP 8](https://pep8.org/) style guidelines
- Use [Black](https://black.readthedocs.io/) for code formatting
- Use [isort](https://pycqa.github.io/isort/) for import sorting
- Maximum line length: 100 characters

### Type Hints
All functions must include type hints:
```python
def calculate_accuracy(results: list[int]) -> float:
    """Calculate accuracy from a list of binary results."""
    return sum(results) / len(results) if results else 0.0
```

### Docstrings
Use NumPy-style docstrings for all public functions and classes:
```python
def evaluate(self, response: str, expected: str) -> tuple[bool, float]:
    """
    Evaluate if response matches expected answer.

    Parameters
    ----------
    response : str
        The model's response text.
    expected : str
        The expected answer.

    Returns
    -------
    tuple[bool, float]
        Tuple of (is_correct, confidence_score).
    """
```

### File Organization
- Keep files under 150 lines
- One class per file (with exceptions for related small classes)
- Use meaningful file and function names

## Development Setup

### Prerequisites
- Python 3.9+
- Ollama installed and running
- Git

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd project6-prompt-engineering-research

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install black isort pytest pytest-cov
```

### Configuration
```bash
# Copy example environment file
cp .env.example .env

# Edit with your settings
# OLLAMA_HOST=http://localhost:11434
# MODEL_NAME=llama3.2:3b
```

## Development Workflow

### 1. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes
- Write tests first (TDD encouraged)
- Implement your feature
- Update documentation as needed

### 3. Run Quality Checks
```bash
# Format code
black src/ tests/
isort src/ tests/

# Run tests
pytest tests/ -v

# Check coverage
pytest --cov=src --cov-report=term-missing
```

### 4. Submit Changes
```bash
git add .
git commit -m "feat: add your feature description"
git push origin feature/your-feature-name
```

## Testing

### Running Tests
```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_config.py

# Run with coverage
pytest --cov=src --cov-report=html

# Run with verbose output
pytest -v
```

### Writing Tests
- Place tests in `tests/` directory
- Name test files `test_*.py`
- Name test functions `test_*`
- Include edge cases and error conditions

Example:
```python
def test_evaluate_exact_match():
    """Test that exact matches are detected correctly."""
    evaluator = AnswerEvaluator()
    is_correct, confidence = evaluator.evaluate("Paris", "Paris", "exact")
    assert is_correct is True
    assert confidence == 1.0
```

## Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/) format:

```
type(scope): description

[optional body]

[optional footer]
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples
```
feat(prompts): add few-shot prompt generator

fix(evaluator): handle empty responses correctly

docs(readme): update installation instructions

test(metrics): add edge case tests for variance calculation
```

## Pull Request Process

### Before Submitting
- [ ] All tests pass (`pytest tests/`)
- [ ] Code is formatted (`black src/ tests/`)
- [ ] No linting errors
- [ ] Documentation is updated
- [ ] Commit messages follow convention

### PR Description Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring

## Testing
How was this tested?

## Checklist
- [ ] Tests pass
- [ ] Code formatted
- [ ] Documentation updated
```

### Review Process
1. Submit PR with description
2. Wait for code review
3. Address feedback
4. Merge after approval

## Questions?

If you have questions about contributing, please open an issue or contact the maintainers.
