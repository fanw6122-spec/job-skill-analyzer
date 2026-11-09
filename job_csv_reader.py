"""Read CSV bytes; leave business validation to the other modules."""

from pathlib import Path
from typing import BinaryIO

import pandas as pd


def read_jobs_csv(csv_path: str | Path | BinaryIO) -> pd.DataFrame:
    """Load UTF-8 / UTF-8-BOM CSV while preserving identifier text."""
    return pd.read_csv(
        csv_path,
        encoding="utf-8-sig",
        dtype={"岗位编号": "string", "城市": "string", "岗位名称": "string"},
    )
