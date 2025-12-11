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
"""

import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.cli_runner import run_experiment
from src.comparison_utils import generate_comparison_stats, print_final_summary
from src.prompts.improved import ImprovedPromptGenerator
from src.prompts.few_shot import FewShotPromptGenerator
from src.prompts.chain_of_thought import ChainOfThoughtPromptGenerator
from src.prompts.role_based import RoleBasedPromptGenerator


TECHNIQUES = [
    ("improved", ImprovedPromptGenerator, "Improved", 5),
    ("few_shot", FewShotPromptGenerator, "Few-Shot", 5),
    ("cot", ChainOfThoughtPromptGenerator, "Chain-of-Thought", 7),
    ("role_based", RoleBasedPromptGenerator, "Role-Based", 5),
]


def main() -> None:
    """Run all prompt engineering experiments."""
    start_time = datetime.now()

    print("=" * 70)
    print("STAGE 3: ALL PROMPT TECHNIQUES EXPERIMENT")
    print("=" * 70)
    print(f"\nStarted at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nThis will run 4 techniques x 100 cases x 2 runs = 800 API calls")
    print("Estimated total time: ~67-135 minutes\n")

    results = {}

    for i, (name, generator_class, display, time_factor) in enumerate(TECHNIQUES, 1):
        print(f"\n{'='*70}")
        print(f"TECHNIQUE {i}/4: {display}")
        print(f"{'='*70}\n")

        try:
            stats = run_experiment(name, generator_class, display, time_factor)
            results[name] = stats
            print(f"\n[OK] {display} completed successfully")
        except Exception as e:
            print(f"\n[ERROR] {display} failed: {e}")
            results[name] = {"error": str(e)}

    print("\n" + "=" * 70)
    print("GENERATING COMPARISON STATISTICS")
    print("=" * 70)
    generate_comparison_stats()
    print_final_summary()

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
    print("  2. Run: python scripts/apply_overrides.py <technique_name>")
    print("  3. Proceed to Stage 4: python scripts/generate_figures.py")


if __name__ == "__main__":
    main()
