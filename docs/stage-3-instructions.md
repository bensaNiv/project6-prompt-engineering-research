# Stage 3: Prompt Improvement Techniques

## Overview

This stage tests different prompt engineering techniques against the baseline to measure improvement or deterioration in performance.

---

## Prompt Versions to Test

| Version | Name | Description |
|---------|------|-------------|
| 0 | **Baseline** | Minimal prompt, no techniques |
| 1 | **Improved Regular** | Better structured phrasing |
| 2 | **Few-Shot** | Include 3 examples per category |
| 3 | **Chain of Thought** | Add "Think step by step" |
| 4 | **Role-Based** | Assign expert role to model |

---

## Prompt Templates

### Version 0: Baseline

```
Answer the following question:
{question}
```

### Version 1: Improved Regular Prompt

Better structure, clear output format, constraints:

```
Question: {question}

Provide a clear and concise answer. Answer only with the final result, no explanation needed.
```

**For specific categories, add format hints:**

- **Sentiment:** `Respond with exactly one word: positive, negative, or neutral.`
- **Math:** `Respond with only the numerical answer.`
- **Logical:** `Respond with only: true or false.`
- **Classification:** `Respond with only the category name.`
- **Code Output:** `Respond with only what the code prints.`

### Version 2: Few-Shot Learning

Include 3 examples before the actual question:

```
Here are some examples:

Example 1:
Question: {example_1_question}
Answer: {example_1_answer}

Example 2:
Question: {example_2_question}
Answer: {example_2_answer}

Example 3:
Question: {example_3_question}
Answer: {example_3_answer}

Now answer this question:
Question: {question}
Answer:
```

**Few-Shot Example Bank:**

Create 3 examples per category (not from the test set):

| Category | Example Pool Size |
|----------|-------------------|
| Sentiment Analysis | 3 examples |
| Multi-step Math | 3 examples |
| Logical Reasoning | 3 examples |
| Text Classification | 3 examples |
| Reading Comprehension | 3 examples |
| Common Sense | 3 examples |
| Code Output | 3 examples |

**Important:** Examples should cover different difficulty levels and be representative of the category.

### Version 3: Chain of Thought (CoT)

Add explicit reasoning instruction:

```
Question: {question}

Let's think step by step:
1. First, identify what the question is asking.
2. Break down the problem into smaller parts.
3. Work through each part carefully.
4. Arrive at the final answer.

Think through this step by step, then provide your final answer.
```

**Simplified CoT (Alternative):**

```
Question: {question}

Think step by step before answering. Show your reasoning, then give the final answer.
```

**CoT with Format Constraint:**

```
Question: {question}

Think step by step, then provide your answer in this format:
Reasoning: [your step-by-step thinking]
Final Answer: [your answer]
```

### Version 4: Role-Based Prompting

Assign an expert role relevant to the category:

| Category | Role |
|----------|------|
| Sentiment Analysis | "You are an expert sentiment analyst with years of experience in NLP." |
| Multi-step Math | "You are a mathematics professor who specializes in problem-solving." |
| Logical Reasoning | "You are a logic professor and expert in formal reasoning." |
| Text Classification | "You are a content categorization expert with expertise in text analysis." |
| Reading Comprehension | "You are a reading comprehension expert and English teacher." |
| Common Sense | "You are an expert in common sense reasoning and everyday logic." |
| Code Output | "You are a senior software engineer who can trace code execution perfectly." |

**Template:**

```
{role_description}

Question: {question}

Provide your expert answer.
```

---

## Combined Techniques (Optional Advanced)

For deeper analysis, consider testing combinations:

| Combo | Techniques |
|-------|------------|
| A | Role-Based + CoT |
| B | Role-Based + Few-Shot |
| C | Few-Shot + CoT |
| D | Role-Based + Few-Shot + CoT |

---

## Implementation Details

### File Structure Additions

```
project/
├── src/
│   ├── prompts/
│   │   ├── baseline.py
│   │   ├── improved.py
│   │   ├── few_shot.py
│   │   ├── chain_of_thought.py
│   │   └── role_based.py
│   ├── few_shot_examples.json     # Example bank for few-shot
│   └── run_experiment.py          # Updated to support all versions
├── results/
│   ├── baseline_results.csv
│   ├── improved_results.csv
│   ├── few_shot_results.csv
│   ├── cot_results.csv
│   ├── role_based_results.csv
│   └── comparison_stats.json
```

### Few-Shot Examples File

**few_shot_examples.json:**

```json
{
  "sentiment": [
    {
      "question": "The service was terrible and the food was cold.",
      "answer": "negative"
    },
    {
      "question": "I had an amazing time at the concert!",
      "answer": "positive"
    },
    {
      "question": "The weather today is partly cloudy.",
      "answer": "neutral"
    }
  ],
  "math": [
    {
      "question": "If a book costs $12 and you buy 3, how much do you spend?",
      "answer": "36"
    },
    ...
  ],
  ...
}
```

### Prompt Generator Module

