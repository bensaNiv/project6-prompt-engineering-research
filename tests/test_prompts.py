"""Tests for baseline and improved prompt generators."""

import pytest

from src.prompts.base import BaselinePromptGenerator
from src.prompts.improved import ImprovedPromptGenerator


class TestBaselinePromptGenerator:
    """Tests for BaselinePromptGenerator."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.generator = BaselinePromptGenerator()
        self.test_case = {
            "question": "What is 2 + 2?",
            "category": "math",
            "difficulty": 1,
            "expected_answer": "4",
            "answer_type": "numeric",
        }

    def test_baseline_prompt_format(self) -> None:
        """Test baseline prompt has correct format."""
        prompt = self.generator.generate(self.test_case)

        assert "Answer the following question:" in prompt
        assert "What is 2 + 2?" in prompt

    def test_baseline_prompt_minimal(self) -> None:
        """Test baseline prompt is minimal without extra content."""
        prompt = self.generator.generate(self.test_case)

        assert "step by step" not in prompt.lower()
        assert "example" not in prompt.lower()


class TestImprovedPromptGenerator:
    """Tests for ImprovedPromptGenerator."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.generator = ImprovedPromptGenerator()

    def test_improved_prompt_has_format_hint(self) -> None:
        """Test improved prompt includes format hint."""
        test_case = {
            "question": "Is this positive or negative?",
            "category": "sentiment",
            "difficulty": 1,
            "expected_answer": "positive",
            "answer_type": "exact",
        }
        prompt = self.generator.generate(test_case)
        assert "positive, negative, or neutral" in prompt.lower()

    def test_improved_prompt_math_hint(self) -> None:
        """Test improved prompt has math-specific hint."""
        test_case = {
            "question": "What is 5 + 3?",
            "category": "math",
            "difficulty": 1,
            "expected_answer": "8",
            "answer_type": "numeric",
        }
        prompt = self.generator.generate(test_case)
        assert "numerical answer" in prompt.lower()

    def test_improved_prompt_default_hint(self) -> None:
        """Test improved prompt uses default hint for unknown category."""
        test_case = {
            "question": "Some question",
            "category": "unknown_category",
            "difficulty": 1,
            "expected_answer": "answer",
            "answer_type": "exact",
        }
        prompt = self.generator.generate(test_case)
        assert "clear and concise" in prompt.lower()
