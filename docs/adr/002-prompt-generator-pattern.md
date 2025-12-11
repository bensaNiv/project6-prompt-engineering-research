# ADR 002: Prompt Generator Base Class Pattern

## Status

Accepted

## Date

2025-12-01

## Context

This project tests 5 different prompt engineering techniques across 100 test cases. Each technique transforms a test case into a different prompt format. We need a consistent way to:

1. Define new prompt techniques
2. Ensure all techniques receive the same input format
3. Make it easy to add new techniques
4. Maintain consistent interfaces for the experiment runner

Design options considered:

1. **Simple functions**: Each technique is a standalone function `def generate_baseline(case) -> str`
2. **Base class with inheritance**: Abstract base class defining the interface
3. **Protocol/Interface**: Python Protocol for duck typing
4. **Configuration-driven**: Templates in YAML/JSON files

## Decision

We chose the **Base Class Pattern** with `BasePromptGenerator` as the abstract base class.

### Implementation

```python
# src/prompts/base.py
class BasePromptGenerator:
    """Base class for all prompt generators."""

    def generate(self, case: dict) -> str:
        """Generate a prompt for the given test case."""
        raise NotImplementedError
```

Each technique inherits from this base:
- `BaselinePromptGenerator` - Minimal prompts
- `ImprovedPromptGenerator` - Structured with hints
- `FewShotPromptGenerator` - Includes examples
- `ChainOfThoughtPromptGenerator` - Step-by-step reasoning
- `RoleBasedPromptGenerator` - Expert persona

### Reasons

1. **Clear contract**: Base class documents expected interface
2. **IDE support**: Type hints and autocomplete work properly
3. **Extensibility**: New techniques just inherit and implement `generate()`
4. **Testability**: Easy to mock/stub for unit tests
5. **Discoverability**: All generators in `src/prompts/` directory

## Consequences

### Positive

- **Consistent interface**: All generators have identical `generate(case) -> str` signature
- **Easy extension**: Adding a new technique = new file with class inheriting from base
- **Type safety**: Type checkers can verify correct usage
- **Documentation**: Base class docstrings serve as specification

### Negative

- **Boilerplate**: Each generator needs class definition even if simple
- **Learning curve**: Contributors must understand inheritance pattern

### Trade-offs Accepted

- Chose classes over functions for better organization despite slight overhead
- Chose inheritance over Protocol for explicit contract enforcement

## Usage Example

```python
from src.prompts import ChainOfThoughtPromptGenerator

generator = ChainOfThoughtPromptGenerator()
prompt = generator.generate({
    "question": "What is 2+2?",
    "category": "math",
    "difficulty": "easy"
})
```

## Adding New Techniques

To add a new prompt technique:

1. Create `src/prompts/new_technique.py`
2. Inherit from `BasePromptGenerator`
3. Implement the `generate(case: dict) -> str` method
4. Export in `src/prompts/__init__.py`
5. Create corresponding `run_new_technique.py` script

## References

- [Python Abstract Base Classes](https://docs.python.org/3/library/abc.html)
- [Strategy Pattern](https://refactoring.guru/design-patterns/strategy)
