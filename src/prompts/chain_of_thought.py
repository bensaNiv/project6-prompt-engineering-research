"""Chain-of-thought prompt generator for step-by-step reasoning."""

from .base import BasePromptGenerator


class ChainOfThoughtPromptGenerator(BasePromptGenerator):
    """
    Chain-of-thought prompt generator that encourages step-by-step reasoning.

    Adds explicit reasoning instructions to guide the model through
    logical problem-solving steps.
    """

    def generate(self, test_case: dict) -> str:
        """
        Generate a chain-of-thought prompt.

        Parameters
        ----------
        test_case : dict
            Test case dictionary.

        Returns
        -------
        str
            Prompt with step-by-step reasoning instructions.
        """
        question = test_case["question"]

        return f"""Question: {question}

Let's think step by step:
1. First, identify what the question is asking.
2. Break down the problem into smaller parts.
3. Work through each part carefully.
4. Arrive at the final answer.

Think through this step by step, then provide your answer in this format:
Reasoning: [your step-by-step thinking]
Final Answer: [your answer]"""
