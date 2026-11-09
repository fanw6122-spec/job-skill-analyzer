"""P02-P1 acceptance contract: tests precede application code."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import pandas as pd

from job_cleaner import clean_jobs
from job_csv_reader import read_jobs_csv
from job_schema import validate_required_columns


SAMPLE_CSV = (
    "岗位编号,城市,岗位名称,技能\n"
    "001,成都, AI应用开发 ,Python;RAG\n"
    "002,深圳,Agent工程师,Python;Agent\n"
    "003,重庆,后端工程师,FastAPI\n"
    "004,,数据开发,Python\n"
    "005,成都,,RAG\n"
    "006, 深圳 ,后端工程师,Python\n"
    "007,   ,数据工程师,Python\n"
    "008,重庆,   ,Agent\n"
)


class JobCsvCleanerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.csv_path = Path(self.temp_dir.name) / "jobs.csv"
        self.csv_path.write_text(SAMPLE_CSV, encoding="utf-8")

    def test_read_csv_returns_dataframe_with_all_rows(self) -> None:
        df = read_jobs_csv(self.csv_path)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 8)

    def test_read_csv_preserves_leading_zeros_in_job_id(self) -> None:
        df = read_jobs_csv(self.csv_path)
        self.assertEqual(df.loc[0, "岗位编号"], "001")
        self.assertIsInstance(df.loc[0, "岗位编号"], str)

    def test_read_csv_accepts_utf8_bom(self) -> None:
        self.csv_path.write_text(SAMPLE_CSV, encoding="utf-8-sig")
        df = read_jobs_csv(self.csv_path)
        self.assertEqual(df.loc[0, "城市"], "成都")

    def test_nonexistent_csv_raises_file_not_found(self) -> None:
        with self.assertRaises(FileNotFoundError):
            read_jobs_csv(self.csv_path.with_name("missing.csv"))

    def test_missing_required_column_raises_clear_error(self) -> None:
        df = pd.DataFrame({"岗位编号": ["001"], "岗位名称": ["工程师"], "技能": ["Python"]})
        with self.assertRaisesRegex(ValueError, "城市"):
            validate_required_columns(df)

    def test_missing_skill_column_is_also_rejected(self) -> None:
        df = pd.DataFrame({"岗位编号": ["001"], "城市": ["成都"], "岗位名称": ["工程师"]})
        with self.assertRaisesRegex(ValueError, "技能"):
            clean_jobs(df)

    def test_non_dataframe_is_rejected(self) -> None:
        with self.assertRaises(TypeError):
            validate_required_columns(["城市", "岗位名称"])

    def test_cleaner_removes_null_and_whitespace_only_rows(self) -> None:
        cleaned = clean_jobs(read_jobs_csv(self.csv_path))
        self.assertEqual(cleaned["岗位编号"].tolist(), ["001", "002", "003", "006"])

    def test_cleaner_strips_city_and_job_name(self) -> None:
        cleaned = clean_jobs(read_jobs_csv(self.csv_path))
        self.assertEqual(cleaned.loc[cleaned["岗位编号"] == "001", "岗位名称"].iloc[0], "AI应用开发")
        self.assertEqual(cleaned.loc[cleaned["岗位编号"] == "006", "城市"].iloc[0], "深圳")

    def test_cleaner_does_not_change_original_dataframe(self) -> None:
        original = read_jobs_csv(self.csv_path)
        snapshot = original.copy(deep=True)
        cleaned = clean_jobs(original)
        pd.testing.assert_frame_equal(original, snapshot)
        cleaned.loc[cleaned["岗位编号"] == "006", "城市"] = "测试"
        pd.testing.assert_frame_equal(original, snapshot)

    def test_no_valid_rows_returns_empty_dataframe_with_columns(self) -> None:
        df = pd.DataFrame(
            {"岗位编号": ["001", "002"], "城市": [" ", None], "岗位名称": ["工程师", "数据开发"], "技能": ["Python", "RAG"]}
        )
        cleaned = clean_jobs(df)
        self.assertEqual(len(cleaned), 0)
        self.assertEqual(cleaned.columns.tolist(), df.columns.tolist())

    def test_valid_rows_are_retained_in_original_order(self) -> None:
        df = pd.DataFrame(
            {"岗位编号": ["A", "B"], "城市": ["成都", "深圳"], "岗位名称": ["工程师", "研究员"], "技能": ["Python", "Agent"]}
        )
        self.assertEqual(clean_jobs(df)["岗位编号"].tolist(), ["A", "B"])


if __name__ == "__main__":
    unittest.main()
