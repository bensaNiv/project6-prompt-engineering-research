# CLAUDE.md

This file provides guidance to Claude Code when working in this repository.

## Project Overview

**Project 6: Prompt Engineering Research** - A research project measuring how different prompt techniques affect LLM performance at scale. Tests baseline, improved prompts, few-shot learning, chain-of-thought, and role-based prompting across 100 test cases with 7 categories and 3 difficulty levels.

## Key Constraints

- **API**: Uses Gemini API (key in `.env` file, never commit)
- **Mass Production Focus**: Optimize for consistency (low variance), not just accuracy
- **Metrics**: Accuracy, Mean, Variance, Embedding Distance, Histograms
- **Runs**: Each prompt tested 3x per case to measure consistency

## Project Structure

```
project6-prompt-engineering-research/
├── .env                  # GEMINI_API_KEY (git-ignored)
├── data/test_cases.csv   # 100 test cases
├── src/                  # Python modules
├── results/              # Raw results + figures
├── report/REPORT.md      # Final analysis
└── docs/                 # Implementation instructions
```

## Documentation

Detailed instructions in `docs/`:
- `stage-1-2-instructions.md` - Dataset creation & baseline
- `stage-3-instructions.md` - Prompt techniques
- `stage-4-instructions.md` - Visualization & report
