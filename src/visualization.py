"""Visualization facade for generating all experiment result charts."""

import pandas as pd

from .charts import BarChartGenerator, HeatmapGenerator, LineChartGenerator


class PromptResearchVisualizer:
    """
    Visualizer for prompt engineering research results.

    Provides a unified interface for generating all visualization types.

    Parameters
    ----------
    results_dir : str
        Directory containing results and for saving figures.
    """

    def __init__(self, results_dir: str = "results") -> None:
        """Initialize the visualizer with chart generators."""
        figures_dir = f"{results_dir}/figures"
        self.bar_charts = BarChartGenerator(figures_dir)
        self.heatmaps = HeatmapGenerator(figures_dir)
        self.line_charts = LineChartGenerator(figures_dir)

    def plot_accuracy_comparison(
        self, stats: dict, filename: str = "accuracy_by_technique.png"
    ) -> None:
        """Create bar chart comparing accuracy across techniques."""
        self.bar_charts.plot_accuracy_comparison(stats, filename)

    def plot_improvement_bars(
        self, stats: dict, filename: str = "improvement_bars.png"
    ) -> None:
        """Create bar chart showing improvement over baseline."""
        self.bar_charts.plot_improvement_bars(stats, filename)

    def plot_accuracy_heatmap(
        self,
        results: dict[str, pd.DataFrame],
        filename: str = "accuracy_heatmap.png",
    ) -> None:
        """Create heatmap of accuracy by technique and category."""
        self.heatmaps.plot_accuracy_heatmap(results, filename)

    def plot_difficulty_trend(
        self,
        results: dict[str, pd.DataFrame],
        filename: str = "difficulty_trend.png",
    ) -> None:
        """Create line chart showing accuracy by difficulty level."""
        self.line_charts.plot_difficulty_trend(results, filename)

    def plot_variance_boxplot(
        self,
        results: dict[str, pd.DataFrame],
        filename: str = "variance_boxplot.png",
    ) -> None:
        """Create box plot showing score distribution by technique."""
        self.bar_charts.plot_variance_boxplot(results, filename)

    def generate_all_figures(
        self, stats: dict, results: dict[str, pd.DataFrame]
    ) -> None:
        """
        Generate all visualization figures.

        Parameters
        ----------
        stats : dict
            Comparison statistics dictionary.
        results : dict
            Dictionary mapping technique names to result DataFrames.
        """
        self.plot_accuracy_comparison(stats)
        self.plot_improvement_bars(stats)
        self.plot_accuracy_heatmap(results)
        self.plot_difficulty_trend(results)
        self.plot_variance_boxplot(results)
