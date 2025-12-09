"""Tests for the answer evaluator module."""

import pytest

from src.answer_evaluator import AnswerEvaluator, AnswerType


class TestAnswerEvaluator:
    """Tests for AnswerEvaluator class."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.evaluator = AnswerEvaluator()

    def test_exact_match_correct(self) -> None:
        """Test exact match with matching strings."""
        is_correct, confidence = self.evaluator.evaluate(
            "positive", "positive", AnswerType.EXACT.value
        )
        assert is_correct is True
        assert confidence == 1.0

    def test_exact_match_case_insensitive(self) -> None:
        """Test exact match is case insensitive."""
        is_correct, confidence = self.evaluator.evaluate(
            "POSITIVE", "positive", AnswerType.EXACT.value
        )
        assert is_correct is True
        assert confidence == 1.0

    def test_exact_match_incorrect(self) -> None:
        """Test exact match with non-matching strings."""
        is_correct, confidence = self.evaluator.evaluate(
            "negative", "positive", AnswerType.EXACT.value
        )
        assert is_correct is False
        assert confidence == 0.0

    def test_exact_match_with_punctuation(self) -> None:
        """Test exact match ignores punctuation differences."""
        is_correct, confidence = self.evaluator.evaluate(
            "positive.", "positive", AnswerType.EXACT.value
        )
        assert is_correct is True

    def test_exact_match_contains_expected(self) -> None:
        """Test exact match when response contains expected."""
        is_correct, confidence = self.evaluator.evaluate(
            "The answer is positive.", "positive", AnswerType.EXACT.value
        )
        assert is_correct is True
        assert confidence == 0.9

    def test_numeric_match_correct(self) -> None:
        """Test numeric match with matching numbers."""
        is_correct, confidence = self.evaluator.evaluate(
            "42", "42", AnswerType.NUMERIC.value
        )
        assert is_correct is True
        assert confidence == 1.0

    def test_numeric_match_with_text(self) -> None:
        """Test numeric match extracts number from text."""
        is_correct, confidence = self.evaluator.evaluate(
            "The answer is 42.", "42", AnswerType.NUMERIC.value
        )
        assert is_correct is True
        assert confidence == 1.0

    def test_numeric_match_incorrect(self) -> None:
        """Test numeric match with wrong number."""
        is_correct, confidence = self.evaluator.evaluate(
            "43", "42", AnswerType.NUMERIC.value
        )
        assert is_correct is False
        assert confidence == 0.0

    def test_numeric_match_no_number(self) -> None:
        """Test numeric match when response has no numbers."""
        is_correct, confidence = self.evaluator.evaluate(
            "no numbers here", "42", AnswerType.NUMERIC.value
        )
        assert is_correct is False
        assert confidence == 0.0

    def test_numeric_match_float(self) -> None:
        """Test numeric match with floating point numbers."""
        is_correct, confidence = self.evaluator.evaluate(
            "3.14", "3.14", AnswerType.NUMERIC.value
        )
        assert is_correct is True

    def test_contains_match_correct(self) -> None:
        """Test contains match when response contains expected."""
        is_correct, confidence = self.evaluator.evaluate(
            "I think the answer is Paris, the capital.",
            "paris",
            AnswerType.CONTAINS.value,
        )
        assert is_correct is True
        assert confidence == 1.0

    def test_contains_match_incorrect(self) -> None:
        """Test contains match when response doesn't contain expected."""
        is_correct, confidence = self.evaluator.evaluate(
            "London is a great city", "paris", AnswerType.CONTAINS.value
        )
        assert is_correct is False
        assert confidence == 0.0

    def test_default_to_exact_for_unknown_type(self) -> None:
        """Test that unknown answer types default to exact matching."""
        is_correct, confidence = self.evaluator.evaluate(
            "test", "test", "unknown_type"
        )
        assert is_correct is True
        assert confidence == 1.0


class TestAnswerTypes:
    """Tests for AnswerType enum."""

    def test_answer_type_values(self) -> None:
        """Test AnswerType enum values."""
        assert AnswerType.EXACT.value == "exact"
        assert AnswerType.NUMERIC.value == "numeric"
        assert AnswerType.CONTAINS.value == "contains"
        assert AnswerType.SEMANTIC.value == "semantic"
