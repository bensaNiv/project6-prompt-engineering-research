"""Shared CLI runner for prompt engineering experiments."""

import json
from datetime import datetime
from pathlib import Path
from typing import Type

from .config import Config
from .experiment_runner import ExperimentRunner
from .metrics import MetricsCalculator
from .ollama_client import OllamaClient
from .prompts.base import BasePromptGenerator


def run_experiment(
    technique_name: str,
    prompt_generator_class: Type[BasePromptGenerator],
    display_name: str | None = None,
    time_factor: int = 5,
) -> dict:
    """Run a prompt engineering experiment with the specified technique."""
    display_name = display_name or technique_name.replace("_", " ").title()
    print("=" * 60)
    print(f"{display_name} Experiment (Ollama)")
    print("=" * 60)
    print("\n[1/5] Loading configuration...")
    config = Config.from_env()
    config.runs_per_case, config.max_retries, config.retry_delay = 2, 3, 2.0
    print(f"  Model: {config.model_name}")
    print(f"  Runs per case: {config.runs_per_case}")
    print(f"  Ollama host: {config.ollama_host}")
    print("\n[2/5] Initializing Ollama client...")
    client = OllamaClient(config, host=config.ollama_host)
    models = client.list_models()
    if models:
        print(f"  Connected! Available models: {', '.join(models[:5])}")
        if not any(config.model_name in m for m in models):
            print(f"  WARNING: {config.model_name} not found. Available: {models}")
    else:
        print(f"  WARNING: Could not list models at {config.ollama_host}")
    runner = ExperimentRunner(config, client=client)
    prompt_generator = prompt_generator_class()
    metrics_calc = MetricsCalculator()
    test_cases = runner.load_test_cases()
    total_cases, total_calls = len(test_cases), len(test_cases) * config.runs_per_case
    print(f"  Test cases: {total_cases}")
    print(f"  Total API calls: {total_calls}")
    est_minutes = (total_calls * time_factor) / 60
    print(f"  Estimated time: ~{est_minutes:.0f}-{est_minutes*2:.0f} minutes")
    print(f"\n[3/5] Running {display_name.lower()} experiment...")
    results_df = runner.run_technique(technique_name, prompt_generator.generate)
    print(f"\n  Completed: {len(results_df)} responses collected")
    api_errors = results_df[~results_df["success"]]
    if len(api_errors) > 0:
        print(f"  WARNING: {len(api_errors)} API errors occurred")
    print("\n[4/5] Calculating statistics...")
    overall = metrics_calc.calculate_metrics(results_df["correct"].tolist())
    by_category = metrics_calc.aggregate_by_category(results_df)
    by_difficulty = metrics_calc.aggregate_by_difficulty(results_df)
    stats = _build_stats_dict(overall, by_category, by_difficulty)
    print("\n[5/5] Saving results...")
    _save_results(technique_name, results_df, stats)
    _print_summary(display_name, overall, by_category, by_difficulty)
    return stats


def _build_stats_dict(overall, by_category: dict, by_difficulty: dict) -> dict:
    """Build statistics dictionary from metrics."""
    return {
        "overall": {
            "accuracy": overall.accuracy,
            "mean": overall.mean,
            "variance": overall.variance,
            "std_dev": overall.std_dev,
            "count": overall.count,
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


def _save_results(technique_name: str, results_df, stats: dict) -> None:
    """Save results CSV and stats JSON."""
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)

    stats_path = results_dir / f"{technique_name}_stats.json"
    with open(stats_path, "w") as f:
        json.dump(stats, f, indent=2)
    print(f"  Saved: {stats_path}")

    raw_path = results_dir / f"{technique_name}_results.csv"
    try:
        results_df.to_csv(raw_path, index=False)
        print(f"  Saved: {raw_path}")
    except PermissionError:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        alt_path = results_dir / f"{technique_name}_results_{timestamp}.csv"
        results_df.to_csv(alt_path, index=False)
        print(f"  WARNING: Could not save to {raw_path} (file is open)")
        print(f"  Saved to: {alt_path}")


def _print_summary(display_name: str, overall, by_category: dict, by_difficulty: dict) -> None:
    """Print experiment summary."""
    print("\n" + "=" * 60)
    print(f"{display_name.upper()} EXPERIMENT RESULTS")
    print("=" * 60)

    print("\nOverall Statistics:")
    print(f"  Accuracy: {overall.accuracy:.2%}")
    print(f"  Variance: {overall.variance:.4f}")
    print(f"  Std Dev:  {overall.std_dev:.4f}")

    print("\nBy Category:")
    for cat, m in sorted(by_category.items()):
        print(f"  {cat:20s}: {m.accuracy:.2%} (n={m.count})")

    print("\nBy Difficulty:")
    diff_labels = {1: "Easy", 2: "Medium", 3: "Hard"}
    for diff, m in sorted(by_difficulty.items()):
        label = diff_labels.get(diff, str(diff))
        print(f"  {label:10s}: {m.accuracy:.2%} (n={m.count})")

    print("\n" + "=" * 60)
    print(f"{display_name} Experiment Complete!")
    print("=" * 60)
