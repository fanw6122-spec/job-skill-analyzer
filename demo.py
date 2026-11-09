"""Command-line demo proving the P02 -> P03 integration without Streamlit."""

from pathlib import Path

from analysis_service import compute_statistics, prepare_jobs


def main() -> None:
    source = Path(__file__).parent / "data" / "sample_jobs.csv"
    cleaned = prepare_jobs(source)
    city_counts, skills = compute_statistics(cleaned, "深圳")
    cities = dict(zip(city_counts["城市"], city_counts["岗位数"]))
    shenzhen = dict(zip(skills["技能"], skills["岗位数"]))
    print("[P03-P2] CSV sample rows: 8")
    print(f"[P03-P2] Cleaned job records: {len(cleaned)}")
    print(f"[P03-P2] City counts: {cities}")
    print(f"[P03-P2] Shenzhen skill counts: {shenzhen}")
    assert len(cleaned) == 4
    assert cities == {"深圳": 2, "成都": 1, "重庆": 1}
    assert shenzhen == {"Python": 2, "Agent": 1}
    print("[PASS] Existing P02 cleaning and P03 statistics are integrated correctly.")


if __name__ == "__main__":
    main()
