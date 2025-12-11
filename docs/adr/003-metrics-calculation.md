# ADR 003: Metrics Calculation Approach

## Status

Accepted

## Date

2025-12-01

## Context

This research project compares prompt engineering techniques for mass production use cases. We need metrics that capture both:

1. **Accuracy**: How often does the technique produce correct answers?
2. **Consistency**: How reliable is the technique across multiple runs?

The key insight is that for production systems, a technique with 80% accuracy and low variance may be preferable to one with 85% accuracy but high variance.

Options considered:

1. **Accuracy only**: Simple percentage correct
2. **Accuracy + Variance**: Measure spread of results
3. **F1/Precision/Recall**: Classification metrics
4. **Custom composite score**: Weighted combination

## Decision

We use **Accuracy, Mean, and Variance** as primary metrics, with variance being the key differentiator for production suitability.

### Metrics Defined

| Metric | Formula | Purpose |
|--------|---------|---------|
| **Accuracy** | `correct / total` | Overall correctness rate |
| **Mean** | `sum(scores) / n` | Average correctness (same as accuracy for binary) |
| **Variance** | `sum((x - mean)^2) / n` | Consistency measure |
| **Improvement %** | `(new - baseline) / baseline * 100` | Relative change vs baseline |

### Why Variance Matters

Consider two techniques:
- **Technique A**: 80% accuracy, variance 0.16
- **Technique B**: 82% accuracy, variance 0.25

For mass production (thousands of automated calls):
- Technique A is more predictable - you know roughly what to expect
- Technique B has higher variance - some batches might be 70%, others 90%

**Lower variance = more suitable for production automation.**

### Implementation

```python
@dataclass
class TechniqueMetrics:
    accuracy: float      # Correct / Total
    mean: float          # Average score
    variance: float      # Score variance
    total_cases: int     # Number of test cases
    correct_count: int   # Number correct
```

## Consequences

### Positive

- **Production-relevant**: Variance captures real-world reliability concerns
- **Simple to understand**: Standard statistical measures
- **Comparable**: Same metrics across all techniques enable fair comparison
- **Actionable**: Clear recommendation (lowest variance + acceptable accuracy)

### Negative

- **Binary simplification**: Treats partial correctness as wrong
- **No category weighting**: All categories contribute equally
- **Sample size sensitivity**: Variance estimates improve with more runs

### Mitigation

- Run each case 2+ times to get meaningful variance
- Provide per-category breakdowns in addition to overall metrics
- Document confidence intervals where applicable

## Results Interpretation

From our experiments with `llama3.2:3b`:

| Technique | Accuracy | Variance | Production Recommendation |
|-----------|----------|----------|---------------------------|
| Baseline | 57.0% | 0.245 | Not recommended |
| Improved | 46.5% | 0.249 | Not recommended |
| Few-Shot | 52.0% | 0.250 | Not recommended |
| **CoT** | **84.0%** | **0.134** | **Recommended** |
| Role-Based | 59.5% | 0.241 | Acceptable fallback |

**Conclusion**: Chain-of-Thought achieves both highest accuracy AND lowest variance, making it optimal for mass production.

## References

- Course Lecture: "Prompt Engineering Techniques for Production"
- [Variance (Wikipedia)](https://en.wikipedia.org/wiki/Variance)
