"""Answer evaluation module for comparing model responses to expected answers."""

import re
from enum import Enum


class AnswerType(Enum):
    """Types of answer matching strategies."""

    EXACT = "exact"
    NUMERIC = "numeric"
    CONTAINS = "contains"
    SEMANTIC = "semantic"


# Word to number mapping for numeric evaluation
WORD_TO_NUM = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4,
    "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
    "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
    "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17,
    "eighteen": 18, "nineteen": 19, "twenty": 20, "thirty": 30,
    "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70,
    "eighty": 80, "ninety": 90, "hundred": 100,
    "first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5,
}


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

    def _normalize_text(self, text: str) -> str:
        """Normalize text by removing punctuation and extra whitespace."""
        # Remove punctuation except hyphens in words
        text = re.sub(r"[^\w\s-]", " ", text)
        # Collapse multiple spaces
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def _get_words(self, text: str) -> set[str]:
        """Extract normalized words from text."""
        normalized = self._normalize_text(text)
        return set(normalized.split())

    def _evaluate_exact(self, response: str, expected: str) -> tuple[bool, float]:
        """Exact string match with flexible normalization."""
        # Direct match
        if response == expected:
            return True, 1.0

        # Normalize and compare
        response_norm = self._normalize_text(response)
        expected_norm = self._normalize_text(expected)

        if response_norm == expected_norm:
            return True, 1.0

        # Check if response starts with expected (e.g., "yes" in "yes, because...")
        if response_norm.startswith(expected_norm):
            return True, 0.95

        # Check if expected is contained in response
        if expected_norm in response_norm:
            return True, 0.9

        # Check if all expected words are in response (for short expected answers)
        expected_words = self._get_words(expected)
        response_words = self._get_words(response)

        if len(expected_words) <= 3 and expected_words.issubset(response_words):
            return True, 0.85

        return False, 0.0

    def _evaluate_numeric(self, response: str, expected: str) -> tuple[bool, float]:
        """Numeric comparison with extraction from text, including word numbers."""
        # Try to parse expected as number
        try:
            expected_num = float(expected)
        except ValueError:
            # Try word-to-number conversion
            expected_lower = expected.lower()
            if expected_lower in WORD_TO_NUM:
                expected_num = WORD_TO_NUM[expected_lower]
            else:
                return False, 0.0

        # Extract all numbers from response (including negatives, decimals, percentages)
        # Remove currency symbols and % signs for number extraction
        response_clean = re.sub(r"[$%]", "", response)
        numbers = re.findall(r"-?\d+\.?\d*", response_clean)

        # Also check for word numbers in response
        response_lower = response.lower()
        for word, num in WORD_TO_NUM.items():
            if word in response_lower:
                numbers.append(str(num))

        if not numbers:
            return False, 0.0

        # Check each extracted number
        for num_str in numbers:
            try:
                response_num = float(num_str)
                # Allow small floating point tolerance
                if abs(response_num - expected_num) < 0.01:
                    return True, 1.0
                # Also check percentage equivalence (e.g., 44 vs 0.44)
                if abs(response_num - expected_num * 100) < 0.01:
                    return True, 0.9
                if abs(response_num / 100 - expected_num) < 0.01:
                    return True, 0.9
            except ValueError:
                continue

        return False, 0.0

    def _evaluate_contains(self, response: str, expected: str) -> tuple[bool, float]:
        """Check if response contains the expected answer (flexible matching)."""
        # Direct substring match
        if expected in response:
            return True, 1.0

        # Normalize both
        response_norm = self._normalize_text(response)
        expected_norm = self._normalize_text(expected)

        # Normalized substring match
        if expected_norm in response_norm:
            return True, 1.0

        # Check if ALL words from expected appear in response (in any order)
        expected_words = self._get_words(expected)
        response_words = self._get_words(response)

        if expected_words and expected_words.issubset(response_words):
            return True, 0.9

        # Check if MOST words from expected appear (80% threshold)
        if expected_words:
            matching_words = expected_words.intersection(response_words)
            match_ratio = len(matching_words) / len(expected_words)
            if match_ratio >= 0.8:
                return True, match_ratio

        # Handle common synonyms/variations
        synonyms = {
            "dont": "don't",
            "cant": "can't",
            "wont": "won't",
            "isnt": "isn't",
            "arent": "aren't",
            "doesnt": "doesn't",
            "didnt": "didn't",
            "hasnt": "hasn't",
            "havent": "haven't",
            "wouldnt": "wouldn't",
            "couldnt": "couldn't",
            "shouldnt": "shouldn't",
            "autumn": "fall",
            "fall": "autumn",
        }

        # Try with synonym substitution
        response_with_syns = response_norm
        for orig, syn in synonyms.items():
            response_with_syns = response_with_syns.replace(orig, syn)

        if expected_norm in response_with_syns:
            return True, 0.85

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
