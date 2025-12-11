"""
Prompt Engineering Research Package.

This package provides tools for testing and comparing different prompt
engineering techniques against LLMs using Ollama.
"""

__version__ = "0.1.0"

from .config import Config
from .ollama_client import OllamaClient
from .answer_evaluator import AnswerEvaluator
from .metrics import MetricsCalculator
from .experiment_runner import ExperimentRunner

__all__ = [
    "Config",
    "OllamaClient",
    "AnswerEvaluator",
    "MetricsCalculator",
    "ExperimentRunner",
]
