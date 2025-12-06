# Stage 1 & 2: Dataset Creation and Baseline Measurement

## Overview

This document outlines the implementation plan for:
- **Stage 1:** Creating a diverse test dataset
- **Stage 2:** Running baseline prompts and collecting metrics

---

## Stage 1: Dataset Creation

### Dataset Schema

Each test case will have the following fields:

| Field | Type | Description |
|-------|------|-------------|
| `id` | int | Unique identifier |
| `category` | string | Problem category (see below) |
| `difficulty` | int | 1=Easy, 2=Medium, 3=Hard |
| `question` | string | The input prompt/question |
| `expected_answer` | string | The correct/expected response |
| `answer_type` | string | `exact`, `contains`, `semantic`, `numeric` |

### Categories and Distribution (~100 cases)

| Category | Total Cases | Easy | Medium | Hard |
|----------|-------------|------|--------|------|
| Sentiment Analysis | 15 | 5 | 5 | 5 |
| Multi-step Math | 20 | 6 | 7 | 7 |
| Logical Reasoning | 15 | 5 | 5 | 5 |
| Text Classification | 15 | 5 | 5 | 5 |
| Reading Comprehension | 15 | 5 | 5 | 5 |
| Common Sense Reasoning | 10 | 3 | 4 | 3 |
| Code Output Prediction | 10 | 3 | 4 | 3 |
| **Total** | **100** | **32** | **35** | **33** |

### Category Definitions

#### 1. Sentiment Analysis
Classify text sentiment as positive, negative, or neutral.

**Difficulty Levels:**
- **Easy:** Clear, single-emotion statements ("I love this product!")
- **Medium:** Mixed signals or sarcasm ("Not bad, I guess")
- **Hard:** Subtle sentiment, context-dependent, or ironic text

#### 2. Multi-step Math
Arithmetic problems requiring 2-4 calculation steps.

**Difficulty Levels:**
- **Easy:** 2 operations, single-digit numbers
- **Medium:** 3 operations, double-digit numbers
- **Hard:** 4+ operations, fractions, or percentages

#### 3. Logical Reasoning
Syllogisms, if-then statements, and deductive reasoning.

**Difficulty Levels:**
- **Easy:** Simple two-premise syllogisms
- **Medium:** Three premises or basic negation
- **Hard:** Multiple negations, contrapositive reasoning

#### 4. Text Classification
Categorize text by topic, intent, or type.

**Difficulty Levels:**
- **Easy:** Clear single-topic text
- **Medium:** Overlapping categories possible
- **Hard:** Ambiguous or multi-topic text

#### 5. Reading Comprehension
Extract specific information from short passages.

**Difficulty Levels:**
- **Easy:** Explicitly stated facts
- **Medium:** Requires simple inference
- **Hard:** Requires synthesizing multiple sentences

#### 6. Common Sense Reasoning
Everyday logic and world knowledge questions.

**Difficulty Levels:**
- **Easy:** Basic physical/social facts
- **Medium:** Requires multi-step common sense
- **Hard:** Counter-intuitive or edge cases

#### 7. Code Output Prediction
Predict the output of short code snippets.

**Difficulty Levels:**
- **Easy:** Simple print statements, basic arithmetic
- **Medium:** Loops, conditionals
- **Hard:** Recursion, edge cases, type coercion

### Dataset File Format

Store as CSV in `data/test_cases.csv`:

```csv
id,category,difficulty,question,expected_answer,answer_type
1,sentiment,1,"The movie was fantastic and I loved every minute!",positive,exact
2,math,2,"If John has 15 apples and gives 3 to each of his 4 friends, how many does he have left?",3,numeric
...
```

---

## Stage 2: Baseline Measurement

### Project Structure

```
project/
├── .env                        # API credentials
├── .gitignore                  # Ignore .env file
├── data/
│   └── test_cases.csv          # The dataset
├── src/
│   ├── config.py               # Load environment variables
│   ├── gemini_client.py        # Gemini API wrapper
│   ├── run_experiment.py       # Execute prompts
│   ├── metrics.py              # Calculate metrics
│   └── utils.py                # Helper functions
├── results/
│   ├── baseline_results.csv    # Raw results
│   └── baseline_stats.json     # Aggregated statistics
└── docs/
    └── stage-1-2-instructions.md
```

### Environment Setup

**.env file:**
```
GEMINI_API_KEY=your_api_key_here
```

