# Stage 3: Test Prompt Improvement Techniques

## Goal
Run 4 prompt improvement techniques and compare against baseline.

## Prerequisites
- Stage 2 completed
- `results/baseline_results.csv` exists
- `.env` file with `GEMINI_API_KEY` configured

## Instructions
Follow `docs/stage-3-instructions.md` — all sections.

## Techniques to Test
1. Improved Regular Prompt
2. Few-Shot Learning (3 examples)
3. Chain of Thought
4. Role-Based Prompting

## Deliverables
- `src/prompts/` — Prompt generator modules
- `src/few_shot_examples.json` — Example bank for few-shot
- `results/improved_results.csv`
- `results/few_shot_results.csv`
- `results/cot_results.csv`
- `results/role_based_results.csv`
- `results/comparison_stats.json`

## Validation
- [ ] 1,200 responses collected (100 cases × 4 techniques × 3 runs)
- [ ] Each technique has accuracy, mean, variance, improvement_pct
- [ ] Results broken down by category and difficulty

## Next Step
Run `PRPs/04-stage-4-analysis.md`
