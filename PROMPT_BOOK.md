# Prompt Book

This document catalogs all prompt engineering techniques used in this research project, including template structures, design rationale, and example outputs.

## Table of Contents
1. [Baseline Prompts](#1-baseline-prompts)
2. [Improved Prompts](#2-improved-prompts)
3. [Few-Shot Prompts](#3-few-shot-prompts)
4. [Chain-of-Thought Prompts](#4-chain-of-thought-prompts)
5. [Role-Based Prompts](#5-role-based-prompts)

---

## 1. Baseline Prompts

### Purpose
Establish a performance baseline with minimal prompt engineering.

### Template
```
Answer the following question:
{question}

Answer concisely with just the answer, no explanation.
```

### Design Rationale
- No formatting hints or structure
- Direct question presentation
- Simple conciseness instruction to reduce verbose outputs

### Example
**Input:**
```
Answer the following question:
What is the capital of France?

Answer concisely with just the answer, no explanation.
```

**Expected Output:** `Paris`

---

## 2. Improved Prompts

### Purpose
Add category-specific format constraints to improve answer consistency.

### Template
```
Question: {question}

{category_specific_hint}

Answer concisely with just the answer, no explanation.
```

### Category-Specific Hints
| Category | Hint |
|----------|------|
| sentiment | "Respond with exactly one word: positive, negative, or neutral." |
| math | "Respond with only the numerical answer." |
| logic | "Respond with only: yes or no." |
| classification | "Respond with only the category name." |
| reading | "Provide a brief, direct answer." |
| commonsense | "Provide a brief, direct answer." |
| code | "Respond with only what the code prints." |

### Example
**Input (math category):**
```
Question: What is 15 + 27?

Respond with only the numerical answer.

Answer concisely with just the answer, no explanation.
```

**Expected Output:** `42`

---

## 3. Few-Shot Prompts

### Purpose
Provide example Q&A pairs to demonstrate expected answer format.

### Template
```
Here are some examples of questions and answers:

{example_1}
{example_2}
{example_3}

Now answer this question in the same format:
Question: {question}
Answer:
```

### Design Rationale
- Shows the model expected answer format through examples
- Uses category-matched examples when possible
- Demonstrates concise answering style

### Example
**Input:**
```
Here are some examples of questions and answers:

Q: What is 5 + 3?
A: 8

Q: What is 10 - 4?
A: 6

Q: What is 7 * 2?
A: 14

Now answer this question in the same format:
Question: What is 15 + 27?
Answer:
```

**Expected Output:** `42`

---

## 4. Chain-of-Thought Prompts

### Purpose
Encourage step-by-step reasoning for complex problems.

### Template
```
Question: {question}

Let's think step by step:
1. First, identify what the question is asking.
2. Break down the problem into smaller parts.
3. Work through each part carefully.
4. Arrive at the final answer.

Think through this step by step, then provide your answer in this format:
Reasoning: [your step-by-step thinking]
Final Answer: [just the answer, no explanation]
```

### Design Rationale
- Explicit reasoning instructions guide logical problem-solving
- Structured output format separates reasoning from final answer
- Particularly effective for math, logic, and multi-step problems

### Example
**Input:**
```
Question: If a train travels 60 mph for 2 hours, how far does it go?

Let's think step by step:
1. First, identify what the question is asking.
2. Break down the problem into smaller parts.
3. Work through each part carefully.
4. Arrive at the final answer.

Think through this step by step, then provide your answer in this format:
Reasoning: [your step-by-step thinking]
Final Answer: [just the answer, no explanation]
```

**Expected Output:**
```
Reasoning: The question asks for distance. Distance = speed × time. Speed is 60 mph, time is 2 hours. So distance = 60 × 2 = 120 miles.
Final Answer: 120 miles
```

---

## 5. Role-Based Prompts

### Purpose
Assign expert roles to leverage domain-specific knowledge patterns.

### Template
```
You are a {role}.

{question}

Provide your expert answer. Be concise and give only the final answer.
```

### Role Assignments by Category
| Category | Role |
|----------|------|
| sentiment | "sentiment analysis expert" |
| math | "mathematics professor" |
| logic | "logic and reasoning expert" |
| classification | "classification specialist" |
| reading | "reading comprehension expert" |
| commonsense | "expert in everyday reasoning" |
| code | "senior software engineer" |

### Design Rationale
- Role assignment primes the model with domain expertise
- Expert framing may improve accuracy on specialized tasks
- Consistent with how humans approach problems in their expertise area

### Example
**Input:**
```
You are a mathematics professor.

What is the derivative of x^2?

Provide your expert answer. Be concise and give only the final answer.
```

**Expected Output:** `2x`

---

## Prompt Engineering Lessons Learned

### What Worked Well
1. **Explicit format constraints** reduced answer variability
2. **Category-specific hints** improved accuracy for structured answers
3. **Conciseness instructions** prevented verbose explanations

### What Could Be Improved
1. Chain-of-thought sometimes produces too much text
2. Few-shot examples need careful selection to match problem types
3. Role-based prompts less effective for simple factual questions

### Recommendations for Future Work
1. Test hybrid approaches (e.g., few-shot + chain-of-thought)
2. Experiment with negative examples ("Don't do X")
3. Try dynamic prompt selection based on question complexity
