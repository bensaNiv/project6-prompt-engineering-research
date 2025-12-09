"""Base chart configuration and utilities."""

from pathlib import Path

import matplotlib.pyplot as plt


TECHNIQUE_COLORS = {
    "baseline": "#808080",
    "improved": "#4CAF50",
    "few_shot": "#2196F3",
    "cot": "#FF9800",
    "role_based": "#9C27B0",
}

TECHNIQUE_LABELS = {
    "baseline": "Baseline",
    "improved": "Improved",
    "few_shot": "Few-Shot",
    "cot": "Chain-of-Thought",
    "role_based": "Role-Based",
}


class ChartBase:
    """
    Base class for chart generators.

    Parameters
    ----------
    figures_dir : str
        Directory for saving figures.
    """

    def __init__(self, figures_dir: str = "results/figures") -> None:
        """Initialize the chart generator."""
        self.figures_dir = Path(figures_dir)
        self.figures_dir.mkdir(parents=True, exist_ok=True)
        plt.style.use("seaborn-v0_8-whitegrid")

    def save_figure(self, filename: str) -> None:
        """Save the current figure."""
        plt.tight_layout()
        plt.savefig(self.figures_dir / filename, dpi=150, bbox_inches="tight")
        plt.close()

    def get_color(self, technique: str) -> str:
        """Get color for a technique."""
        return TECHNIQUE_COLORS.get(technique, "#808080")

    def get_label(self, technique: str) -> str:
        """Get display label for a technique."""
        return TECHNIQUE_LABELS.get(technique, technique)
