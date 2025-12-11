"""Experiment runner module for orchestrating prompt technique experiments."""

import json
import logging
from pathlib import Path
from typing import Callable, Protocol

import pandas as pd

from .answer_evaluator import AnswerEvaluator
from .config import Config
from .metrics import MetricsCalculator

# Configure module logger
logger = logging.getLogger(__name__)


class LLMClient(Protocol):
    """Protocol for LLM clients (Gemini, Ollama, etc.)."""



class ExperimentRunner:
    """Runner for executing prompt engineering experiments."""

    def __init__(
        self,
        config: Config,
        client: LLMClient | None = None,
        data_path: str = "data/test_cases.csv",
        results_dir: str = "results",
    ) -> None:
        """Initialize the experiment runner."""
        logger.info("Initializing ExperimentRunner")
        logger.debug(f"Config: model={config.model_name}, runs_per_case={config.runs_per_case}")

        self.config = config
        self.data_path = Path(data_path)
        self.results_dir = Path(results_dir)

        # Use provided client or default to OllamaClient
        if client is not None:
            self.client = client
            logger.debug("Using provided LLM client")
        else:
            from .ollama_client import OllamaClient
            self.client = OllamaClient(config, host=config.ollama_host)
            logger.debug(f"Created OllamaClient with host={config.ollama_host}")

        self.evaluator = AnswerEvaluator()
        self.metrics_calc = MetricsCalculator()
        self._setup_directories()
        logger.info("ExperimentRunner initialization complete")

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
        logger.info(f"Starting experiment: technique={technique_name}")

        if test_cases is None:
            test_cases = self.load_test_cases()
            logger.debug(f"Loaded {len(test_cases)} test cases from {self.data_path}")

        total_cases = len(test_cases)
        total_calls = total_cases * self.config.runs_per_case
        call_count = 0

        logger.info(f"Experiment plan: {total_cases} cases x {self.config.runs_per_case} runs = {total_calls} API calls")

        results = []
        for idx, (_, case) in enumerate(test_cases.iterrows()):
            case_dict = case.to_dict()
            prompt = prompt_generator(case_dict)
            logger.debug(f"Processing case {idx+1}/{total_cases}: id={case_dict.get('id')}, category={case_dict.get('category')}")

            for run in range(1, self.config.runs_per_case + 1):
                call_count += 1
                result = self._run_single_case(case_dict, prompt, run)
                results.append(result)

                logger.debug(f"Call {call_count}: case_id={case_dict.get('id')}, run={run}, correct={result['correct']}")

                # Progress update every 10 calls
                if call_count % 10 == 0 or call_count == total_calls:
                    correct_count = sum(1 for r in results if r["correct"])
                    accuracy = correct_count / len(results) * 100
                    logger.info(f"Progress: [{call_count}/{total_calls}] accuracy={accuracy:.1f}%")
                    print(f"  [{call_count}/{total_calls}] Case {idx+1}/{total_cases}, "
                          f"Running accuracy: {accuracy:.1f}%")

        results_df = pd.DataFrame(results)
        output_path = self.results_dir / "raw" / f"{technique_name}_results.csv"
        results_df.to_csv(output_path, index=False)

        final_accuracy = results_df["correct"].mean() * 100
        logger.info(f"Experiment complete: technique={technique_name}, accuracy={final_accuracy:.1f}%, saved to {output_path}")

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
