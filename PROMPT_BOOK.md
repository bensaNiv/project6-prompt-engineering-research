# Prompt Book

This document catalogs the prompts (PRPs - Prompt Request Plans) used with **Claude Code** to build this project. Each PRP was executed sequentially to complete different stages of the research project.

## Overview

The project was built using a staged approach where each PRP instructed Claude Code to implement a specific phase. The PRPs are located in the `PRPs/` folder and were executed in order.

| Stage | PRP File | Purpose |
|-------|----------|---------|
| 0 | `00-project-overview.md` | Project structure and workflow overview |
| 1 | `01-stage-1-dataset.md` | Create the test dataset |
| 2 | `02-stage-2-baseline.md` | Implement baseline experiment |
| 3 | `03-stage-3-techniques.md` | Implement 4 prompt techniques |
| 4 | `04-stage-4-analysis.md` | Generate visualizations and report |

---

## PRP 00: Project Overview

**File:** `PRPs/00-project-overview.md`

**Purpose:** Establish project structure and define the workflow for subsequent stages.

**Prompt Given to Claude Code:**
```
# Project Overview: Prompt Engineering Research

## Objective
Measure how different prompt techniques affect LLM performance at scale (mass production context).

## Stages
| Stage | PRP File | Description |
|-------|----------|-------------|
| 1 | 01-stage-1-dataset.md | Create 100 test cases dataset |
| 2 | 02-stage-2-baseline.md | Run baseline prompts, collect metrics |
| 3 | 03-stage-3-techniques.md | Test 4 prompt improvement techniques |
| 4 | 04-stage-4-analysis.md | Generate visualizations and final report |

## Execution Order
Run stages sequentially: 1 → 2 → 3 → 4
```

**Outcome:** Claude Code understood the project scope and prepared for stage-by-stage execution.

---

## PRP 01: Stage 1 - Create Dataset

**File:** `PRPs/01-stage-1-dataset.md`

**Purpose:** Create a dataset of 100 test cases for the prompt engineering experiments.

**Prompt Given to Claude Code:**
```
# Stage 1: Create Dataset

## Goal
Create a dataset of 100 test cases across 7 categories and 3 difficulty levels.

## Prerequisites
- None (first stage)

## Instructions
Follow docs/stage-1-2-instructions.md — Stage 1: Dataset Creation section.

## Deliverables
- data/test_cases.csv — 100 test cases with columns: id, category, difficulty,
  question, expected_answer, answer_type

## Validation
- [ ] CSV has exactly 100 rows
- [ ] All 7 categories represented
- [ ] Difficulty levels 1, 2, 3 distributed correctly
- [ ] No empty fields

## Next Step
Run PRPs/02-stage-2-baseline.md
```

**Outcome:**
- Created `data/test_cases.csv` with 100 test cases
- Categories: sentiment, math, logic, classification, reading, commonsense, code
- Difficulty levels: Easy (1), Medium (2), Hard (3)

---

## PRP 02: Stage 2 - Baseline Experiment

**File:** `PRPs/02-stage-2-baseline.md`

**Purpose:** Implement the baseline prompt experiment infrastructure and run initial tests.

**Prompt Given to Claude Code:**
```
# Stage 2: Run Baseline Experiment

## Goal
Run baseline prompts on all test cases and collect performance metrics.

## Prerequisites
- Stage 1 completed
- data/test_cases.csv exists
- .env file with API key configured

## Instructions
Follow docs/stage-1-2-instructions.md — Stage 2: Baseline Measurement section.

## Deliverables
- src/ — Python modules (config, client, metrics, run_experiment)
- results/baseline_results.csv — Raw results
- results/baseline_stats.json — Aggregated statistics

## Validation
- [ ] Responses collected (100 cases × runs)
- [ ] Stats include: accuracy, mean, variance by category and difficulty
- [ ] No API errors in results

## Next Step
Run PRPs/03-stage-3-techniques.md
```

**Outcome:**
- Created `src/` module structure with:
  - `config.py` - Configuration management
  - `ollama_client.py` - LLM API client
  - `metrics.py` - Statistical calculations
  - `experiment_runner.py` - Test orchestration
  - `answer_evaluator.py` - Response evaluation
- Created `run_baseline.py` script
- Generated baseline results and statistics

---

## PRP 03: Stage 3 - Prompt Techniques

**File:** `PRPs/03-stage-3-techniques.md`

**Purpose:** Implement and test 4 different prompt improvement techniques.

