# Stage 4: Comparison and Presentation

## Overview

This stage focuses on visualizing results and presenting findings with comprehensive analysis.

---

## Final Deliverable Structure

```
project/
├── src/
│   ├── visualization.py          # All chart generation code
│   └── analysis.py               # Statistical analysis functions
├── results/
│   ├── raw/                      # Raw experiment data
│   │   ├── baseline_results.csv
│   │   ├── improved_results.csv
│   │   ├── few_shot_results.csv
│   │   ├── cot_results.csv
│   │   └── role_based_results.csv
│   ├── stats/
│   │   └── comparison_stats.json
│   └── figures/                  # Generated charts
│       ├── accuracy_by_technique.png
│       ├── accuracy_heatmap.png
│       ├── variance_boxplot.png
│       ├── radar_comparison.png
│       ├── difficulty_trend.png
│       └── ...
├── report/
│   ├── REPORT.md                 # Main analysis report
│   └── figures/                  # Figures embedded in report
└── docs/
```

---

## Visualization Suite

### 1. Bar Charts

#### A. Overall Accuracy by Technique

**Purpose:** Compare raw accuracy across all 5 prompt versions.

```python
import matplotlib.pyplot as plt
import numpy as np

def plot_accuracy_comparison(stats: dict):
    techniques = ['Baseline', 'Improved', 'Few-Shot', 'CoT', 'Role-Based']
    accuracies = [stats[t]['accuracy'] for t in techniques]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(techniques, accuracies, color=['#808080', '#4CAF50', '#2196F3', '#FF9800', '#9C27B0'])

    # Add value labels on bars
    for bar, acc in zip(bars, accuracies):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                 f'{acc:.1%}', ha='center', va='bottom', fontsize=12)

    plt.ylabel('Accuracy')
    plt.title('Accuracy Comparison by Prompt Technique')
    plt.ylim(0, 1)
    plt.savefig('results/figures/accuracy_by_technique.png', dpi=150, bbox_inches='tight')
```

#### B. Improvement Percentage vs Baseline

**Purpose:** Show relative improvement/deterioration.

```python
def plot_improvement_bars(stats: dict):
    techniques = ['Improved', 'Few-Shot', 'CoT', 'Role-Based']
    improvements = [stats[t]['improvement_pct'] for t in techniques]

    colors = ['green' if x >= 0 else 'red' for x in improvements]

    plt.figure(figsize=(10, 6))
    plt.bar(techniques, improvements, color=colors)
    plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    plt.ylabel('Improvement vs Baseline (%)')
    plt.title('Performance Change vs Baseline')
    plt.savefig('results/figures/improvement_bars.png', dpi=150, bbox_inches='tight')
```

---

### 2. Heatmaps

#### A. Technique × Category Accuracy Heatmap

**Purpose:** Show which techniques work best for which categories.

```python
import seaborn as sns

def plot_accuracy_heatmap(stats: dict):
    categories = ['Sentiment', 'Math', 'Logical', 'Classification', 'Comprehension', 'Common Sense', 'Code']
    techniques = ['Baseline', 'Improved', 'Few-Shot', 'CoT', 'Role-Based']

    # Create accuracy matrix
    data = np.array([[stats[t][c]['accuracy'] for c in categories] for t in techniques])

    plt.figure(figsize=(12, 6))
    sns.heatmap(data, annot=True, fmt='.2f', cmap='RdYlGn',
                xticklabels=categories, yticklabels=techniques,
                vmin=0, vmax=1, center=0.5)
    plt.title('Accuracy Heatmap: Technique × Category')
    plt.tight_layout()
    plt.savefig('results/figures/accuracy_heatmap.png', dpi=150, bbox_inches='tight')
```

#### B. Technique × Difficulty Heatmap

**Purpose:** Show how techniques perform across difficulty levels.

```python
def plot_difficulty_heatmap(stats: dict):
    difficulties = ['Easy (1)', 'Medium (2)', 'Hard (3)']
    techniques = ['Baseline', 'Improved', 'Few-Shot', 'CoT', 'Role-Based']

    data = np.array([[stats[t][d]['accuracy'] for d in [1, 2, 3]] for t in techniques])

    plt.figure(figsize=(8, 6))
    sns.heatmap(data, annot=True, fmt='.2f', cmap='RdYlGn',
                xticklabels=difficulties, yticklabels=techniques,
                vmin=0, vmax=1, center=0.5)
    plt.title('Accuracy Heatmap: Technique × Difficulty')
    plt.savefig('results/figures/difficulty_heatmap.png', dpi=150, bbox_inches='tight')
```

---

### 3. Box Plots

#### A. Variance/Consistency Box Plot

**Purpose:** Show distribution and consistency of results across 3 runs.

