"""Utilities for applying manual overrides to experiment results."""

from io import StringIO
from pathlib import Path

import pandas as pd


def load_overrides(overrides_path: Path | str) -> pd.DataFrame:
    """
    Load manual overrides, filtering out comment lines.

    Parameters
    ----------
    overrides_path : Path or str
        Path to the manual_overrides.csv file.

    Returns
    -------
    pd.DataFrame
        DataFrame with override data.
    """
    overrides_path = Path(overrides_path)

    if not overrides_path.exists():
        print(f"  No overrides file found at {overrides_path}")
        return pd.DataFrame(columns=["id", "run", "technique", "correct_override", "reason"])

    lines = []
    with open(overrides_path, "r") as f:
        for line in f:
            if not line.strip().startswith("#"):
                lines.append(line)

    if len(lines) <= 1:
        return pd.DataFrame(columns=["id", "run", "technique", "correct_override", "reason"])

    return pd.read_csv(StringIO("".join(lines)))


def apply_overrides(
    results_df: pd.DataFrame,
    overrides_df: pd.DataFrame,
    technique: str
) -> tuple[pd.DataFrame, int]:
    """
    Apply overrides to results DataFrame.

    Parameters
    ----------
    results_df : pd.DataFrame
        The experiment results to modify.
    overrides_df : pd.DataFrame
        The override instructions.
    technique : str
        The technique name to filter overrides for.

    Returns
    -------
    tuple[pd.DataFrame, int]
        Modified results DataFrame and count of changes made.
    """
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
                print(f"  Override: id={override['id']}, run={override['run']}: {old_val} -> {new_val}")
                print(f"    Reason: {override['reason']}")

    return results_df, changes_made


def calculate_stats(results_df: pd.DataFrame) -> dict:
    """
    Calculate statistics from results DataFrame.

    Parameters
    ----------
    results_df : pd.DataFrame
        The experiment results.

    Returns
    -------
    dict
        Statistics dictionary with overall, by_category, and by_difficulty metrics.
    """
    def calc_metrics(correct_values: list) -> dict:
        count = len(correct_values)
        if count == 0:
            return {"accuracy": 0, "mean": 0, "variance": 0, "std_dev": 0, "count": 0}

        mean = sum(correct_values) / count
        variance = sum((x - mean) ** 2 for x in correct_values) / count if count > 1 else 0
        std_dev = variance ** 0.5

        return {
            "accuracy": mean,
            "mean": mean,
            "variance": variance,
            "std_dev": std_dev,
            "count": count,
        }

    overall = calc_metrics(results_df["correct"].tolist())

    by_category = {}
    for cat in results_df["category"].unique():
        cat_data = results_df[results_df["category"] == cat]["correct"].tolist()
        by_category[cat] = calc_metrics(cat_data)

    by_difficulty = {}
    for diff in results_df["difficulty"].unique():
        diff_data = results_df[results_df["difficulty"] == diff]["correct"].tolist()
        by_difficulty[str(diff)] = calc_metrics(diff_data)

    return {
        "overall": overall,
        "by_category": by_category,
        "by_difficulty": by_difficulty,
    }
