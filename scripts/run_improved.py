#!/usr/bin/env python3
"""
Run the improved prompt engineering experiment.

This script executes the improved prompt technique across all test cases.
Results are saved to results/improved_results.csv and results/improved_stats.json.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.cli_runner import run_experiment
from src.prompts.improved import ImprovedPromptGenerator


if __name__ == "__main__":
    run_experiment(
        technique_name="improved",
        prompt_generator_class=ImprovedPromptGenerator,
        display_name="Improved",
        time_factor=5,
    )
