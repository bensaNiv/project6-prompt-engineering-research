"""Heatmap generators for category and difficulty analysis."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from .base import ChartBase


class HeatmapGenerator(ChartBase):
    """Generator for heatmap visualizations."""

    def plot_accuracy_heatmap(
        self,
        results: dict[str, pd.DataFrame],
        filename: str = "accuracy_heatmap.png",
    ) -> None:
        """
        Create heatmap of accuracy by technique and category.

        Parameters
        ----------
        results : dict
            Dictionary mapping technique names to result DataFrames.
        filename : str
            Output filename.
        """
        first_key = list(results.keys())[0]
        categories = sorted(results[first_key]["category"].unique())
        techniques = list(results.keys())

        data = np.zeros((len(techniques), len(categories)))

        for i, technique in enumerate(techniques):
            df = results[technique]
            for j, category in enumerate(categories):
                cat_df = df[df["category"] == category]
                data[i, j] = cat_df["correct"].mean()

        technique_labels = [self.get_label(t) for t in techniques]

        plt.figure(figsize=(12, 6))
        sns.heatmap(
            data,
            annot=True,
            fmt=".2f",
            cmap="RdYlGn",
            xticklabels=categories,
            yticklabels=technique_labels,
            vmin=0,
            vmax=1,
            center=0.5,
        )
        plt.title("Accuracy Heatmap: Technique x Category")
        self.save_figure(filename)

    def plot_difficulty_heatmap(
        self,
        results: dict[str, pd.DataFrame],
        filename: str = "difficulty_heatmap.png",
    ) -> None:
        """
        Create heatmap of accuracy by technique and difficulty level.

        Parameters
        ----------
        results : dict
            Dictionary mapping technique names to result DataFrames.
        filename : str
            Output filename.
        """
        difficulties = [1, 2, 3]
        difficulty_labels = ["Easy (1)", "Medium (2)", "Hard (3)"]
        techniques = list(results.keys())

        data = np.zeros((len(techniques), len(difficulties)))

        for i, technique in enumerate(techniques):
            df = results[technique]
            for j, diff in enumerate(difficulties):
                diff_df = df[df["difficulty"] == diff]
                if len(diff_df) > 0:
                    data[i, j] = diff_df["correct"].mean()
                else:
                    data[i, j] = np.nan

        technique_labels = [self.get_label(t) for t in techniques]

        plt.figure(figsize=(8, 6))
        sns.heatmap(
            data,
            annot=True,
            fmt=".2f",
            cmap="RdYlGn",
            xticklabels=difficulty_labels,
            yticklabels=technique_labels,
            vmin=0,
            vmax=1,
            center=0.5,
        )
        plt.title("Accuracy Heatmap: Technique x Difficulty")
        self.save_figure(filename)
