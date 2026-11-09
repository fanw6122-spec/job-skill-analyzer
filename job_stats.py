"""Count job records by city, regardless of missing skills."""

import pandas as pd

from input_contract import validate_input


def count_jobs_by_city(df: pd.DataFrame) -> pd.DataFrame:
    """Return city and job-row counts, sorted by count then city."""
    validate_input(df, ("城市",))
    if df.empty:
        return pd.DataFrame({"城市": pd.Series(dtype="string"), "岗位数": pd.Series(dtype="int64")})

    counts = df.groupby("城市").size().reset_index(name="岗位数")
    return counts.sort_values(["岗位数", "城市"], ascending=[False, True], kind="stable").reset_index(drop=True)
