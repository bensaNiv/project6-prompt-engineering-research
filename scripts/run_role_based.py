#!/usr/bin/env python3
"""
Run the role-based prompt engineering experiment.

This script executes the role-based prompt technique across all test cases.
Results are saved to results/role_based_results.csv and results/role_based_stats.json.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.cli_runner import run_experiment
from src.prompts.role_based import RoleBasedPromptGenerator


if __name__ == "__main__":
    run_experiment(
        technique_name="role_based",
        prompt_generator_class=RoleBasedPromptGenerator,
        display_name="Role-Based",
        time_factor=5,
    )
