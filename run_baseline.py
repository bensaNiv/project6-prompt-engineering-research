#!/usr/bin/env python3
"""
Run the baseline prompt engineering experiment.

This script executes the baseline (minimal) prompt across all test cases.
Results are saved to results/baseline_results.csv and results/baseline_stats.json.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.cli_runner import run_experiment
from src.prompts.base import BaselinePromptGenerator


if __name__ == "__main__":
    run_experiment(
        technique_name="baseline",
        prompt_generator_class=BaselinePromptGenerator,
        display_name="Baseline",
        time_factor=5,
    )
