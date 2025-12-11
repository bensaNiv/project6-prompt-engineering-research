"""Specialized chart generators for radar and histogram visualizations."""

from math import pi

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .base import ChartBase


class SpecializedChartGenerator(ChartBase):
    """Generator for specialized visualizations (radar, histograms)."""

    def plot_radar_comparison(
        self,
        stats: dict,
        results: dict[str, pd.DataFrame],
        filename: str = "radar_comparison.png",
    ) -> None:
        """
        Create radar chart comparing techniques across multiple metrics.

        Parameters
        ----------
        stats : dict
            Statistics dictionary with technique data.
        results : dict
            Dictionary mapping technique names to result DataFrames.
        filename : str
            Output filename.
        """
        categories = ["Accuracy", "Consistency", "Math", "Logic", "Reading"]
        techniques = list(results.keys())
        N = len(categories)
        angles = [n / float(N) * 2 * pi for n in range(N)]
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))

        for technique in techniques:
            df = results[technique]
            tech_stats = stats["by_technique"].get(technique, {})

            # Calculate metrics
            accuracy = tech_stats.get("accuracy", df["correct"].mean())
            variance = tech_stats.get("variance", df["correct"].var())
            consistency = 1 - min(variance, 1)  # Invert variance for consistency

            # Category-specific accuracy
            math_acc = df[df["category"] == "math"]["correct"].mean() if len(df[df["category"] == "math"]) > 0 else 0
            logic_acc = df[df["category"] == "logic"]["correct"].mean() if len(df[df["category"] == "logic"]) > 0 else 0
            reading_acc = df[df["category"] == "reading"]["correct"].mean() if len(df[df["category"] == "reading"]) > 0 else 0

            values = [accuracy, consistency, math_acc, logic_acc, reading_acc]
            values += values[:1]

            ax.plot(
                angles,
                values,
                "o-",
                linewidth=2,
                label=self.get_label(technique),
                color=self.get_color(technique),
            )
            ax.fill(angles, values, alpha=0.1, color=self.get_color(technique))

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)
        ax.set_ylim(0, 1)
        plt.legend(loc="upper right", bbox_to_anchor=(1.3, 1.0))
        plt.title("Multi-Dimensional Technique Comparison", y=1.08)
        self.save_figure(filename)

    def plot_score_histograms(
        self,
        results: dict[str, pd.DataFrame],
        filename: str = "score_histograms.png",
    ) -> None:
        """
        Create histograms showing score distribution for each technique.

        Parameters
        ----------
        results : dict
            Dictionary mapping technique names to result DataFrames.
        filename : str
            Output filename.
        """
        techniques = list(results.keys())
        n_techniques = len(techniques)

        # Calculate grid size
        cols = 3
        rows = (n_techniques + cols - 1) // cols

        fig, axes = plt.subplots(rows, cols, figsize=(15, 5 * rows))
        axes = axes.flatten() if n_techniques > 1 else [axes]

        for i, technique in enumerate(techniques):
            df = results[technique]
            scores = df["correct"].values
            color = self.get_color(technique)

            axes[i].hist(
                scores,
                bins=[0, 0.5, 1],
                color=color,
                edgecolor="black",
                alpha=0.7,
                rwidth=0.8,
            )
            axes[i].set_title(f"{self.get_label(technique)} Score Distribution")
            axes[i].set_xlabel("Correct (0 or 1)")
            axes[i].set_ylabel("Count")
            axes[i].set_xticks([0.25, 0.75])
            axes[i].set_xticklabels(["Incorrect", "Correct"])

        # Hide empty subplots
        for j in range(i + 1, len(axes)):
            axes[j].axis("off")

        plt.tight_layout()
        self.save_figure(filename)
