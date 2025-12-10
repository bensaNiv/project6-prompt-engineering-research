#!/usr/bin/env python3
"""
Run the few-shot prompt engineering experiment.

This script executes the few-shot prompt technique across all 100 test cases,
running each case 2 times to measure consistency. Results are saved to:
- results/few_shot_results.csv (raw data)
- results/few_shot_stats.json (aggregated statistics)
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
from src.prompts.few_shot import FewShotPromptGenerator


def main() -> None:
    """Run the few-shot prompt experiment and generate statistics."""
    print("=" * 60)
    print("Stage 3: Few-Shot Prompt Experiment (Ollama)")
    print("=" * 60)

    # Configuration for Ollama
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
    prompt_generator = FewShotPromptGenerator()
    metrics_calc = MetricsCalculator()

    # Load test cases to show count
    test_cases = runner.load_test_cases()
    total_cases = len(test_cases)
    total_calls = total_cases * config.runs_per_case
    print(f"  Test cases: {total_cases}")
    print(f"  Total API calls: {total_calls}")

    # Estimate time for Ollama
    est_minutes = (total_calls * 5) / 60
    print(f"  Estimated time: ~{est_minutes:.0f}-{est_minutes*2:.0f} minutes")

    # Run few-shot prompt experiment
    print(f"\n[3/5] Running few-shot prompt experiment ({total_calls} API calls)...")
    print("  Progress will be shown below...")

    results_df = runner.run_technique(
        technique_name="few_shot",
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
    stats_path = results_dir / "few_shot_stats.json"
    with open(stats_path, "w") as f:
        json.dump(stats, f, indent=2)
    print(f"  Saved: {stats_path}")

    # Also copy raw results to expected location
    raw_results_path = results_dir / "few_shot_results.csv"
    try:
        results_df.to_csv(raw_results_path, index=False)
        print(f"  Saved: {raw_results_path}")
    except PermissionError:
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        alt_path = results_dir / f"few_shot_results_{timestamp}.csv"
        results_df.to_csv(alt_path, index=False)
        print(f"  WARNING: Could not save to {raw_results_path} (file is open)")
        print(f"  Saved to: {alt_path}")

    # Print summary
    print("\n" + "=" * 60)
    print("FEW-SHOT PROMPT EXPERIMENT RESULTS")
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
        diff_label = {1: "Easy", 2: "Medium", 3: "Hard"}.get(diff, str(diff))
        print(f"  {diff_label:10s}: {m.accuracy:.2%} (n={m.count})")

    print("\n" + "=" * 60)
    print("Few-Shot Prompt Experiment Complete!")
    print("=" * 60)

    return stats


if __name__ == "__main__":
    main()
