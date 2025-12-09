# CLAUDE.md

This file provides guidance to Claude Code when working in this repository.

## Project Overview

**Project 6: Prompt Engineering Research** - A research project measuring how different prompt techniques affect LLM performance at scale. Tests baseline, improved prompts, few-shot learning, chain-of-thought, and role-based prompting across 100 test cases with 7 categories and 3 difficulty levels.

## Key Constraints

- **LLM**: Uses Ollama with local models (default: `llama3.2:3b`)
- **Mass Production Focus**: Optimize for consistency (low variance), not just accuracy
- **Metrics**: Accuracy, Mean, Variance, Embedding Distance, Histograms
- **Runs**: Each prompt tested 2x per case to measure consistency

## Project Structure

```
project6-prompt-engineering-research/
├── .env                  # OLLAMA_HOST, MODEL_NAME (git-ignored)
├── data/test_cases.csv   # 100 test cases
├── src/                  # Python modules
├── results/              # Raw results + figures
├── report/REPORT.md      # Final analysis
└── docs/                 # Implementation instructions
```

## Running the Experiment

1. Ensure Ollama is running locally (or set `OLLAMA_HOST` in `.env`)
2. Run: `python run_baseline.py`
3. Review results in `results/baseline_results.csv`
4. Apply manual overrides if needed: `python apply_overrides.py baseline`

## Documentation

Detailed instructions in `docs/`:
- `stage-1-2-instructions.md` - Dataset creation & baseline
- `stage-3-instructions.md` - Prompt techniques
- `stage-4-instructions.md` - Visualization & report