**.gitignore:**
```
.env
results/
__pycache__/
```

### Gemini API Integration

**Dependencies:**
```
google-generativeai
python-dotenv
pandas
numpy
scikit-learn  # for embeddings/distance metrics
matplotlib    # for histograms
```

**Basic API Call Pattern:**
```python
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def query_gemini(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text
```

### Baseline Prompt

The baseline prompt should be minimal - no special techniques:

```
Answer the following question:
{question}
```

### Metrics to Collect

#### Per-Response Metrics

| Metric | Description | Calculation |
|--------|-------------|-------------|
| `correct` | Binary correctness | Based on `answer_type` matching |
| `response_length` | Token/character count | `len(response)` |
| `latency_ms` | Response time | Time API call |

#### Aggregated Metrics

| Metric | Description | Formula |
|--------|-------------|---------|
| **Accuracy** | Proportion correct | `correct_count / total_count` |
| **Mean Score** | Average correctness | `sum(scores) / n` |
| **Variance** | Score spread | `sum((x - mean)^2) / n` |
| **Std Dev** | Score deviation | `sqrt(variance)` |

#### Consistency Metrics (for Mass Production)

Run each prompt **3 times** to measure consistency:

| Metric | Description | Goal |
|--------|-------------|------|
| **Response Variance** | How much answers differ across runs | Lower = better |
| **Agreement Rate** | % of runs with same answer | Higher = better |

#### Embedding Distance (Semantic Similarity)

For non-exact answers, measure semantic similarity:

```python
from sklearn.metrics.pairwise import cosine_similarity

def semantic_distance(expected_embedding, actual_embedding):
    return 1 - cosine_similarity([expected_embedding], [actual_embedding])[0][0]
```

### Output Format

**baseline_results.csv:**
```csv
id,category,difficulty,question,expected,response_1,response_2,response_3,correct_1,correct_2,correct_3,latency_1,latency_2,latency_3
```

**baseline_stats.json:**
```json
{
  "overall": {
    "accuracy": 0.65,
    "mean": 0.65,
    "variance": 0.23,
    "std_dev": 0.48
  },
  "by_category": {
    "sentiment": {"accuracy": 0.80, "mean": 0.80, "variance": 0.16},
    "math": {"accuracy": 0.45, "mean": 0.45, "variance": 0.25},
    ...
  },
  "by_difficulty": {
    "1": {"accuracy": 0.78, "mean": 0.78},
    "2": {"accuracy": 0.62, "mean": 0.62},
    "3": {"accuracy": 0.51, "mean": 0.51}
  }
}
```

### Visualization

Generate histograms for:
1. **Accuracy by category** (bar chart)
2. **Accuracy by difficulty** (bar chart)
3. **Score distribution** (histogram)
4. **Consistency across runs** (variance plot)

---

## Implementation Checklist

### Stage 1 Tasks
- [ ] Create project folder structure
- [ ] Create `.env` and `.gitignore` files
- [ ] Design 15 Sentiment Analysis cases (5 per difficulty)
- [ ] Design 20 Multi-step Math cases (6/7/7 split)
- [ ] Design 15 Logical Reasoning cases (5 per difficulty)
- [ ] Design 15 Text Classification cases (5 per difficulty)
- [ ] Design 15 Reading Comprehension cases (5 per difficulty)
- [ ] Design 10 Common Sense cases (3/4/3 split)
- [ ] Design 10 Code Output cases (3/4/3 split)
- [ ] Validate dataset (no duplicates, balanced distribution)

### Stage 2 Tasks
- [ ] Set up Python environment with dependencies
- [ ] Implement `config.py` for environment loading
- [ ] Implement `gemini_client.py` API wrapper
- [ ] Implement answer matching logic (exact, contains, numeric, semantic)
- [ ] Implement `run_experiment.py` to execute baseline
- [ ] Implement `metrics.py` for statistical calculations
- [ ] Run baseline experiment (3 runs per case)
- [ ] Generate results CSV and stats JSON
- [ ] Create visualization charts

---

## Notes

- **Mass Production Context:** The goal is to find prompts that work consistently at scale. Variance matters as much as accuracy.
- **Entropy Principle:** Lower entropy (more consistent outputs) is desirable.
- **Budget Consideration:** 100 cases × 3 runs = 300 API calls for baseline alone. Plan accordingly for Gemini API costs.
