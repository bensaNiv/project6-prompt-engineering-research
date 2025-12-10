"""Improved prompt generator with structured formatting and constraints."""

from .base import BasePromptGenerator


class ImprovedPromptGenerator(BasePromptGenerator):
    """
    Improved prompt generator with category-specific format hints.

    Adds clear output format constraints and structure to prompts.
    """

    FORMAT_HINTS = {
        "sentiment": "Respond with exactly one word: positive, negative, or neutral.",
        "math": "Respond with only the numerical answer.",
        "logic": "Respond with only: yes or no.",
        "classification": "Respond with only the category name.",
        "reading": "Provide a brief, direct answer.",
        "commonsense": "Provide a brief, direct answer.",
        "code": "Respond with only what the code prints.",
    }

    def generate(self, test_case: dict) -> str:
        """
        Generate an improved prompt with format constraints.

        Parameters
        ----------
        test_case : dict
            Test case dictionary.

        Returns
        -------
        str
            Structured prompt with format hints.
        """
        question = test_case["question"]
        category = test_case["category"]

        hint = self.FORMAT_HINTS.get(
            category, "Provide a clear and concise answer."
        )

        return f"""Question: {question}

{hint}

Answer concisely with just the answer, no explanation."""
