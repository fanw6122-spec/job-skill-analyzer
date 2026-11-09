"""P03-P2 contract tests, written before the integration implementation."""

from __future__ import annotations

import io
import unittest

import pandas as pd

from analysis_service import available_cities, compute_statistics, prepare_jobs


def csv_bytes(text: str) -> io.BytesIO:
    return io.BytesIO(text.encode("utf-8-sig"))


SAMPLE = (
    "岗位编号,城市,岗位名称,技能\n"
    "001, 深圳 ,AI工程师,Python;RAG;Python\n"
    "002,成都,数据分析师,RAG\n"
    "003,深圳,后端工程师,Python\n"
    "004,   ,不合法,Agent\n"
)


class AnalysisServiceTests(unittest.TestCase):
    def test_uploaded_file_reuses_reader_and_cleaner_without_losing_ids(self) -> None:
        cleaned = prepare_jobs(csv_bytes(SAMPLE))
        self.assertEqual(cleaned["岗位编号"].tolist(), ["001", "002", "003"])
        self.assertEqual(cleaned["城市"].tolist(), ["深圳", "成都", "深圳"])

    def test_repeated_reads_of_same_uploaded_buffer_start_at_beginning(self) -> None:
        source = csv_bytes(SAMPLE)
        self.assertEqual(len(prepare_jobs(source)), 3)
        self.assertEqual(len(prepare_jobs(source)), 3)

    def test_missing_required_city_column_is_rejected(self) -> None:
        source = csv_bytes("岗位编号,岗位名称,技能\n001,AI工程师,Python\n")
        with self.assertRaisesRegex(ValueError, "城市"):
            prepare_jobs(source)

    def test_empty_csv_is_rejected_with_clear_error(self) -> None:
        with self.assertRaisesRegex(ValueError, "CSV.*空"):
            prepare_jobs(io.BytesIO(b""))

    def test_available_cities_are_deterministic_and_cleaned(self) -> None:
        self.assertEqual(available_cities(prepare_jobs(csv_bytes(SAMPLE))), ["成都", "深圳"])

    def test_stats_are_reused_and_same_job_skill_is_counted_once(self) -> None:
        df = prepare_jobs(csv_bytes(SAMPLE))
        before = df.copy(deep=True)
        city_counts, skill_counts = compute_statistics(df, "深圳")
        self.assertEqual(dict(zip(city_counts["城市"], city_counts["岗位数"])), {"深圳": 2, "成都": 1})
        self.assertEqual(dict(zip(skill_counts["技能"], skill_counts["岗位数"])), {"Python": 2, "RAG": 1})
        pd.testing.assert_frame_equal(df, before)


if __name__ == "__main__":
    unittest.main()