```python
def plot_variance_boxplot(results: dict):
    data = []
    labels = []
    for technique in ['Baseline', 'Improved', 'Few-Shot', 'CoT', 'Role-Based']:
        scores = [r['correct'] for r in results[technique]]
        data.append(scores)
        labels.append(technique)

    plt.figure(figsize=(10, 6))
    bp = plt.boxplot(data, labels=labels, patch_artist=True)

    colors = ['#808080', '#4CAF50', '#2196F3', '#FF9800', '#9C27B0']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    plt.ylabel('Correctness Score')
    plt.title('Score Distribution by Technique (Lower variance = Better for Mass Production)')
    plt.savefig('results/figures/variance_boxplot.png', dpi=150, bbox_inches='tight')
```

#### B. Category-wise Box Plot

**Purpose:** Show score distribution per category across all techniques.

```python
def plot_category_boxplot(results: dict, category: str):
    # Create grouped box plot for one category across all techniques
    ...
```

---

### 4. Radar Charts

#### A. Multi-Dimensional Technique Comparison

**Purpose:** Compare techniques across multiple metrics simultaneously.

```python
from math import pi

def plot_radar_comparison(stats: dict):
    categories = ['Accuracy', 'Consistency', 'Math Score', 'Reasoning Score', 'Token Efficiency']
    techniques = ['Baseline', 'Improved', 'Few-Shot', 'CoT', 'Role-Based']

    # Number of variables
    N = len(categories)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]  # Close the polygon

    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))

    colors = ['#808080', '#4CAF50', '#2196F3', '#FF9800', '#9C27B0']

    for i, technique in enumerate(techniques):
        values = get_radar_values(stats, technique)  # Normalize to 0-1
        values += values[:1]

        ax.plot(angles, values, 'o-', linewidth=2, label=technique, color=colors[i])
        ax.fill(angles, values, alpha=0.1, color=colors[i])

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    ax.set_ylim(0, 1)
    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
    plt.title('Multi-Dimensional Technique Comparison')
    plt.savefig('results/figures/radar_comparison.png', dpi=150, bbox_inches='tight')
```

---

### 5. Line Charts

#### A. Accuracy Trend by Difficulty

**Purpose:** Show how each technique degrades as difficulty increases.

```python
def plot_difficulty_trend(stats: dict):
    difficulties = [1, 2, 3]
    techniques = ['Baseline', 'Improved', 'Few-Shot', 'CoT', 'Role-Based']
    colors = ['#808080', '#4CAF50', '#2196F3', '#FF9800', '#9C27B0']

    plt.figure(figsize=(10, 6))

    for technique, color in zip(techniques, colors):
        accuracies = [stats[technique][d]['accuracy'] for d in difficulties]
        plt.plot(difficulties, accuracies, 'o-', label=technique, color=color, linewidth=2, markersize=8)

    plt.xlabel('Difficulty Level')
    plt.ylabel('Accuracy')
    plt.title('Accuracy Degradation by Difficulty')
    plt.xticks([1, 2, 3], ['Easy', 'Medium', 'Hard'])
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('results/figures/difficulty_trend.png', dpi=150, bbox_inches='tight')
```

---

### 6. Histogram

#### A. Score Distribution Histogram

**Purpose:** Show the distribution of correctness scores.

```python
def plot_score_histogram(results: dict):
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()

    techniques = ['Baseline', 'Improved', 'Few-Shot', 'CoT', 'Role-Based']
    colors = ['#808080', '#4CAF50', '#2196F3', '#FF9800', '#9C27B0']

    for i, (technique, color) in enumerate(zip(techniques, colors)):
        scores = [r['correct'] for r in results[technique]]
        axes[i].hist(scores, bins=2, color=color, edgecolor='black', alpha=0.7)
        axes[i].set_title(f'{technique} Score Distribution')
        axes[i].set_xlabel('Correct (0 or 1)')
        axes[i].set_ylabel('Count')

    # Hide empty subplot
    axes[5].axis('off')

    plt.tight_layout()
    plt.savefig('results/figures/score_histograms.png', dpi=150, bbox_inches='tight')
```

---

## Report Template

### REPORT.md Structure

