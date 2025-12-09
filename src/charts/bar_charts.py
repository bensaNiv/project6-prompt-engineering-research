"""Bar chart generators for accuracy and improvement visualization."""

import matplotlib.pyplot as plt
import pandas as pd

from .base import ChartBase


class BarChartGenerator(ChartBase):
    """Generator for bar chart visualizations."""

    def plot_accuracy_comparison(
        self, stats: dict, filename: str = "accuracy_by_technique.png"
    ) -> None:
        """
        Create bar chart comparing accuracy across techniques.

        Parameters
        ----------
        stats : dict
            Statistics dictionary with 'by_technique' key.
        filename : str
            Output filename.
        """
        techniques = list(stats["by_technique"].keys())
        accuracies = [stats["by_technique"][t]["accuracy"] for t in techniques]
        colors = [self.get_color(t) for t in techniques]
        labels = [self.get_label(t) for t in techniques]

        plt.figure(figsize=(10, 6))
        bars = plt.bar(labels, accuracies, color=colors)

        for bar, acc in zip(bars, accuracies):
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.01,
                f"{acc:.1%}",
                ha="center",
                va="bottom",
                fontsize=12,
            )

        plt.ylabel("Accuracy")
        plt.title("Accuracy Comparison by Prompt Technique")
        plt.ylim(0, 1.1)
        self.save_figure(filename)

    def plot_improvement_bars(
        self, stats: dict, filename: str = "improvement_bars.png"
    ) -> None:
        """
        Create bar chart showing improvement over baseline.

        Parameters
        ----------
        stats : dict
            Statistics dictionary with improvement percentages.
        filename : str
            Output filename.
        """
        techniques = [t for t in stats["by_technique"] if t != "baseline"]
        improvements = [
            stats["by_technique"][t].get("improvement_pct", 0) for t in techniques
        ]
        labels = [self.get_label(t) for t in techniques]
        colors = ["green" if x >= 0 else "red" for x in improvements]

        plt.figure(figsize=(10, 6))
        plt.bar(labels, improvements, color=colors)
        plt.axhline(y=0, color="black", linestyle="-", linewidth=0.5)
        plt.ylabel("Improvement vs Baseline (%)")
        plt.title("Performance Change vs Baseline")
        self.save_figure(filename)

    def plot_variance_boxplot(
        self,
        results: dict[str, pd.DataFrame],
        filename: str = "variance_boxplot.png",
    ) -> None:
        """
        Create box plot showing score distribution by technique.

        Parameters
        ----------
        results : dict
            Dictionary mapping technique names to result DataFrames.
        filename : str
            Output filename.
        """
        data = []
        labels = []
        colors = []

        for technique, df in results.items():
            data.append(df["correct"].values)
            labels.append(self.get_label(technique))
            colors.append(self.get_color(technique))

        plt.figure(figsize=(10, 6))
        bp = plt.boxplot(data, labels=labels, patch_artist=True)

        for patch, color in zip(bp["boxes"], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)

        plt.ylabel("Correctness Score")
        plt.title("Score Distribution by Technique")
        self.save_figure(filename)
