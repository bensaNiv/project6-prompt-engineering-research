#!/usr/bin/env python3
"""Generate all visualization figures for the prompt engineering research."""

import json
import os
import sys
import pandas as pd
from pathlib import Path
from src.visualization import PromptResearchVisualizer



# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))
os.chdir(Path(__file__).parent.parent)


def load_results() -> dict[str, pd.DataFrame]:
    """Load all result CSV files."""
    results_dir = Path("results")
    techniques = ["baseline", "improved", "few_shot", "cot", "role_based"]

    results = {}
    for technique in techniques:
        filepath = results_dir / f"{technique}_results.csv"
        if filepath.exists():
            results[technique] = pd.read_csv(filepath)
            print(f"Loaded {technique}: {len(results[technique])} rows")
        else:
            print(f"Warning: {filepath} not found")

    return results


def load_stats() -> dict:
    """Load all stats files and combine into comparison format."""
    results_dir = Path("results")
    techniques = ["baseline", "improved", "few_shot", "cot", "role_based"]

    stats = {"by_technique": {}}
    baseline_accuracy = None

    for technique in techniques:
        filepath = results_dir / f"{technique}_stats.json"
        if filepath.exists():
            with open(filepath) as f:
                tech_stats = json.load(f)
                stats["by_technique"][technique] = tech_stats["overall"]
                stats["by_technique"][technique]["by_category"] = tech_stats["by_category"]

                if technique == "baseline":
                    baseline_accuracy = tech_stats["overall"]["accuracy"]
                elif baseline_accuracy is not None:
                    # Calculate improvement percentage
                    current_acc = tech_stats["overall"]["accuracy"]
                    improvement = ((current_acc - baseline_accuracy) / baseline_accuracy) * 100
                    stats["by_technique"][technique]["improvement_pct"] = improvement

            print(f"Loaded {technique}_stats.json")
        else:
            print(f"Warning: {filepath} not found")

    # Save combined stats
    stats_dir = results_dir / "stats"
    stats_dir.mkdir(exist_ok=True)
    with open(stats_dir / "comparison_stats.json", "w") as f:
        json.dump(stats, f, indent=2)
    print("Saved comparison_stats.json")

    return stats


def main():
    """Generate all figures."""
    print("=" * 60)
    print("Generating Prompt Engineering Research Figures")
    print("=" * 60)

    # Load data
    print("\nLoading results...")
    results = load_results()

    print("\nLoading statistics...")
    stats = load_stats()

    # Create visualizer and generate figures
    print("\nGenerating figures...")
    visualizer = PromptResearchVisualizer(results_dir="results")

    print("  - Accuracy comparison bar chart...")
    visualizer.plot_accuracy_comparison(stats)

    print("  - Improvement bars chart...")
    visualizer.plot_improvement_bars(stats)

    print("  - Accuracy heatmap (technique x category)...")
    visualizer.plot_accuracy_heatmap(results)

    print("  - Difficulty heatmap (technique x difficulty)...")
    visualizer.plot_difficulty_heatmap(results)

    print("  - Variance boxplot...")
    visualizer.plot_variance_boxplot(results)

    print("  - Radar comparison chart...")
    visualizer.plot_radar_comparison(stats, results)

    print("  - Difficulty trend line chart...")
    visualizer.plot_difficulty_trend(results)

    print("  - Score histograms...")
    visualizer.plot_score_histograms(results)

    print("\n" + "=" * 60)
    print("All figures generated successfully!")
    print("Output directory: results/figures/")
    print("=" * 60)

    # List generated files
    figures_dir = Path("results/figures")
    print("\nGenerated files:")
    for f in sorted(figures_dir.glob("*.png")):
        print(f"  - {f.name}")


if __name__ == "__main__":
    main()
