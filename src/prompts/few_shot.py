"""Few-shot prompt generator with examples."""

import json
from pathlib import Path

from .base import BasePromptGenerator


class FewShotPromptGenerator(BasePromptGenerator):
    """
    Few-shot prompt generator that includes examples before the question.

    Loads examples from a JSON file and includes 3 relevant examples
    based on the test case category.
    """

    DEFAULT_EXAMPLES = {
        "sentiment": [
            {"question": "The service was terrible and the food was cold.", "answer": "negative"},
            {"question": "I had an amazing time at the concert!", "answer": "positive"},
            {"question": "The weather today is partly cloudy.", "answer": "neutral"},
        ],
        "math": [
            {"question": "If a book costs $12 and you buy 3, how much do you spend?", "answer": "36"},
            {"question": "What is 15 plus 27?", "answer": "42"},
            {"question": "If you have 20 cookies and eat 8, how many remain?", "answer": "12"},
        ],
        "logic": [
            {"question": "All cats are animals. Whiskers is a cat. Is Whiskers an animal?", "answer": "yes"},
            {"question": "If it rains, the ground is wet. It rained. Is the ground wet?", "answer": "yes"},
            {"question": "All birds can fly. Penguins are birds. Can penguins fly?", "answer": "no"},
        ],
        "classification": [
            {"question": "The stock market closed higher today with tech leading gains.", "answer": "finance"},
            {"question": "The team won the championship after a thrilling overtime.", "answer": "sports"},
            {"question": "Scientists discovered a new species in the Amazon.", "answer": "science"},
        ],
        "reading": [
            {"question": "Text: John is 25 years old. Question: How old is John?", "answer": "25"},
            {"question": "Text: The capital of France is Paris. Question: What is France's capital?", "answer": "Paris"},
            {"question": "Text: Water boils at 100 degrees Celsius. Question: At what temperature does water boil?", "answer": "100 degrees Celsius"},
        ],
        "commonsense": [
            {"question": "What do you use to cut paper?", "answer": "scissors"},
            {"question": "Where do fish live?", "answer": "water"},
            {"question": "What season comes after summer?", "answer": "fall"},
        ],
        "code": [
            {"question": "What does print(2 + 3) output?", "answer": "5"},
            {"question": "What does print('hello'.upper()) output?", "answer": "HELLO"},
            {"question": "What does print(len([1, 2, 3])) output?", "answer": "3"},
        ],
    }

    def __init__(self, examples_path: str | None = None) -> None:
        """
        Initialize the few-shot generator.

        Parameters
        ----------
        examples_path : str, optional
            Path to JSON file with examples. Uses defaults if not provided.
        """
        self.examples = self.DEFAULT_EXAMPLES.copy()

        if examples_path:
            path = Path(examples_path)
            if path.exists():
                with open(path) as f:
                    self.examples.update(json.load(f))

    def generate(self, test_case: dict) -> str:
        """
        Generate a few-shot prompt with examples.

        Parameters
        ----------
        test_case : dict
            Test case dictionary.

        Returns
        -------
        str
            Prompt with examples followed by the question.
        """
        question = test_case["question"]
        category = test_case["category"]

        examples = self.examples.get(category, [])[:3]

        example_text = "\n\n".join([
            f"Example {i + 1}:\nQuestion: {ex['question']}\nAnswer: {ex['answer']}"
            for i, ex in enumerate(examples)
        ])

        return f"""Here are some examples:

{example_text}

Now answer this question:
Question: {question}
Answer:"""
