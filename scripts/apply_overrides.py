#!/usr/bin/env python3
"""
Apply manual overrides to experiment results.

This script reads the manual_overrides.csv file and applies corrections
to the experiment results, then regenerates statistics.

Usage:
    python apply_overrides.py [technique_name]

    technique_name: baseline, fewshot, cot, role, etc. (default: baseline)
"""

import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.override_utils import load_overrides, apply_overrides, calculate_stats


def main() -> None:
    """Apply overrides and regenerate statistics."""
    technique = sys.argv[1] if len(sys.argv) > 1 else "baseline"

    print("=" * 60)
    print(f"Applying Manual Overrides: {technique}")
    print("=" * 60)

    results_dir = Path("results")
    data_dir = Path("data")

    results_path = results_dir / f"{technique}_results.csv"
    overrides_path = data_dir / "manual_overrides.csv"
    stats_path = results_dir / f"{technique}_stats.json"

    print(f"\n[1/4] Loading results from {results_path}...")
    if not results_path.exists():
        print(f"  ERROR: Results file not found: {results_path}")
        sys.exit(1)

    results_df = pd.read_csv(results_path)
    print(f"  Loaded {len(results_df)} rows")

    print(f"\n[2/4] Loading overrides from {overrides_path}...")
    overrides_df = load_overrides(overrides_path)
    technique_overrides = overrides_df[overrides_df["technique"] == technique] if not overrides_df.empty else pd.DataFrame()
    print(f"  Found {len(technique_overrides)} overrides for '{technique}'")

    print("\n[3/4] Applying overrides...")
    results_df, changes_made = apply_overrides(results_df, overrides_df, technique)
    print(f"  Applied {changes_made} changes")

    if changes_made > 0:
        results_df.to_csv(results_path, index=False)
        print(f"  Saved updated results to {results_path}")

    print("\n[4/4] Regenerating statistics...")
    stats = calculate_stats(results_df)

    with open(stats_path, "w") as f:
        json.dump(stats, f, indent=2)
    print(f"  Saved statistics to {stats_path}")

    print("\n" + "=" * 60)
    print("UPDATED RESULTS SUMMARY")
    print("=" * 60)

    print("\nOverall Statistics:")
    print(f"  Accuracy: {stats['overall']['accuracy']:.2%}")
    print(f"  Variance: {stats['overall']['variance']:.4f}")
    print(f"  Std Dev:  {stats['overall']['std_dev']:.4f}")

    print("\nBy Category:")
    for cat, m in sorted(stats["by_category"].items()):
        print(f"  {cat:20s}: {m['accuracy']:.2%} (n={m['count']})")

    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)


if __name__ == "__main__":
    main()
