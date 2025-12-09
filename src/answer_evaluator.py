"""Answer evaluation module for comparing model responses to expected answers."""

import re
from enum import Enum


class AnswerType(Enum):
    """Types of answer matching strategies."""

    EXACT = "exact"
    NUMERIC = "numeric"
    CONTAINS = "contains"
    SEMANTIC = "semantic"


class AnswerEvaluator:
    """
    Evaluator for comparing model responses to expected answers.

    Supports multiple matching strategies based on answer type.
    """

    def __init__(self, semantic_threshold: float = 0.8) -> None:
        """
        Initialize the answer evaluator.

        Parameters
        ----------
        semantic_threshold : float
            Similarity threshold for semantic matching (0-1).
        """
        self.semantic_threshold = semantic_threshold
        self._embedder = None

    def evaluate(
        self, response: str, expected: str, answer_type: str
    ) -> tuple[bool, float]:
        """
        Evaluate if a response matches the expected answer.

        Parameters
        ----------
        response : str
            The model's response text.
        expected : str
            The expected answer.
        answer_type : str
            Type of matching to use: exact, numeric, contains, semantic.

        Returns
        -------
        tuple[bool, float]
            Tuple of (is_correct, confidence_score).
        """
        response = response.strip().lower()
        expected = expected.strip().lower()

        if answer_type == AnswerType.EXACT.value:
            return self._evaluate_exact(response, expected)
        elif answer_type == AnswerType.NUMERIC.value:
            return self._evaluate_numeric(response, expected)
        elif answer_type == AnswerType.CONTAINS.value:
            return self._evaluate_contains(response, expected)
        elif answer_type == AnswerType.SEMANTIC.value:
            return self._evaluate_semantic(response, expected)
        else:
            return self._evaluate_exact(response, expected)

    def _evaluate_exact(self, response: str, expected: str) -> tuple[bool, float]:
        """Exact string match (case-insensitive)."""
        is_match = response == expected
        if is_match:
            return True, 1.0

        response_clean = re.sub(r"[^\w\s]", "", response)
        expected_clean = re.sub(r"[^\w\s]", "", expected)

        if response_clean == expected_clean:
            return True, 1.0

        if expected in response:
            return True, 0.9

        return False, 0.0

    def _evaluate_numeric(self, response: str, expected: str) -> tuple[bool, float]:
        """Numeric comparison with extraction from text."""
        try:
            expected_num = float(expected)
        except ValueError:
            return False, 0.0

        numbers = re.findall(r"-?\d+\.?\d*", response)

        if not numbers:
            return False, 0.0

        for num_str in numbers:
            try:
                response_num = float(num_str)
                if abs(response_num - expected_num) < 0.001:
                    return True, 1.0
            except ValueError:
                continue

        return False, 0.0

    def _evaluate_contains(self, response: str, expected: str) -> tuple[bool, float]:
        """Check if response contains the expected substring."""
        if expected in response:
            return True, 1.0
        return False, 0.0

    def _evaluate_semantic(self, response: str, expected: str) -> tuple[bool, float]:
        """Semantic similarity using sentence embeddings."""
        if self._embedder is None:
            try:
                from sentence_transformers import SentenceTransformer

                self._embedder = SentenceTransformer("all-MiniLM-L6-v2")
            except ImportError:
                return self._evaluate_contains(response, expected)

        embeddings = self._embedder.encode([response, expected])
        similarity = self._cosine_similarity(embeddings[0], embeddings[1])

        is_match = similarity >= self.semantic_threshold
        return is_match, float(similarity)

    def _cosine_similarity(self, vec1: list, vec2: list) -> float:
        """Calculate cosine similarity between two vectors."""
        import numpy as np

        vec1 = np.array(vec1)
        vec2 = np.array(vec2)

        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)
