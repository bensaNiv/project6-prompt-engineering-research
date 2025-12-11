# Extension Guide: Adding New Prompt Techniques

This guide explains how to add new prompt engineering techniques to the project.

## Overview

All prompt techniques inherit from `BasePromptGenerator` and implement a single method: `generate(test_case: dict) -> str`. This design allows easy extension without modifying existing code.

## Step-by-Step Guide

### Step 1: Create the Generator Class

Create a new file in `src/prompts/` (e.g., `src/prompts/my_technique.py`):

```python
"""My custom prompt generator."""

from .base import BasePromptGenerator


class MyTechniquePromptGenerator(BasePromptGenerator):
    """
    Custom prompt generator implementing my technique.

    Describe what makes this technique unique and when to use it.
    """

    def generate(self, test_case: dict) -> str:
        """
        Generate a prompt using my technique.

        Parameters
        ----------
        test_case : dict
            Dictionary containing:
            - question: The question text
            - category: Problem category (sentiment, math, logic, etc.)
            - difficulty: Difficulty level (1-3)
            - expected_answer: The expected answer
            - answer_type: Type of answer matching

        Returns
        -------
        str
            The generated prompt string.
        """
        question = test_case["question"]
        category = test_case["category"]

        # Build your custom prompt here
        prompt = f"""[Your technique-specific formatting]

Question: {question}

[Your technique-specific instructions]
"""
        return prompt
```

### Step 2: Export the Generator

Add your generator to `src/prompts/__init__.py`:

```python
from .base import BasePromptGenerator, BaselinePromptGenerator
from .improved import ImprovedPromptGenerator
from .few_shot import FewShotPromptGenerator
from .chain_of_thought import ChainOfThoughtPromptGenerator
from .role_based import RoleBasedPromptGenerator
from .my_technique import MyTechniquePromptGenerator  # Add this line

__all__ = [
    "BasePromptGenerator",
    "BaselinePromptGenerator",
    "ImprovedPromptGenerator",
    "FewShotPromptGenerator",
    "ChainOfThoughtPromptGenerator",
    "RoleBasedPromptGenerator",
    "MyTechniquePromptGenerator",  # Add this line
]
```

### Step 3: Create a Runner Script

Create `scripts/run_my_technique.py`:

```python
#!/usr/bin/env python3
"""Run experiment with my custom technique."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.cli_runner import run_experiment
from src.prompts import MyTechniquePromptGenerator

if __name__ == "__main__":
    generator = MyTechniquePromptGenerator()
    run_experiment("my_technique", generator.generate)
```

### Step 4: Run the Experiment

```bash
python scripts/run_my_technique.py
```

Results will be saved to:
- `results/raw/my_technique_results.csv`
- `results/stats/my_technique_stats.json`

## Test Case Dictionary Structure

Your `generate()` method receives a dictionary with these keys:

| Key | Type | Description | Example |
|-----|------|-------------|---------|
| `question` | str | The question text | "What is 2 + 2?" |
| `category` | str | Problem category | "math", "sentiment", "logic" |
| `difficulty` | int | Difficulty level | 1 (easy), 2 (medium), 3 (hard) |
| `expected_answer` | str | Expected answer | "4" |
| `answer_type` | str | Matching type | "exact", "contains", "numeric" |
| `id` | int | Test case ID | 42 |

## Best Practices

### 1. End with Concise Instructions

Always instruct the model to give a concise answer:

```python
prompt += "\n\nAnswer concisely with just the answer, no explanation."
```

### 2. Use Category-Specific Formatting

Adapt your prompt based on the category:

```python
if category == "math":
    prompt = f"Solve this math problem: {question}"
elif category == "sentiment":
    prompt = f"Analyze the sentiment: {question}"
```

### 3. Keep Prompts Focused

Avoid over-engineering. Our research found that simpler prompts often outperform complex ones on smaller models.

### 4. Test on Multiple Categories

Ensure your technique works across all 7 categories before deploying.

## Example Techniques to Try

### Structured Output
```python
def generate(self, test_case: dict) -> str:
    return f"""Question: {test_case['question']}

Respond in this exact format:
ANSWER: [your answer]"""
```

### Reflection Technique
```python
def generate(self, test_case: dict) -> str:
    return f"""Question: {test_case['question']}

Before answering:
1. What type of question is this?
2. What information do I need?
3. What's my answer?

Final Answer:"""
```

### Confidence-Based
```python
def generate(self, test_case: dict) -> str:
    return f"""Question: {test_case['question']}

Provide your answer and confidence level (low/medium/high).
Format: [answer] (confidence: [level])"""
```

## Adding Tests

Create tests in `tests/test_my_technique.py`:

```python
"""Tests for MyTechniquePromptGenerator."""

import pytest
from src.prompts import MyTechniquePromptGenerator


class TestMyTechniquePromptGenerator:
    def setup_method(self):
        self.generator = MyTechniquePromptGenerator()

    def test_generates_prompt(self):
        test_case = {
            "question": "What is 2+2?",
            "category": "math",
            "difficulty": 1,
            "expected_answer": "4",
            "answer_type": "exact",
        }
        prompt = self.generator.generate(test_case)
        assert "2+2" in prompt
        assert len(prompt) > 0

    def test_handles_all_categories(self):
        categories = ["sentiment", "math", "logic", "classification",
                      "reading", "commonsense", "code"]
        for cat in categories:
            test_case = {"question": "Test?", "category": cat,
                         "difficulty": 1, "expected_answer": "x",
                         "answer_type": "exact"}
            prompt = self.generator.generate(test_case)
            assert prompt is not None
```

Run tests:
```bash
pytest tests/test_my_technique.py -v
```

## Comparing Results

After running your experiment, compare with existing techniques:

```python
from src.comparison_utils import load_all_results, compare_techniques

results = load_all_results()
comparison = compare_techniques(results)
print(comparison)
```

Or regenerate all figures including your new technique:
```bash
python scripts/generate_figures.py
```
