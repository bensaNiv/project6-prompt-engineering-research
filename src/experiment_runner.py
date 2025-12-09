"""Experiment runner module for orchestrating prompt technique experiments."""

import json
from pathlib import Path
from typing import Callable

import pandas as pd

from .answer_evaluator import AnswerEvaluator
from .config import Config
from .gemini_client import GeminiClient
from .metrics import MetricsCalculator


class ExperimentRunner:
    """Runner for executing prompt engineering experiments."""

    def __init__(
        self,
        config: Config,
        data_path: str = "data/test_cases.csv",
        results_dir: str = "results",
    ) -> None:
        """Initialize the experiment runner."""
        self.config = config
        self.data_path = Path(data_path)
        self.results_dir = Path(results_dir)
        self.client = GeminiClient(config)
        self.evaluator = AnswerEvaluator()
        self.metrics_calc = MetricsCalculator()
        self._setup_directories()

    def _setup_directories(self) -> None:
        """Create required output directories."""
        self.results_dir.mkdir(parents=True, exist_ok=True)
        (self.results_dir / "raw").mkdir(exist_ok=True)
        (self.results_dir / "stats").mkdir(exist_ok=True)
        (self.results_dir / "figures").mkdir(exist_ok=True)

    def load_test_cases(self) -> pd.DataFrame:
        """Load test cases from CSV file."""
        return pd.read_csv(self.data_path)

    def _run_single_case(
        self, case: dict, prompt: str, run: int
    ) -> dict:
        """Run a single test case and return result dict."""
        response = self.client.query(prompt)

        if response.success:
            is_correct, confidence = self.evaluator.evaluate(
                response.text, str(case["expected_answer"]), case["answer_type"]
            )
        else:
            is_correct, confidence = False, 0.0

        return {
            "id": case["id"],
            "category": case["category"],
            "difficulty": case["difficulty"],
            "run": run,
            "prompt": prompt[:500],
            "response": response.text[:500] if response.success else "",
            "expected": case["expected_answer"],
            "correct": int(is_correct),
            "confidence": confidence,
            "latency_ms": response.latency_ms,
            "success": response.success,
        }

    def run_technique(
        self,
        technique_name: str,
        prompt_generator: Callable[[dict], str],
        test_cases: pd.DataFrame | None = None,
    ) -> pd.DataFrame:
        """Run a single prompt technique across all test cases."""
        if test_cases is None:
            test_cases = self.load_test_cases()

        results = []
        for _, case in test_cases.iterrows():
            case_dict = case.to_dict()
            prompt = prompt_generator(case_dict)

            for run in range(1, self.config.runs_per_case + 1):
                result = self._run_single_case(case_dict, prompt, run)
                results.append(result)

        results_df = pd.DataFrame(results)
        output_path = self.results_dir / "raw" / f"{technique_name}_results.csv"
        results_df.to_csv(output_path, index=False)
        return results_df

    def run_all_techniques(
        self, technique_generators: dict[str, Callable[[dict], str]]
    ) -> dict[str, pd.DataFrame]:
        """Run all prompt techniques and collect results."""
        test_cases = self.load_test_cases()
        all_results = {}

        for technique_name, generator in technique_generators.items():
            results = self.run_technique(technique_name, generator, test_cases)
            all_results[technique_name] = results

        stats = self.metrics_calc.generate_comparison_stats(all_results)
        stats_path = self.results_dir / "stats" / "comparison_stats.json"
        with open(stats_path, "w") as f:
            json.dump(stats, f, indent=2)

        return all_results
