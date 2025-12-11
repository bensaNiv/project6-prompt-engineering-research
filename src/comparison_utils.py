"""Comparison utilities for analyzing results across techniques."""

import json
from datetime import datetime
from pathlib import Path


def generate_comparison_stats(results_dir: Path | str = "results") -> dict:
    """Generate comparison statistics across all techniques."""
    results_dir = Path(results_dir)
    techniques = ["baseline", "improved", "few_shot", "cot", "role_based"]
    all_stats = {}

    for technique in techniques:
        stats_path = results_dir / f"{technique}_stats.json"
        if stats_path.exists():
            with open(stats_path) as f:
                all_stats[technique] = json.load(f)

    if not all_stats:
        print("  WARNING: No stats files found to compare")
        return {}

    baseline_accuracy = all_stats.get("baseline", {}).get("overall", {}).get("accuracy", 0)

    comparison = {
        "generated_at": datetime.now().isoformat(),
        "by_technique": {},
        "by_category": {},
        "by_difficulty": {},
    }

    # Per-technique comparison
    for technique, stats in all_stats.items():
        overall = stats.get("overall", {})
        accuracy = overall.get("accuracy", 0)

        comparison["by_technique"][technique] = {
            "accuracy": accuracy,
            "mean": overall.get("mean", 0),
            "variance": overall.get("variance", 0),
            "std_dev": overall.get("std_dev", 0),
            "count": overall.get("count", 0),
        }

        if technique != "baseline" and baseline_accuracy > 0:
            improvement_pct = ((accuracy - baseline_accuracy) / baseline_accuracy) * 100
            comparison["by_technique"][technique]["improvement_pct"] = round(improvement_pct, 2)

    # Per-category comparison
    categories = set()
    for stats in all_stats.values():
        categories.update(stats.get("by_category", {}).keys())

    for category in categories:
        comparison["by_category"][category] = {}
        best_technique = None
        best_accuracy = 0

        for technique, stats in all_stats.items():
            cat_stats = stats.get("by_category", {}).get(category, {})
            accuracy = cat_stats.get("accuracy", 0)
            comparison["by_category"][category][technique] = accuracy

            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best_technique = technique

        comparison["by_category"][category]["best_technique"] = best_technique

    # Per-difficulty comparison
    difficulties = set()
    for stats in all_stats.values():
        difficulties.update(stats.get("by_difficulty", {}).keys())

    for difficulty in difficulties:
        comparison["by_difficulty"][difficulty] = {}
        for technique, stats in all_stats.items():
            diff_stats = stats.get("by_difficulty", {}).get(difficulty, {})
            comparison["by_difficulty"][difficulty][technique] = diff_stats.get("accuracy", 0)

    # Save comparison stats
    comparison_path = results_dir / "comparison_stats.json"
    with open(comparison_path, "w") as f:
        json.dump(comparison, f, indent=2)
    print(f"  Saved: {comparison_path}")

    return comparison


def print_final_summary(results_dir: Path | str = "results") -> None:
    """Print final comparison summary."""
    results_dir = Path(results_dir)
    comparison_path = results_dir / "comparison_stats.json"

    if not comparison_path.exists():
        return

    with open(comparison_path) as f:
        comparison = json.load(f)

    print("\n" + "=" * 70)
    print("FINAL COMPARISON SUMMARY")
    print("=" * 70)

    print("\nAccuracy by Technique:")
    print("-" * 50)

    by_technique = comparison.get("by_technique", {})

    for technique in ["baseline", "improved", "few_shot", "cot", "role_based"]:
        if technique in by_technique:
            stats = by_technique[technique]
            acc = stats.get("accuracy", 0)
            improvement = stats.get("improvement_pct", 0)

            if technique == "baseline":
                print(f"  {technique:15s}: {acc:.2%} (baseline)")
            else:
                sign = "+" if improvement >= 0 else ""
                print(f"  {technique:15s}: {acc:.2%} ({sign}{improvement:.1f}%)")

    print("\nBest Technique by Category:")
    print("-" * 50)

    by_category = comparison.get("by_category", {})
    for category in sorted(by_category.keys()):
        cat_data = by_category[category]
        best = cat_data.get("best_technique", "unknown")
        best_acc = cat_data.get(best, 0)
        print(f"  {category:20s}: {best:15s} ({best_acc:.2%})")

    print("\n" + "=" * 70)
