#!/usr/bin/env python3
"""
Apply manual overrides to experiment results.

This script reads the manual_overrides.csv file and applies corrections
to the experiment results, then regenerates statistics.

Usage:
    python apply_overrides.py [technique_name]

    technique_name: baseline, fewshot, cot, role, etc. (default: baseline)

The script will:
1. Load results from results/{technique}_results.csv
2. Load overrides from data/manual_overrides.csv
3. Apply overrides to the 'correct' column
4. Save updated results
5. Regenerate statistics in results/{technique}_stats.json
"""

import json
import sys
from pathlib import Path

import pandas as pd


def load_overrides(overrides_path: Path) -> pd.DataFrame:
    """Load manual overrides, filtering out comments."""
    if not overrides_path.exists():
        print(f"  No overrides file found at {overrides_path}")
        return pd.DataFrame(columns=["id", "run", "technique", "correct_override", "reason"])

    # Read file, skip comment lines
    lines = []
    with open(overrides_path, "r") as f:
        for line in f:
            if not line.strip().startswith("#"):
                lines.append(line)

    if len(lines) <= 1:  # Only header or empty
        return pd.DataFrame(columns=["id", "run", "technique", "correct_override", "reason"])

    from io import StringIO
    return pd.read_csv(StringIO("".join(lines)))


def apply_overrides(results_df: pd.DataFrame, overrides_df: pd.DataFrame, technique: str) -> tuple[pd.DataFrame, int]:
    """Apply overrides to results DataFrame."""
    # Filter overrides for this technique
    technique_overrides = overrides_df[overrides_df["technique"] == technique]

    changes_made = 0
    for _, override in technique_overrides.iterrows():
        mask = (results_df["id"] == override["id"]) & (results_df["run"] == override["run"])

        if mask.any():
            old_val = results_df.loc[mask, "correct"].values[0]
            new_val = int(override["correct_override"])

            if old_val != new_val:
                results_df.loc[mask, "correct"] = new_val
                results_df.loc[mask, "confidence"] = 1.0 if new_val else 0.0
                changes_made += 1
                print(f"  Override applied: id={override['id']}, run={override['run']}: {old_val} -> {new_val}")
                print(f"    Reason: {override['reason']}")

    return results_df, changes_made


def calculate_stats(results_df: pd.DataFrame) -> dict:
    """Calculate statistics from results."""
    def calc_metrics(correct_values):
        count = len(correct_values)
        if count == 0:
            return {"accuracy": 0, "mean": 0, "variance": 0, "std_dev": 0, "count": 0}

        mean = sum(correct_values) / count
        variance = sum((x - mean) ** 2 for x in correct_values) / count if count > 1 else 0
        std_dev = variance ** 0.5
        accuracy = mean

        return {
            "accuracy": accuracy,
            "mean": mean,
            "variance": variance,
            "std_dev": std_dev,
            "count": count,
        }

    # Overall metrics
    overall = calc_metrics(results_df["correct"].tolist())

    # By category
    by_category = {}
    for cat in results_df["category"].unique():
        cat_data = results_df[results_df["category"] == cat]["correct"].tolist()
        by_category[cat] = calc_metrics(cat_data)

    # By difficulty
    by_difficulty = {}
    for diff in results_df["difficulty"].unique():
        diff_data = results_df[results_df["difficulty"] == diff]["correct"].tolist()
        by_difficulty[str(diff)] = calc_metrics(diff_data)

    return {
        "overall": overall,
        "by_category": by_category,
        "by_difficulty": by_difficulty,
    }


def main():
    """Apply overrides and regenerate statistics."""
    # Get technique name from command line
    technique = sys.argv[1] if len(sys.argv) > 1 else "baseline"

    print("=" * 60)
    print(f"Applying Manual Overrides: {technique}")
    print("=" * 60)

    # Paths
    results_dir = Path("results")
    data_dir = Path("data")

    results_path = results_dir / f"{technique}_results.csv"
    overrides_path = data_dir / "manual_overrides.csv"
    stats_path = results_dir / f"{technique}_stats.json"

    # Load results
    print(f"\n[1/4] Loading results from {results_path}...")
    if not results_path.exists():
        print(f"  ERROR: Results file not found: {results_path}")
        sys.exit(1)

    results_df = pd.read_csv(results_path)
    print(f"  Loaded {len(results_df)} rows")

    # Load overrides
    print(f"\n[2/4] Loading overrides from {overrides_path}...")
    overrides_df = load_overrides(overrides_path)
    technique_overrides = overrides_df[overrides_df["technique"] == technique] if not overrides_df.empty else pd.DataFrame()
    print(f"  Found {len(technique_overrides)} overrides for '{technique}'")

    # Apply overrides
    print(f"\n[3/4] Applying overrides...")
    results_df, changes_made = apply_overrides(results_df, overrides_df, technique)
    print(f"  Applied {changes_made} changes")

    # Save updated results
    if changes_made > 0:
        results_df.to_csv(results_path, index=False)
        print(f"  Saved updated results to {results_path}")

    # Regenerate statistics
    print(f"\n[4/4] Regenerating statistics...")
    stats = calculate_stats(results_df)

    with open(stats_path, "w") as f:
        json.dump(stats, f, indent=2)
    print(f"  Saved statistics to {stats_path}")

    # Print summary
    print("\n" + "=" * 60)
    print("UPDATED RESULTS SUMMARY")
    print("=" * 60)

    print(f"\nOverall Statistics:")
    print(f"  Accuracy: {stats['overall']['accuracy']:.2%}")
    print(f"  Variance: {stats['overall']['variance']:.4f}")
    print(f"  Std Dev:  {stats['overall']['std_dev']:.4f}")

    print(f"\nBy Category:")
    for cat, m in sorted(stats["by_category"].items()):
        print(f"  {cat:20s}: {m['accuracy']:.2%} (n={m['count']})")

    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)


if __name__ == "__main__":
    main()
