# Stage 1: Create Dataset

## Goal
Create a dataset of 100 test cases across 7 categories and 3 difficulty levels.

## Prerequisites
- None (first stage)

## Instructions
Follow `docs/stage-1-2-instructions.md` — **Stage 1: Dataset Creation** section.

## Deliverables
- `data/test_cases.csv` — 100 test cases with columns: id, category, difficulty, question, expected_answer, answer_type

## Validation
- [ ] CSV has exactly 100 rows
- [ ] All 7 categories represented
- [ ] Difficulty levels 1, 2, 3 distributed correctly
- [ ] No empty fields

## Next Step
Run `PRPs/02-stage-2-baseline.md`
