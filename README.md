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
- Ollama (local LLM runtime)

### Installing Ollama

Ollama is a tool for running large language models locally. Follow the instructions for your operating system:

#### Windows

1. Download the installer from [ollama.com/download](https://ollama.com/download)
2. Run the installer and follow the prompts
3. After installation, Ollama will run as a background service
4. Open a terminal and pull the model:
   ```powershell
   ollama pull llama3.2:3b
   ```

#### macOS

1. Download from [ollama.com/download](https://ollama.com/download) or use Homebrew:
   ```bash
   brew install ollama
   ```
2. Start Ollama:
   ```bash
   ollama serve
   ```
3. In another terminal, pull the model:
   ```bash
   ollama pull llama3.2:3b
   ```

#### Linux

1. Install using the official script:
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ```
2. Start Ollama:
   ```bash
   ollama serve
   ```
3. In another terminal, pull the model:
   ```bash
   ollama pull llama3.2:3b
   ```

#### WSL (Windows Subsystem for Linux)

If running Python in WSL but Ollama on Windows:

1. Install Ollama on Windows (see Windows instructions above)
2. Find your Windows host IP:
   ```bash
   # In WSL, run:
   cat /etc/resolv.conf | grep nameserver | awk '{print $2}'
   ```
3. Set the host in your `.env` file:
   ```bash
   OLLAMA_HOST=http://<windows-ip>:11434
   ```

### Verifying Ollama Installation

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# List available models
ollama list

# Test the model
ollama run llama3.2:3b "Hello, how are you?"
```

### Project Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd project6-prompt-engineering-research
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
# Or with dev dependencies:
pip install -e ".[dev]"
```

4. Configure environment variables (optional):
```bash
cp .env.example .env
# Edit .env to customize OLLAMA_HOST or MODEL_NAME if needed
```

## Usage

### Running the Baseline Experiment

```bash
# Ensure Ollama is running, then:
python run_baseline.py
```

This will:
- Run 100 test cases with the baseline prompt
- Execute each case 2 times to measure consistency
- Save results to `results/baseline_results.csv`
- Generate statistics in `results/baseline_stats.json`

### Configuration Options

Set these in `.env` or as environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama server URL |
| `MODEL_NAME` | `llama3.2:3b` | Model to use for experiments |

### Applying Manual Overrides

If you need to manually correct answer evaluations:

1. Edit `data/manual_overrides.csv` with your corrections
2. Run the override script:
   ```bash
   python apply_overrides.py baseline
   ```

### Running All Techniques

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

# Initialize runner with Ollama client
from src.ollama_client import OllamaClient
client = OllamaClient(config)
runner = ExperimentRunner(config, client=client)

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
├── run_baseline.py         # Baseline experiment script
├── apply_overrides.py      # Manual override application
├── data/
│   ├── test_cases.csv      # 100 test cases
│   └── manual_overrides.csv# Manual answer corrections
├── src/
│   ├── __init__.py
│   ├── config.py           # Configuration loading
│   ├── ollama_client.py    # Ollama API wrapper
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

## Troubleshooting

### Ollama Connection Issues

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not running, start it:
ollama serve
```

### Model Not Found

```bash
# Pull the required model
ollama pull llama3.2:3b

# List available models
ollama list
```

### WSL Network Issues

If running in WSL and can't connect to Ollama on Windows:
1. Ensure Windows Firewall allows connections on port 11434
2. Use the Windows host IP instead of localhost
3. Check that Ollama is configured to listen on all interfaces

## License

MIT License
