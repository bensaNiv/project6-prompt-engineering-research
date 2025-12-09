# Architecture Documentation

## System Overview

This project implements a prompt engineering research pipeline that tests multiple prompt techniques against an LLM and analyzes the results.

```
┌─────────────────────────────────────────────────────────────────┐
│                        Data Layer                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ test_cases   │  │ few_shot     │  │ results/             │  │
│  │ .csv         │  │ _examples    │  │ ├── raw/*.csv        │  │
│  │              │  │ .json        │  │ └── stats/*.json     │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Application Layer                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ config.py    │  │ ollama_      │  │ prompts/             │  │
│  │              │  │ client.py    │  │ ├── base.py          │  │
│  │ Environment  │  │              │  │ ├── improved.py      │  │
│  │ loading      │  │ API wrapper  │  │ ├── few_shot.py      │  │
│  │              │  │              │  │ ├── chain_of_thought │  │
│  │              │  │              │  │ └── role_based.py    │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
│                              │                                   │
│  ┌──────────────┐  ┌────────┴─────┐  ┌──────────────────────┐  │
│  │ metrics.py   │  │ experiment   │  │ answer_evaluator.py  │  │
│  │              │  │ _runner.py   │  │                      │  │
│  │ Statistics   │  │              │  │ Answer matching      │  │
│  │ calculation  │  │ Orchestrates │  │ (exact, numeric,     │  │
│  │              │  │ experiments  │  │ semantic, contains)  │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Visualization Layer                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ visualization.py                                          │  │
│  │ ├── Bar charts (accuracy comparison)                      │  │
│  │ ├── Heatmaps (technique x category)                       │  │
│  │ ├── Box plots (variance analysis)                         │  │
│  │ ├── Line charts (difficulty trends)                       │  │
│  │ └── Radar charts (multi-dimensional comparison)           │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Directory Structure

```
project6-prompt-engineering-research/
├── .env                    # Ollama configuration (git-ignored)
├── .env.example            # Template for environment variables
├── .gitignore              # Git ignore rules
├── pyproject.toml          # Project configuration and dependencies
├── README.md               # Project overview
│
├── data/
│   └── test_cases.csv      # 100 test cases dataset
│
├── src/
│   ├── __init__.py         # Package initialization
│   ├── config.py           # Environment configuration
│   ├── ollama_client.py    # Ollama API wrapper
│   ├── answer_evaluator.py # Answer matching logic
│   ├── metrics.py          # Statistical calculations
│   ├── experiment_runner.py# Experiment orchestration
│   ├── visualization.py    # Chart generation
│   │
│   └── prompts/            # Prompt technique modules
│       ├── __init__.py
│       ├── base.py         # Base prompt class
│       ├── improved.py     # Improved regular prompts
│       ├── few_shot.py     # Few-shot learning
│       ├── chain_of_thought.py
│       └── role_based.py   # Role-based prompts
│
├── tests/
│   ├── __init__.py
│   ├── test_config.py
│   ├── test_ollama_client.py
│   ├── test_answer_evaluator.py
│   ├── test_metrics.py
│   └── test_prompts.py
│
├── results/
│   ├── raw/                # Raw experiment results
│   ├── stats/              # Aggregated statistics
│   └── figures/            # Generated visualizations
│
├── report/
│   └── REPORT.md           # Final analysis report
│
└── docs/
    ├── PRD.md              # Product requirements
    ├── ARCHITECTURE.md     # This file
    └── stage-*.md          # Implementation instructions
```

## Module Descriptions

### Core Modules

#### `config.py`
- Loads environment variables from `.env`
- Provides configuration constants (model name, rate limits)
- Validates required configuration

#### `ollama_client.py`
- Wraps Ollama API for consistent interface
- Handles connection errors and retries
- Returns response text and latency metrics
- Supports configurable host for WSL/remote setups

#### `answer_evaluator.py`
- Evaluates model responses against expected answers
- Supports multiple answer types:
  - `exact`: Exact string match (case-insensitive)
  - `numeric`: Numerical comparison with tolerance
  - `contains`: Response contains expected substring
  - `semantic`: Embedding-based similarity (using sentence-transformers)

#### `metrics.py`
- Calculates accuracy, mean, variance, standard deviation
- Aggregates results by category, difficulty, technique
- Generates comparison statistics JSON

#### `experiment_runner.py`
- Loads test cases from CSV
- Iterates through prompt techniques
- Runs each test case 3 times
- Saves results incrementally

### Prompt Modules

#### `prompts/base.py`
- Abstract base class for prompt generators
- Defines interface: `generate(question, category, **kwargs)`

#### `prompts/improved.py`
- Structured prompts with format hints per category
- Clear output constraints

#### `prompts/few_shot.py`
- Includes 3 examples before the question
- Loads examples from `few_shot_examples.json`

#### `prompts/chain_of_thought.py`
- Adds step-by-step reasoning instructions
- Includes format for extracting final answer

#### `prompts/role_based.py`
- Assigns expert role based on category
- Maps categories to role descriptions

### Visualization Module

#### `visualization.py`
- `PromptResearchVisualizer` class
- Methods for each chart type
- Consistent color scheme across visualizations
- Saves figures to `results/figures/`

## Data Flow

1. **Input**: `data/test_cases.csv` loaded by experiment runner
2. **Processing**:
   - For each test case and prompt technique:
     - Generate prompt using appropriate module
     - Call Ollama API via client
     - Evaluate answer correctness
     - Record results
3. **Output**:
   - Raw results saved to `results/raw/*.csv`
   - Statistics computed and saved to `results/stats/*.json`
   - Visualizations generated to `results/figures/*.png`

## Key Design Decisions

1. **Modular Prompts**: Each technique is a separate module for easy extension
2. **2 Runs per Case**: Measures consistency for mass production analysis
3. **Incremental Saves**: Prevents data loss on failures
4. **Semantic Evaluation**: Uses embeddings for non-exact answer comparison
5. **Separation of Concerns**: Config, API, evaluation, metrics, visualization are independent
6. **Local LLM**: Uses Ollama for cost-free, reproducible experiments
