#!/usr/bin/env python3
"""
Run all prompt engineering technique experiments.

This master script runs all 4 prompt techniques sequentially:
1. Improved Prompt
2. Few-Shot Learning
3. Chain-of-Thought
4. Role-Based Prompting

Each technique runs 100 test cases x 2 runs = 200 API calls.
Total: 800 API calls across all techniques.

Results are saved to:
- results/{technique}_results.csv (raw data)
- results/{technique}_stats.json (aggregated statistics)
- results/comparison_stats.json (cross-technique comparison)
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import main functions from each runner
from run_improved import main as run_improved_main
from run_few_shot import main as run_few_shot_main
from run_cot import main as run_cot_main
from run_role_based import main as run_role_based_main


def generate_comparison_stats() -> None:
    """Generate comparison statistics across all techniques."""
    results_dir = Path("results")

    techniques = ["baseline", "improved", "few_shot", "cot", "role_based"]
    all_stats = {}

    # Load all stats files
    for technique in techniques:
        stats_path = results_dir / f"{technique}_stats.json"
        if stats_path.exists():
            with open(stats_path) as f:
                all_stats[technique] = json.load(f)

    if not all_stats:
        print("  WARNING: No stats files found to compare")
        return

    # Get baseline accuracy for comparison
    baseline_accuracy = all_stats.get("baseline", {}).get("overall", {}).get("accuracy", 0)

    # Build comparison stats
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

        # Calculate improvement over baseline
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


def print_final_summary() -> None:
    """Print final comparison summary."""
    results_dir = Path("results")
    comparison_path = results_dir / "comparison_stats.json"

    if not comparison_path.exists():
        return

    with open(comparison_path) as f:
        comparison = json.load(f)

    print("\n" + "=" * 70)
    print("FINAL COMPARISON SUMMARY")
    print("=" * 70)

    # Technique comparison
    print("\nAccuracy by Technique:")
    print("-" * 50)

    by_technique = comparison.get("by_technique", {})
    baseline_acc = by_technique.get("baseline", {}).get("accuracy", 0)

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

    # Best technique per category
    print("\nBest Technique by Category:")
    print("-" * 50)

    by_category = comparison.get("by_category", {})
    for category in sorted(by_category.keys()):
        cat_data = by_category[category]
        best = cat_data.get("best_technique", "unknown")
        best_acc = cat_data.get(best, 0)
        print(f"  {category:20s}: {best:15s} ({best_acc:.2%})")

    print("\n" + "=" * 70)


def main() -> None:
    """Run all prompt engineering experiments."""
    start_time = datetime.now()

    print("=" * 70)
    print("STAGE 3: ALL PROMPT TECHNIQUES EXPERIMENT")
    print("=" * 70)
    print(f"\nStarted at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nThis will run 4 techniques x 100 cases x 2 runs = 800 API calls")
    print("Estimated total time: ~67-135 minutes\n")

    techniques = [
        ("Improved", run_improved_main),
        ("Few-Shot", run_few_shot_main),
        ("Chain-of-Thought", run_cot_main),
        ("Role-Based", run_role_based_main),
    ]

    results = {}

    for i, (name, runner) in enumerate(techniques, 1):
        print(f"\n{'='*70}")
        print(f"TECHNIQUE {i}/4: {name}")
        print(f"{'='*70}\n")

        try:
            stats = runner()
            results[name] = stats
            print(f"\n[OK] {name} completed successfully")
        except Exception as e:
            print(f"\n[ERROR] {name} failed: {e}")
            results[name] = {"error": str(e)}

    # Generate comparison stats
    print("\n" + "=" * 70)
    print("GENERATING COMPARISON STATISTICS")
    print("=" * 70)
    generate_comparison_stats()

    # Print final summary
    print_final_summary()

    # Final timing
    end_time = datetime.now()
    duration = end_time - start_time

    print(f"\nCompleted at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total duration: {duration}")

    print("\n" + "=" * 70)
    print("STAGE 3 COMPLETE!")
    print("=" * 70)
    print("\nDeliverables:")
    print("  - results/improved_results.csv")
    print("  - results/few_shot_results.csv")
    print("  - results/cot_results.csv")
    print("  - results/role_based_results.csv")
    print("  - results/comparison_stats.json")
    print("\nNext steps:")
    print("  1. Review results and add overrides to data/manual_overrides.csv")
    print("  2. Run: python apply_overrides.py <technique_name>")
    print("  3. Proceed to Stage 4: python PRPs/04-stage-4-analysis.md")


if __name__ == "__main__":
    main()
