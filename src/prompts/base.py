"""Base prompt generator implementing the baseline technique."""

from abc import ABC, abstractmethod


class BasePromptGenerator(ABC):
    """
    Abstract base class for prompt generators.

    All prompt technique implementations should inherit from this class
    and implement the generate method.
    """

    @abstractmethod
    def generate(self, test_case: dict) -> str:
        """
        Generate a prompt for the given test case.

        Parameters
        ----------
        test_case : dict
            Dictionary containing test case data with keys:
            - question: The question text
            - category: Problem category
            - difficulty: Difficulty level (1-3)
            - expected_answer: The expected answer
            - answer_type: Type of answer matching

        Returns
        -------
        str
            The generated prompt string.
        """
        pass


class BaselinePromptGenerator(BasePromptGenerator):
    """
    Baseline prompt generator with minimal formatting.

    Uses a simple prompt with no special techniques.
    """

    # Suffix to ensure concise responses
    CONCISE_SUFFIX = "\n\nAnswer concisely with just the answer, no explanation."

    def generate(self, test_case: dict) -> str:
        """
        Generate a minimal baseline prompt.

        Parameters
        ----------
        test_case : dict
            Test case dictionary.

        Returns
        -------
        str
            Simple prompt with just the question.
        """
        question = test_case["question"]
        return f"Answer the following question:\n{question}{self.CONCISE_SUFFIX}"
