"""Answer evaluation module for comparing model responses to expected answers."""

from enum import Enum

from .answer_utils import (
    WORD_TO_NUM, normalize_text, get_words, extract_numbers,
    apply_synonyms, cosine_similarity,
)


class AnswerType(Enum):
    """Types of answer matching strategies."""
    EXACT = "exact"
    NUMERIC = "numeric"
    CONTAINS = "contains"
    SEMANTIC = "semantic"


class AnswerEvaluator:
    """Evaluator for comparing model responses to expected answers."""

    def __init__(self, semantic_threshold: float = 0.8) -> None:
        """Initialize evaluator with semantic similarity threshold (0-1)."""
        self.semantic_threshold = semantic_threshold
        self._embedder = None

    def evaluate(
        self, response: str, expected: str, answer_type: str
    ) -> tuple[bool, float]:
        """
        Evaluate if response matches expected answer.

        Returns tuple of (is_correct, confidence_score).
        """
        response = response.strip().lower()
        expected = expected.strip().lower()

        evaluators = {
            AnswerType.EXACT.value: self._evaluate_exact,
            AnswerType.NUMERIC.value: self._evaluate_numeric,
            AnswerType.CONTAINS.value: self._evaluate_contains,
            AnswerType.SEMANTIC.value: self._evaluate_semantic,
        }
        evaluator = evaluators.get(answer_type, self._evaluate_exact)
        return evaluator(response, expected)

    def _evaluate_exact(self, response: str, expected: str) -> tuple[bool, float]:
        """Exact string match with flexible normalization."""
        if response == expected:
            return True, 1.0

        response_norm = normalize_text(response)
        expected_norm = normalize_text(expected)

        if response_norm == expected_norm:
            return True, 1.0
        if response_norm.startswith(expected_norm):
            return True, 0.95
        if expected_norm in response_norm:
            return True, 0.9

        expected_words = get_words(expected)
        response_words = get_words(response)
        if len(expected_words) <= 3 and expected_words.issubset(response_words):
            return True, 0.85

        return False, 0.0

    def _evaluate_numeric(self, response: str, expected: str) -> tuple[bool, float]:
        """Numeric comparison with extraction from text, including word numbers."""
        try:
            expected_num = float(expected)
        except ValueError:
            if expected.lower() in WORD_TO_NUM:
                expected_num = WORD_TO_NUM[expected.lower()]
            else:
                return False, 0.0

        numbers = extract_numbers(response)
        if not numbers:
            return False, 0.0

        for num_str in numbers:
            try:
                response_num = float(num_str)
                if abs(response_num - expected_num) < 0.01:
                    return True, 1.0
                if abs(response_num - expected_num * 100) < 0.01:
                    return True, 0.9
                if abs(response_num / 100 - expected_num) < 0.01:
                    return True, 0.9
            except ValueError:
                continue
        return False, 0.0

    def _evaluate_contains(self, response: str, expected: str) -> tuple[bool, float]:
        """Check if response contains the expected answer (flexible matching)."""
        if expected in response:
            return True, 1.0

        response_norm = normalize_text(response)
        expected_norm = normalize_text(expected)

        if expected_norm in response_norm:
            return True, 1.0

        expected_words = get_words(expected)
        response_words = get_words(response)

        if expected_words and expected_words.issubset(response_words):
            return True, 0.9

        if expected_words:
            matching = expected_words.intersection(response_words)
            match_ratio = len(matching) / len(expected_words)
            if match_ratio >= 0.8:
                return True, match_ratio

        if expected_norm in apply_synonyms(response_norm):
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
        similarity = cosine_similarity(embeddings[0], embeddings[1])
        return similarity >= self.semantic_threshold, float(similarity)