```markdown
# Prompt Engineering Research Report

## Executive Summary
- Brief overview of findings
- Best performing technique overall
- Key insights for mass production

## 1. Introduction
- Research question
- Hypothesis statements
- Dataset overview

## 2. Methodology
### 2.1 Dataset Description
- Categories and distribution
- Difficulty levels
- Sample questions

### 2.2 Prompt Techniques Tested
- Baseline description
- Each technique with examples

### 2.3 Evaluation Metrics
- Accuracy, Mean, Variance definitions
- How consistency was measured

## 3. Results

### 3.1 Overall Performance
![Accuracy Comparison](figures/accuracy_by_technique.png)

| Technique | Accuracy | Mean | Variance | Improvement |
|-----------|----------|------|----------|-------------|
| Baseline  | X%       | X.XX | X.XX     | -           |
| ...       | ...      | ...  | ...      | ...         |

### 3.2 Performance by Category
![Accuracy Heatmap](figures/accuracy_heatmap.png)

**Key Findings:**
- CoT showed X% improvement on math problems
- Few-Shot was most effective for sentiment analysis
- ...

### 3.3 Performance by Difficulty
![Difficulty Trend](figures/difficulty_trend.png)

**Analysis:**
- All techniques showed degradation on hard problems
- CoT maintained best performance on difficult cases
- ...

### 3.4 Consistency Analysis (Mass Production)
![Variance Boxplot](figures/variance_boxplot.png)

**For Mass Production:**
- Technique X has lowest variance (most consistent)
- Tradeoff between accuracy and consistency
- ...

### 3.5 Multi-Dimensional Comparison
![Radar Chart](figures/radar_comparison.png)

## 4. Discussion

### 4.1 Hypothesis Validation
| Hypothesis | Result | Explanation |
|------------|--------|-------------|
| CoT improves math | ✓/✗ | ... |
| ... | ... | ... |

### 4.2 Why Techniques Helped or Hurt
- **Improved Prompts:** Better format constraints reduced ambiguity
- **Few-Shot:** Examples anchored model expectations
- **CoT:** Step-by-step reasoning prevented shortcuts
- **Role-Based:** Expert persona activated relevant knowledge

### 4.3 Recommendations for Mass Production
Based on entropy minimization principle:
1. For high-accuracy needs: Use [X]
2. For consistency: Use [Y]
3. For cost-efficiency: Use [Z]

## 5. Limitations
- Dataset size (100 cases)
- Single model (Gemini)
- Limited run count (3 per case)

## 6. Conclusion
- Summary of findings
- Best practices identified
- Future work suggestions

## Appendix
- A: Full dataset
- B: All prompt templates used
- C: Raw statistical data
```

---

## Visualization Code Organization

### visualization.py

```python
"""
Visualization module for prompt engineering research.
Generates all charts and saves to results/figures/
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from math import pi
import json

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

class PromptResearchVisualizer:
    def __init__(self, results_dir: str = 'results'):
        self.results_dir = results_dir
        self.figures_dir = f'{results_dir}/figures'
        self.colors = {
            'baseline': '#808080',
            'improved': '#4CAF50',
            'few_shot': '#2196F3',
            'cot': '#FF9800',
            'role_based': '#9C27B0'
        }

    def load_results(self):
        """Load all result CSV files and stats JSON"""
        ...

    def generate_all_figures(self):
        """Generate all visualizations"""
        self.plot_accuracy_comparison()
        self.plot_improvement_bars()
        self.plot_accuracy_heatmap()
        self.plot_difficulty_heatmap()
        self.plot_variance_boxplot()
        self.plot_radar_comparison()
        self.plot_difficulty_trend()
        self.plot_score_histograms()

    def save_figure(self, name: str):
        """Save current figure to figures directory"""
        plt.savefig(f'{self.figures_dir}/{name}.png', dpi=150, bbox_inches='tight')
        plt.close()

    # Individual plot methods...
```

---

## Implementation Checklist

### Visualization Development
- [ ] Set up matplotlib/seaborn styling
- [ ] Implement `plot_accuracy_comparison()` bar chart
- [ ] Implement `plot_improvement_bars()` chart
- [ ] Implement `plot_accuracy_heatmap()` (technique × category)
- [ ] Implement `plot_difficulty_heatmap()` (technique × difficulty)
- [ ] Implement `plot_variance_boxplot()`
- [ ] Implement `plot_radar_comparison()`
- [ ] Implement `plot_difficulty_trend()` line chart
- [ ] Implement `plot_score_histograms()`
- [ ] Create visualization.py module

### Report Writing
- [ ] Create REPORT.md template
- [ ] Write Introduction section
- [ ] Write Methodology section
- [ ] Document all figures with captions
- [ ] Write Discussion with insights
- [ ] Add hypothesis validation table
- [ ] Write recommendations for mass production
- [ ] Complete Appendix

### Final Quality Check
- [ ] All figures render correctly
- [ ] Report markdown displays properly
- [ ] Statistics are accurate
- [ ] Insights are data-driven
- [ ] Critical thinking is demonstrated

---

## Dependencies

```
# requirements.txt additions for Stage 4
matplotlib>=3.7.0
seaborn>=0.12.0
numpy>=1.24.0
pandas>=2.0.0
```

---

## Key Insights to Highlight

When writing the report, emphasize:

1. **What Helped and Why** - Connect improvements to lecture concepts (entropy reduction, information bottleneck)

2. **What Hurt and Why** - Document any techniques that decreased performance and explain

3. **Mass Production Relevance** - Emphasize consistency over single-run accuracy

4. **Category-Specific Recommendations** - Which technique for which problem type

5. **Cost-Benefit Analysis** - Token usage vs. improvement tradeoff