**Prompt Given to Claude Code:**
```
# Stage 3: Test Prompt Improvement Techniques

## Goal
Run 4 prompt improvement techniques and compare against baseline.

## Prerequisites
- Stage 2 completed
- results/baseline_results.csv exists

## Instructions
Follow docs/stage-3-instructions.md — all sections.

## Techniques to Test
1. Improved Regular Prompt
2. Few-Shot Learning (3 examples)
3. Chain of Thought
4. Role-Based Prompting

## Deliverables
- src/prompts/ — Prompt generator modules
- results/improved_results.csv
- results/few_shot_results.csv
- results/cot_results.csv
- results/role_based_results.csv
- results/comparison_stats.json

## Validation
- [ ] All technique results collected
- [ ] Each technique has accuracy, mean, variance, improvement_pct
- [ ] Results broken down by category and difficulty

## Next Step
Run PRPs/04-stage-4-analysis.md
```

**Outcome:**
- Created `src/prompts/` module with:
  - `base.py` - BaselinePromptGenerator
  - `improved.py` - ImprovedPromptGenerator
  - `few_shot.py` - FewShotPromptGenerator
  - `chain_of_thought.py` - ChainOfThoughtPromptGenerator
  - `role_based.py` - RoleBasedPromptGenerator
- Created runner scripts: `run_improved.py`, `run_few_shot.py`, `run_cot.py`, `run_role_based.py`
- Generated comparison statistics

---

## PRP 04: Stage 4 - Analysis and Report

**File:** `PRPs/04-stage-4-analysis.md`

**Purpose:** Generate visualizations and create the final research report.

**Prompt Given to Claude Code:**
```
# Stage 4: Generate Visualizations and Report

## Goal
Create comprehensive visualizations and final analysis report.

## Prerequisites
- Stage 3 completed
- All result CSV files exist in results/
- results/comparison_stats.json exists

## Instructions
Follow docs/stage-4-instructions.md — all sections.

## Deliverables

### Visualizations
- results/figures/accuracy_by_technique.png
- results/figures/improvement_bars.png
- results/figures/accuracy_heatmap.png
- results/figures/difficulty_heatmap.png
- results/figures/variance_boxplot.png
- results/figures/radar_comparison.png
- results/figures/difficulty_trend.png
- results/figures/score_histograms.png

### Report
- report/REPORT.md — Full analysis with embedded figures

## Validation
- [ ] All 8 figures generated
- [ ] Report includes: Introduction, Methodology, Results, Discussion, Conclusion
- [ ] Hypothesis validation table completed
- [ ] Mass production recommendations included

## Project Complete
All stages finished. Review report/REPORT.md for final submission.
```

**Outcome:**
- Created `src/visualization.py` and `src/charts/` module
- Created `generate_figures.py` script
- Generated 8+ visualization figures
- Created `report/REPORT.md` with full analysis

---

## How PRPs Were Used

### Execution Process

1. **Open Claude Code** in the project directory
2. **Reference the PRP file**: `@PRPs/01-stage-1-dataset.md`
3. **Claude Code reads** the PRP and referenced documentation
4. **Claude Code executes** the instructions, creating files and running code
5. **Validate deliverables** using the checklist in the PRP
6. **Proceed to next stage** by referencing the next PRP file

### Example Session

```
User: @PRPs/02-stage-2-baseline.md

Claude Code: I'll implement Stage 2 - the baseline experiment. Let me:
1. Read the stage-1-2-instructions.md for details
2. Create the src/ module structure
3. Implement the baseline experiment runner
4. Run the experiment and collect results
...
```

### Benefits of PRP Approach

1. **Structured workflow** - Each stage has clear goals and deliverables
2. **Validation checklists** - Easy to verify completion
3. **Sequential dependencies** - Each PRP builds on previous work
4. **Documentation reference** - PRPs point to detailed docs for implementation
5. **Reproducibility** - Same prompts can recreate the project

---

## Additional Prompts Used

Beyond the main PRPs, additional Claude Code prompts were used for:

### Quality Checks
```
/quality-check @project6-prompt-engineering-research/
```
Used to verify code standards compliance after each stage.

### Bug Fixes and Improvements
```
Fix the failing tests in test_config.py - the Config class no longer requires api_key
```

### Documentation Updates
```
Update the README to reflect that we're using Ollama instead of Gemini API
```

---

## Lessons Learned

1. **Break work into stages** - PRPs work best when each has a focused goal
2. **Include validation criteria** - Checklists help verify completion
3. **Reference documentation** - Keep detailed docs separate from PRPs
4. **Sequential execution** - Dependencies between stages ensure proper order
5. **Iterate as needed** - Run quality checks and fix issues between stages
