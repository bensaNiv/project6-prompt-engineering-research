"""Tests for few-shot, chain-of-thought, and role-based prompt generators."""

import pytest

from src.prompts.few_shot import FewShotPromptGenerator
from src.prompts.chain_of_thought import ChainOfThoughtPromptGenerator
from src.prompts.role_based import RoleBasedPromptGenerator


class TestFewShotPromptGenerator:
    """Tests for FewShotPromptGenerator."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.generator = FewShotPromptGenerator()

    def test_few_shot_has_examples(self) -> None:
        """Test few-shot prompt includes examples."""
        test_case = {
            "question": "What is the sentiment?",
            "category": "sentiment",
            "difficulty": 1,
            "expected_answer": "positive",
            "answer_type": "exact",
        }
        prompt = self.generator.generate(test_case)
        assert "Example 1:" in prompt
        assert "Example 2:" in prompt
        assert "Example 3:" in prompt

    def test_few_shot_has_answer_marker(self) -> None:
        """Test few-shot prompt ends with answer marker."""
        test_case = {
            "question": "Test question",
            "category": "math",
            "difficulty": 1,
            "expected_answer": "42",
            "answer_type": "numeric",
        }
        prompt = self.generator.generate(test_case)
        assert "Answer:" in prompt
        assert prompt.strip().endswith("Answer:")


class TestChainOfThoughtPromptGenerator:
    """Tests for ChainOfThoughtPromptGenerator."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.generator = ChainOfThoughtPromptGenerator()

    def test_cot_has_step_instructions(self) -> None:
        """Test CoT prompt has step-by-step instructions."""
        test_case = {
            "question": "What is 5 * 4?",
            "category": "math",
            "difficulty": 1,
            "expected_answer": "20",
            "answer_type": "numeric",
        }
        prompt = self.generator.generate(test_case)
        assert "step by step" in prompt.lower()
        assert "1." in prompt
        assert "2." in prompt

    def test_cot_has_reasoning_format(self) -> None:
        """Test CoT prompt asks for reasoning format."""
        test_case = {
            "question": "Is this logical?",
            "category": "logical",
            "difficulty": 1,
            "expected_answer": "true",
            "answer_type": "exact",
        }
        prompt = self.generator.generate(test_case)
        assert "Reasoning:" in prompt
        assert "Final Answer:" in prompt


class TestRoleBasedPromptGenerator:
    """Tests for RoleBasedPromptGenerator."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.generator = RoleBasedPromptGenerator()

    def test_role_based_has_expert_role(self) -> None:
        """Test role-based prompt assigns expert role."""
        test_case = {
            "question": "What is 10 / 2?",
            "category": "math",
            "difficulty": 1,
            "expected_answer": "5",
            "answer_type": "numeric",
        }
        prompt = self.generator.generate(test_case)
        assert "professor" in prompt.lower() or "expert" in prompt.lower()

    def test_role_based_sentiment_role(self) -> None:
        """Test role-based uses sentiment analyst for sentiment category."""
        test_case = {
            "question": "Is this positive?",
            "category": "sentiment",
            "difficulty": 1,
            "expected_answer": "positive",
            "answer_type": "exact",
        }
        prompt = self.generator.generate(test_case)
        assert "sentiment" in prompt.lower()

    def test_role_based_default_role(self) -> None:
        """Test role-based uses default role for unknown category."""
        test_case = {
            "question": "Some question",
            "category": "unknown_category",
            "difficulty": 1,
            "expected_answer": "answer",
            "answer_type": "exact",
        }
        prompt = self.generator.generate(test_case)
        assert "helpful assistant" in prompt.lower()

    def test_role_based_asks_for_expert_answer(self) -> None:
        """Test role-based prompt asks for expert answer."""
        test_case = {
            "question": "Test question",
            "category": "code",
            "difficulty": 1,
            "expected_answer": "42",
            "answer_type": "exact",
        }
        prompt = self.generator.generate(test_case)
        assert "expert answer" in prompt.lower()
