"""Line chart generators for trend analysis."""

import matplotlib.pyplot as plt
import pandas as pd

from .base import ChartBase


class LineChartGenerator(ChartBase):
    """Generator for line chart visualizations."""

    def plot_difficulty_trend(
        self,
        results: dict[str, pd.DataFrame],
        filename: str = "difficulty_trend.png",
    ) -> None:
        """
        Create line chart showing accuracy by difficulty level.

        Parameters
        ----------
        results : dict
            Dictionary mapping technique names to result DataFrames.
        filename : str
            Output filename.
        """
        difficulties = [1, 2, 3]
        difficulty_labels = ["Easy", "Medium", "Hard"]

        plt.figure(figsize=(10, 6))

        for technique, df in results.items():
            accuracies = []
            for diff in difficulties:
                diff_df = df[df["difficulty"] == diff]
                accuracies.append(diff_df["correct"].mean())

            plt.plot(
                difficulties,
                accuracies,
                "o-",
                label=self.get_label(technique),
                color=self.get_color(technique),
                linewidth=2,
                markersize=8,
            )

        plt.xlabel("Difficulty Level")
        plt.ylabel("Accuracy")
        plt.title("Accuracy by Difficulty Level")
        plt.xticks(difficulties, difficulty_labels)
        plt.legend()
        plt.grid(True, alpha=0.3)
        self.save_figure(filename)
