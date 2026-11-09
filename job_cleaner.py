"""Normalize and filter recruiting records without mutating the input."""

import pandas as pd

from job_schema import validate_required_columns


TEXT_COLUMNS: tuple[str, str] = ("城市", "岗位名称")


def clean_jobs(df: pd.DataFrame) -> pd.DataFrame:
    """Remove invalid city/job-name values; preserve order and other fields."""
    validate_required_columns(df)
    result = df.copy(deep=True)

    for column in TEXT_COLUMNS:
        # Treat whitespace-only text the same way as genuinely missing text.
        result[column] = result[column].astype("string").str.strip().replace("", pd.NA)

    return result.dropna(subset=list(TEXT_COLUMNS)).copy()
