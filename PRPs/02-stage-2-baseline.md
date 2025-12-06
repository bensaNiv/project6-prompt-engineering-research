# Stage 2: Run Baseline Experiment

## Goal
Run baseline prompts on all test cases and collect performance metrics.

## Prerequisites
- Stage 1 completed
- `data/test_cases.csv` exists
- `.env` file with `GEMINI_API_KEY` configured

## Instructions
Follow `docs/stage-1-2-instructions.md` — **Stage 2: Baseline Measurement** section.

## Deliverables
- `src/` — Python modules (config, gemini_client, metrics, run_experiment)
- `results/baseline_results.csv` — Raw results (3 runs per case)
- `results/baseline_stats.json` — Aggregated statistics

## Validation
- [ ] 300 responses collected (100 cases × 3 runs)
- [ ] Stats include: accuracy, mean, variance by category and difficulty
- [ ] No API errors in results

## Next Step
Run `PRPs/03-stage-3-techniques.md`
