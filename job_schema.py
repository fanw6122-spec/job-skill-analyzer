"""Validate the required recruiting CSV schema."""

import pandas as pd


REQUIRED_COLUMNS: tuple[str, ...] = ("岗位编号", "城市", "岗位名称", "技能")


def validate_required_columns(df: pd.DataFrame) -> None:
    """Raise a clear error before any business transformation starts."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")

    missing = sorted(set(REQUIRED_COLUMNS) - set(df.columns))
    if missing:
        raise ValueError(f"缺少必需列: {', '.join(missing)}")
