"""Metrics calculation module for statistical analysis of experiment results."""

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class TechniqueMetrics:
    """Metrics for a single prompt technique."""

    accuracy: float
    mean: float
    variance: float
    std_dev: float
    count: int


class MetricsCalculator:
    """Calculator for experiment metrics and statistics."""

    def calculate_metrics(self, scores: list[int | float]) -> TechniqueMetrics:
        """Calculate metrics from a list of correctness scores."""
        if not scores:
            return TechniqueMetrics(
                accuracy=0.0, mean=0.0, variance=0.0, std_dev=0.0, count=0
            )

        scores_array = np.array(scores)
        count = len(scores_array)
        mean = float(np.mean(scores_array))
        variance = float(np.var(scores_array))
        std_dev = float(np.std(scores_array))

        return TechniqueMetrics(
            accuracy=mean,
            mean=mean,
            variance=variance,
            std_dev=std_dev,
            count=count,
        )

    def calculate_improvement(
        self, baseline_accuracy: float, technique_accuracy: float
    ) -> float:
        """Calculate improvement percentage over baseline."""
        if baseline_accuracy == 0:
            return 0.0
        return ((technique_accuracy - baseline_accuracy) / baseline_accuracy) * 100

    def aggregate_by_category(
        self, df: pd.DataFrame, score_column: str = "correct"
    ) -> dict[str, TechniqueMetrics]:
        """Aggregate metrics by category."""
        results = {}
        for category in df["category"].unique():
            category_df = df[df["category"] == category]
            scores = category_df[score_column].tolist()
            results[category] = self.calculate_metrics(scores)
        return results

    def aggregate_by_difficulty(
        self, df: pd.DataFrame, score_column: str = "correct"
    ) -> dict[int, TechniqueMetrics]:
        """Aggregate metrics by difficulty level."""
        results = {}
        for difficulty in df["difficulty"].unique():
            difficulty_df = df[df["difficulty"] == difficulty]
            scores = difficulty_df[score_column].tolist()
            results[int(difficulty)] = self.calculate_metrics(scores)
        return results

    def generate_comparison_stats(self, results: dict[str, pd.DataFrame]) -> dict:
        """Generate comprehensive comparison statistics across techniques."""
        stats = {
            "by_technique": {},
            "by_category": {},
            "by_difficulty": {},
        }

        baseline_accuracy = 0.0

        for technique, df in results.items():
            scores = df["correct"].tolist()
            metrics = self.calculate_metrics(scores)

            if technique == "baseline":
                baseline_accuracy = metrics.accuracy

            stats["by_technique"][technique] = {
                "accuracy": metrics.accuracy,
                "mean": metrics.mean,
                "variance": metrics.variance,
                "std_dev": metrics.std_dev,
                "count": metrics.count,
            }

        for technique in stats["by_technique"]:
            if technique != "baseline":
                improvement = self.calculate_improvement(
                    baseline_accuracy,
                    stats["by_technique"][technique]["accuracy"],
                )
                stats["by_technique"][technique]["improvement_pct"] = improvement

        return stats
