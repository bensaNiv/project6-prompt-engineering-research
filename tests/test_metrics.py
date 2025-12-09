"""Tests for the metrics calculation module."""

import pandas as pd
import pytest

from src.metrics import MetricsCalculator, TechniqueMetrics


class TestMetricsCalculator:
    """Tests for MetricsCalculator class."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.calculator = MetricsCalculator()

    def test_calculate_metrics_all_correct(self) -> None:
        """Test metrics calculation with all correct scores."""
        scores = [1, 1, 1, 1, 1]
        metrics = self.calculator.calculate_metrics(scores)

        assert metrics.accuracy == 1.0
        assert metrics.mean == 1.0
        assert metrics.variance == 0.0
        assert metrics.std_dev == 0.0
        assert metrics.count == 5

    def test_calculate_metrics_all_wrong(self) -> None:
        """Test metrics calculation with all wrong scores."""
        scores = [0, 0, 0, 0, 0]
        metrics = self.calculator.calculate_metrics(scores)

        assert metrics.accuracy == 0.0
        assert metrics.mean == 0.0
        assert metrics.variance == 0.0
        assert metrics.count == 5

    def test_calculate_metrics_mixed(self) -> None:
        """Test metrics calculation with mixed scores."""
        scores = [1, 1, 0, 0, 1]
        metrics = self.calculator.calculate_metrics(scores)

        assert metrics.accuracy == 0.6
        assert metrics.mean == 0.6
        assert metrics.variance > 0
        assert metrics.count == 5

    def test_calculate_metrics_empty(self) -> None:
        """Test metrics calculation with empty list."""
        scores = []
        metrics = self.calculator.calculate_metrics(scores)

        assert metrics.accuracy == 0.0
        assert metrics.mean == 0.0
        assert metrics.variance == 0.0
        assert metrics.count == 0

    def test_calculate_improvement_positive(self) -> None:
        """Test improvement calculation with positive improvement."""
        improvement = self.calculator.calculate_improvement(0.5, 0.7)
        assert improvement == pytest.approx(40.0)

    def test_calculate_improvement_negative(self) -> None:
        """Test improvement calculation with negative improvement."""
        improvement = self.calculator.calculate_improvement(0.7, 0.5)
        assert improvement == pytest.approx(-28.57, rel=0.01)

    def test_calculate_improvement_zero_baseline(self) -> None:
        """Test improvement calculation with zero baseline."""
        improvement = self.calculator.calculate_improvement(0.0, 0.5)
        assert improvement == 0.0

    def test_calculate_improvement_no_change(self) -> None:
        """Test improvement calculation with no change."""
        improvement = self.calculator.calculate_improvement(0.5, 0.5)
        assert improvement == 0.0

    def test_aggregate_by_category(self) -> None:
        """Test aggregation by category."""
        df = pd.DataFrame({
            "category": ["math", "math", "sentiment", "sentiment"],
            "correct": [1, 0, 1, 1],
        })

        results = self.calculator.aggregate_by_category(df)

        assert "math" in results
        assert "sentiment" in results
        assert results["math"].accuracy == 0.5
        assert results["sentiment"].accuracy == 1.0

    def test_aggregate_by_difficulty(self) -> None:
        """Test aggregation by difficulty level."""
        df = pd.DataFrame({
            "difficulty": [1, 1, 2, 2, 3],
            "correct": [1, 1, 1, 0, 0],
        })

        results = self.calculator.aggregate_by_difficulty(df)

        assert 1 in results
        assert 2 in results
        assert 3 in results
        assert results[1].accuracy == 1.0
        assert results[2].accuracy == 0.5
        assert results[3].accuracy == 0.0


class TestTechniqueMetrics:
    """Tests for TechniqueMetrics dataclass."""

    def test_technique_metrics_creation(self) -> None:
        """Test creating TechniqueMetrics instance."""
        metrics = TechniqueMetrics(
            accuracy=0.75,
            mean=0.75,
            variance=0.1875,
            std_dev=0.433,
            count=100,
        )

        assert metrics.accuracy == 0.75
        assert metrics.mean == 0.75
        assert metrics.variance == 0.1875
        assert metrics.std_dev == 0.433
        assert metrics.count == 100
