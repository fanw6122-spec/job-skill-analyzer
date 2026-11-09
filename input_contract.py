"""Reject malformed input before statistics can produce misleading results."""

import pandas as pd


def validate_input(df: pd.DataFrame, required: tuple[str, ...]) -> None:
    """Require the columns needed by the caller and P02-cleaned city values."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")

    if df.columns.duplicated().any():
        raise ValueError("输入数据存在重复列名")

    missing = sorted(set(required) - set(df.columns))
    if missing:
        raise ValueError(f"缺少必需列: {', '.join(missing)}")

    if "城市" in required and not df.empty:
        cities = df["城市"].astype("string").str.strip()
        invalid = cities.isna() | cities.eq("")
        if invalid.fillna(False).any():
            raise ValueError("城市存在缺失或纯空格内容，请先执行 P02 数据清洗")
