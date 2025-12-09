# Project 6: Prompt Engineering Research

A research project measuring how different prompt engineering techniques affect LLM performance at scale. Tests baseline, improved prompts, few-shot learning, chain-of-thought, and role-based prompting across 100 test cases with 7 categories and 3 difficulty levels.

## Overview

This project investigates the effectiveness of various prompt engineering techniques for mass production use cases where consistency (low variance) matters as much as accuracy.

### Prompt Techniques Tested

| Technique | Description |
|-----------|-------------|
| **Baseline** | Minimal prompt with no special techniques |
| **Improved** | Structured format with category-specific hints |
| **Few-Shot** | Includes 3 examples before the question |
| **Chain-of-Thought** | Step-by-step reasoning instructions |
| **Role-Based** | Expert persona assignment |

### Test Categories

- Sentiment Analysis (15 cases)
- Multi-step Math (20 cases)
- Logical Reasoning (15 cases)
- Text Classification (15 cases)
- Reading Comprehension (15 cases)
- Common Sense Reasoning (10 cases)
- Code Output Prediction (10 cases)

## Installation

### Prerequisites

- Python 3.9 or higher
- Gemini API key

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd project6-prompt-engineering-research
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e ".[dev]"
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

## Usage

### Running Experiments

```python
from src import Config, ExperimentRunner
from src.prompts import (
    BaselinePromptGenerator,
    ImprovedPromptGenerator,
    FewShotPromptGenerator,
    ChainOfThoughtPromptGenerator,
    RoleBasedPromptGenerator,
)

# Load configuration
config = Config.from_env()

# Initialize runner
runner = ExperimentRunner(config)

# Define prompt generators
generators = {
    "baseline": BaselinePromptGenerator().generate,
    "improved": ImprovedPromptGenerator().generate,
    "few_shot": FewShotPromptGenerator().generate,
    "cot": ChainOfThoughtPromptGenerator().generate,
    "role_based": RoleBasedPromptGenerator().generate,
}

# Run all experiments
results = runner.run_all_techniques(generators)
```

### Generating Visualizations

```python
from src.visualization import PromptResearchVisualizer
import json

# Load statistics
with open("results/stats/comparison_stats.json") as f:
    stats = json.load(f)

# Generate all figures
visualizer = PromptResearchVisualizer()
visualizer.generate_all_figures(stats, results)
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html
```

## Project Structure

```
project6-prompt-engineering-research/
├── .env.example            # Environment variables template
├── pyproject.toml          # Project configuration
├── README.md               # This file
├── data/
│   └── test_cases.csv      # 100 test cases
├── src/
│   ├── __init__.py
│   ├── config.py           # Configuration loading
│   ├── gemini_client.py    # API wrapper
│   ├── answer_evaluator.py # Answer matching
│   ├── metrics.py          # Statistics calculation
│   ├── experiment_runner.py# Experiment orchestration
│   ├── visualization.py    # Chart generation
│   └── prompts/            # Prompt techniques
│       ├── base.py
│       ├── improved.py
│       ├── few_shot.py
│       ├── chain_of_thought.py
│       └── role_based.py
├── tests/                  # Unit tests
├── results/                # Output directory
│   ├── raw/                # Raw CSV results
│   ├── stats/              # Statistics JSON
│   └── figures/            # Generated charts
├── report/
│   └── REPORT.md           # Analysis report
└── docs/
    ├── PRD.md              # Requirements
    └── ARCHITECTURE.md     # System design
```

## Key Metrics

- **Accuracy**: Proportion of correct answers
- **Mean**: Average correctness score
- **Variance**: Score spread (lower = more consistent)
- **Improvement %**: Change relative to baseline

## License

MIT License
