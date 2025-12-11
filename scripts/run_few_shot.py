#!/usr/bin/env python3
"""
Run the few-shot prompt engineering experiment.

This script executes the few-shot prompt technique across all test cases.
Results are saved to results/few_shot_results.csv and results/few_shot_stats.json.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.cli_runner import run_experiment
from src.prompts.few_shot import FewShotPromptGenerator


if __name__ == "__main__":
    run_experiment(
        technique_name="few_shot",
        prompt_generator_class=FewShotPromptGenerator,
        display_name="Few-Shot",
        time_factor=5,
    )