```python
# src/prompts/prompt_generator.py

class PromptGenerator:
    def __init__(self, few_shot_examples: dict, roles: dict):
        self.examples = few_shot_examples
        self.roles = roles

    def baseline(self, question: str) -> str:
        return f"Answer the following question:\n{question}"

    def improved(self, question: str, category: str) -> str:
        format_hints = {
            "sentiment": "Respond with exactly one word: positive, negative, or neutral.",
            "math": "Respond with only the numerical answer.",
            "logical": "Respond with only: true or false.",
            ...
        }
        hint = format_hints.get(category, "Provide a clear and concise answer.")
        return f"Question: {question}\n\n{hint}"

    def few_shot(self, question: str, category: str) -> str:
        examples = self.examples.get(category, [])
        example_text = "\n\n".join([
            f"Example {i+1}:\nQuestion: {ex['question']}\nAnswer: {ex['answer']}"
            for i, ex in enumerate(examples[:3])
        ])
        return f"Here are some examples:\n\n{example_text}\n\nNow answer this question:\nQuestion: {question}\nAnswer:"

    def chain_of_thought(self, question: str) -> str:
        return f"Question: {question}\n\nThink step by step, then provide your answer in this format:\nReasoning: [your step-by-step thinking]\nFinal Answer: [your answer]"

    def role_based(self, question: str, category: str) -> str:
        role = self.roles.get(category, "You are a helpful assistant.")
        return f"{role}\n\nQuestion: {question}\n\nProvide your expert answer."
```

### Experiment Runner

```python
# src/run_experiment.py

PROMPT_VERSIONS = ["baseline", "improved", "few_shot", "cot", "role_based"]

def run_all_experiments(test_cases: list, num_runs: int = 3):
    results = {version: [] for version in PROMPT_VERSIONS}

    for case in test_cases:
        for version in PROMPT_VERSIONS:
            prompt = generate_prompt(version, case)

            for run in range(num_runs):
                response, latency = query_gemini(prompt)
                correct = evaluate_answer(response, case["expected_answer"], case["answer_type"])

                results[version].append({
                    "id": case["id"],
                    "category": case["category"],
                    "difficulty": case["difficulty"],
                    "run": run + 1,
                    "response": response,
                    "correct": correct,
                    "latency_ms": latency
                })

    return results
```

---

## Metrics Comparison

### Per-Technique Metrics

For each prompt version, calculate:

| Metric | Description |
|--------|-------------|
| **Accuracy** | % correct answers |
| **Mean Score** | Average correctness |
| **Variance** | Consistency of results |
| **Std Dev** | Standard deviation |
| **Improvement %** | `(technique_accuracy - baseline_accuracy) / baseline_accuracy * 100` |

### Breakdown Analysis

Calculate metrics broken down by:
- **Category:** Which technique works best for each problem type?
- **Difficulty:** Do techniques help more on easy or hard problems?
- **Consistency:** Which technique has lowest variance (best for mass production)?

### Output: comparison_stats.json

```json
{
  "by_technique": {
    "baseline": {
      "accuracy": 0.65,
      "mean": 0.65,
      "variance": 0.23,
      "std_dev": 0.48
    },
    "improved": {
      "accuracy": 0.72,
      "mean": 0.72,
      "variance": 0.20,
      "improvement_pct": 10.8
    },
    "few_shot": {
      "accuracy": 0.78,
      "mean": 0.78,
      "variance": 0.17,
      "improvement_pct": 20.0
    },
    "cot": {
      "accuracy": 0.74,
      "mean": 0.74,
      "variance": 0.19,
      "improvement_pct": 13.8
    },
    "role_based": {
      "accuracy": 0.70,
      "mean": 0.70,
      "variance": 0.21,
      "improvement_pct": 7.7
    }
  },
  "by_category": {
    "math": {
      "baseline": 0.45,
      "cot": 0.72,
      "best_technique": "cot"
    },
    "sentiment": {
      "baseline": 0.80,
      "few_shot": 0.93,
      "best_technique": "few_shot"
    },
    ...
  },
  "by_difficulty": {
    "1": { ... },
    "2": { ... },
    "3": { ... }
  }
}
```

---

## API Call Budget

| Version | Cases | Runs | Total Calls |
|---------|-------|------|-------------|
| Baseline | 100 | 3 | 300 |
| Improved | 100 | 3 | 300 |
| Few-Shot | 100 | 3 | 300 |
| CoT | 100 | 3 | 300 |
| Role-Based | 100 | 3 | 300 |
| **Total** | - | - | **1,500** |

**Cost Consideration:** With Gemini 1.5 Flash pricing, estimate ~$0.075 per 1K input tokens. Plan token budget based on prompt lengths (Few-Shot and CoT will use more tokens).

---

## Implementation Checklist

### Prompt Development
- [ ] Finalize baseline prompt template
- [ ] Create improved prompt templates (per category)
- [ ] Create 21 few-shot examples (3 per category × 7 categories)
- [ ] Create CoT prompt templates
- [ ] Create role descriptions for all 7 categories
- [ ] Implement PromptGenerator class

### Experiment Execution
- [ ] Update run_experiment.py to support all versions
- [ ] Add progress tracking (100 cases × 5 versions × 3 runs)
- [ ] Implement rate limiting for API calls
- [ ] Add error handling and retry logic
- [ ] Save intermediate results (in case of failures)

### Analysis
- [ ] Calculate per-technique metrics
- [ ] Calculate breakdown by category
- [ ] Calculate breakdown by difficulty
- [ ] Generate comparison_stats.json
- [ ] Identify best technique per category

---

## Hypotheses to Test

Before running experiments, document expected outcomes:

1. **CoT will improve math scores significantly** (based on lecture: 18% → 58% improvement on GSM8K)
2. **Few-Shot will improve classification tasks** (sentiment, text classification)
3. **Role-Based will have moderate improvement across categories**
4. **Improved prompts will reduce variance** (better for mass production)
5. **All techniques will show diminishing returns on "Easy" problems**

Document actual results vs. hypotheses in the final analysis.

---

## Notes

- **Consistency Matters:** For mass production, a technique with 70% accuracy and low variance may be preferable to one with 75% accuracy and high variance.
- **Token Cost:** CoT and Few-Shot use more tokens. Factor this into the cost-benefit analysis.
- **Answer Extraction:** CoT responses need parsing to extract the final answer from the reasoning.
