"""Thin integration layer: P02 CSV preparation followed by P03 statistics."""

from __future__ import annotations

from pathlib import Path
from typing import BinaryIO

import pandas as pd

from job_cleaner import clean_jobs
from job_csv_reader import read_jobs_csv
from job_stats import count_jobs_by_city
from skill_stats import count_skills


def prepare_jobs(source: str | Path | BinaryIO) -> pd.DataFrame:
    """Read and clean the uploaded CSV; reject malformed input explicitly."""
    if hasattr(source, "seek"):
        source.seek(0)
    try:
        raw = read_jobs_csv(source)
    except pd.errors.EmptyDataError as exc:
        raise ValueError("CSV 文件为空或不包含表头") from exc
    except UnicodeDecodeError as exc:
        raise ValueError("CSV 编码错误，请使用 UTF-8 编码") from exc
    except pd.errors.ParserError as exc:
        raise ValueError("CSV 格式错误，无法正确解析记录") from exc
    return clean_jobs(raw)


def available_cities(df: pd.DataFrame) -> list[str]:
    """Build deterministic selectbox choices from P02-cleaned records."""
    if "城市" not in df.columns:
        raise ValueError("缺少必需列: 城市")
    return sorted(str(city) for city in df["城市"].dropna().unique())


def compute_statistics(
    cleaned: pd.DataFrame, city: str | None
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Keep both proven P03 statistics functions unchanged."""
    return count_jobs_by_city(cleaned), count_skills(cleaned, city)
