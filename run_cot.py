#!/usr/bin/env python3
"""
Run the chain-of-thought prompt engineering experiment.

This script executes the chain-of-thought prompt technique across all test cases.
Results are saved to results/cot_results.csv and results/cot_stats.json.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.cli_runner import run_experiment
from src.prompts.chain_of_thought import ChainOfThoughtPromptGenerator


if __name__ == "__main__":
    run_experiment(
        technique_name="cot",
        prompt_generator_class=ChainOfThoughtPromptGenerator,
        display_name="Chain-of-Thought",
        time_factor=7,
    )
