#!/usr/bin/env python3
"""
Run the baseline prompt engineering experiment.

This script executes the baseline (minimal) prompt across all 100 test cases,
running each case 2 times to measure consistency. Results are saved to:
- results/raw/baseline_results.csv (raw data)
- results/baseline_stats.json (aggregated statistics)
"""

import json
import os
import sys
from pathlib import Path

import pandas as pd

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.config import Config
from src.experiment_runner import ExperimentRunner
from src.metrics import MetricsCalculator
from src.ollama_client import OllamaClient
from src.prompts.base import BaselinePromptGenerator


def main() -> None:
    """Run the baseline experiment and generate statistics."""
    print("=" * 60)
    print("Stage 2: Baseline Experiment (Ollama)")
    print("=" * 60)

    # Configuration for Ollama
    # Default to localhost (run script on same machine as Ollama)
    OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    MODEL_NAME = os.getenv("MODEL_NAME", "llama3.2:3b")

    print("\n[1/5] Loading configuration...")
    config = Config(
        api_key="not-needed-for-ollama",
        model_name=MODEL_NAME,
        runs_per_case=2,
        max_retries=3,
        retry_delay=2.0,
    )
    print(f"  Model: {config.model_name}")
    print(f"  Runs per case: {config.runs_per_case}")
    print(f"  Ollama host: {OLLAMA_HOST}")

    # Initialize Ollama client
    print("\n[2/5] Initializing Ollama client...")
    client = OllamaClient(config, host=OLLAMA_HOST)

    # Check connection and list models
    models = client.list_models()
    if models:
        print(f"  Connected! Available models: {', '.join(models[:5])}")
        if MODEL_NAME not in models and not any(MODEL_NAME in m for m in models):
            print(f"  WARNING: {MODEL_NAME} not found. Available: {models}")
    else:
        print(f"  WARNING: Could not list models. Ensure Ollama is running at {OLLAMA_HOST}")

    # Initialize runner with Ollama client
    runner = ExperimentRunner(config, client=client)
    prompt_generator = BaselinePromptGenerator()
    metrics_calc = MetricsCalculator()

    # Load test cases to show count
    test_cases = runner.load_test_cases()
    total_cases = len(test_cases)
    total_calls = total_cases * config.runs_per_case
    print(f"  Test cases: {total_cases}")
    print(f"  Total API calls: {total_calls}")

    # Estimate time for Ollama (roughly 3-10 seconds per call depending on model)
    est_minutes = (total_calls * 5) / 60
    print(f"  Estimated time: ~{est_minutes:.0f}-{est_minutes*2:.0f} minutes")

    # Run baseline experiment
    print(f"\n[3/5] Running baseline experiment ({total_calls} API calls)...")
    print("  Progress will be shown below...")

    results_df = runner.run_technique(
        technique_name="baseline",
        prompt_generator=prompt_generator.generate,
    )

    print(f"\n  Completed: {len(results_df)} responses collected")

    # Check for API errors
    api_errors = results_df[~results_df["success"]]
    if len(api_errors) > 0:
        print(f"  WARNING: {len(api_errors)} API errors occurred")

    # Calculate statistics
    print("\n[4/5] Calculating statistics...")
    overall_metrics = metrics_calc.calculate_metrics(results_df["correct"].tolist())
    by_category = metrics_calc.aggregate_by_category(results_df)
    by_difficulty = metrics_calc.aggregate_by_difficulty(results_df)

    # Build stats dictionary
    stats = {
        "overall": {
            "accuracy": overall_metrics.accuracy,
            "mean": overall_metrics.mean,
            "variance": overall_metrics.variance,
            "std_dev": overall_metrics.std_dev,
            "count": overall_metrics.count,
        },
        "by_category": {
            cat: {
                "accuracy": m.accuracy,
                "mean": m.mean,
                "variance": m.variance,
                "std_dev": m.std_dev,
                "count": m.count,
            }
            for cat, m in by_category.items()
        },
        "by_difficulty": {
            str(diff): {
                "accuracy": m.accuracy,
                "mean": m.mean,
                "variance": m.variance,
                "std_dev": m.std_dev,
                "count": m.count,
            }
            for diff, m in by_difficulty.items()
        },
    }

    # Save statistics
    print("\n[5/5] Saving results...")
    results_dir = Path("results")

    # Save stats JSON
    stats_path = results_dir / "baseline_stats.json"
    with open(stats_path, "w") as f:
        json.dump(stats, f, indent=2)
    print(f"  Saved: {stats_path}")

    # Also copy raw results to expected location
    raw_results_path = results_dir / "baseline_results.csv"
    results_df.to_csv(raw_results_path, index=False)
    print(f"  Saved: {raw_results_path}")

    # Print summary
    print("\n" + "=" * 60)
    print("BASELINE EXPERIMENT RESULTS")
    print("=" * 60)

    print(f"\nOverall Statistics:")
    print(f"  Accuracy: {overall_metrics.accuracy:.2%}")
    print(f"  Variance: {overall_metrics.variance:.4f}")
    print(f"  Std Dev:  {overall_metrics.std_dev:.4f}")

    print(f"\nBy Category:")
    for cat, m in sorted(by_category.items()):
        print(f"  {cat:20s}: {m.accuracy:.2%} (n={m.count})")

    print(f"\nBy Difficulty:")
    for diff, m in sorted(by_difficulty.items()):
        diff_label = {1: "Easy", 2: "Medium", 3: "Hard"}[diff]
        print(f"  {diff_label:10s}: {m.accuracy:.2%} (n={m.count})")

    print("\n" + "=" * 60)
    print("Stage 2 Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
