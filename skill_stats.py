"""Count job demand for each skill (one vote per skill per job row)."""

import pandas as pd

from input_contract import validate_input


def _empty_skill_counts() -> pd.DataFrame:
    return pd.DataFrame({"技能": pd.Series(dtype="string"), "岗位数": pd.Series(dtype="int64")})


def count_skills(df: pd.DataFrame, city: str | None = None) -> pd.DataFrame:
    """Return skill/job counts across all cities or a single selected city.

    English semicolons separate skills. Skill case is preserved. Repeated
    skill tokens within one job row count only once; different rows count
    as different job records even if their DataFrame indices are identical.
    """
    validate_input(df, ("城市", "技能"))
    if city is not None and (not isinstance(city, str) or not city.strip()):
        raise ValueError("city must be a nonempty city name or None")

    filtered = df if city is None else df.loc[df["城市"] == city]
    if filtered.empty:
        return _empty_skill_counts()

    # A fresh zero-based index is a unique row identifier even when callers
    # supply repeated DataFrame index labels.
    row_skills = filtered["技能"].reset_index(drop=True).astype("string")
    tokens = row_skills.str.split(";").explode().dropna().str.strip()
    tokens = tokens.loc[tokens.ne("")]
    if tokens.empty:
        return _empty_skill_counts()

    job_skill_pairs = tokens.reset_index()
    job_skill_pairs.columns = ["job_row", "技能"]
    job_skill_pairs = job_skill_pairs.drop_duplicates(subset=["job_row", "技能"])

    counts = job_skill_pairs.groupby("技能").size().reset_index(name="岗位数")
    return counts.sort_values(["岗位数", "技能"], ascending=[False, True], kind="stable").reset_index(drop=True)
