"""
Prompt Engineering Research Package.

This package provides tools for testing and comparing different prompt
engineering techniques against LLMs.
"""

__version__ = "0.1.0"

from .config import Config
from .gemini_client import GeminiClient
from .answer_evaluator import AnswerEvaluator
from .metrics import MetricsCalculator
from .experiment_runner import ExperimentRunner

__all__ = [
    "Config",
    "GeminiClient",
    "AnswerEvaluator",
    "MetricsCalculator",
    "ExperimentRunner",
]
