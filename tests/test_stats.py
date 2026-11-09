"""P03-P1 executable acceptance tests, written before implementation."""

import unittest

import pandas as pd

from input_contract import validate_input
from job_stats import count_jobs_by_city
from skill_stats import count_skills


def sample_jobs() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "岗位编号": ["A", "B", "C", "D", "E", "F"],
            "城市": ["成都", "成都", "深圳", "深圳", "重庆", "深圳"],
            "岗位名称": ["开发", "测试", "Agent工程师", "应用开发", "研究员", "工程师"],
            "技能": ["Python", pd.NA, "Agent", "Python;RAG", "Agent", "Python;Python"],
        }
    )


def count_map(result: pd.DataFrame, key: str) -> dict[str, int]:
    return dict(zip(result[key].tolist(), result["岗位数"].tolist()))


class JobCountTests(unittest.TestCase):
    def test_city_job_counts_include_rows_with_missing_skill(self) -> None:
        self.assertEqual(count_map(count_jobs_by_city(sample_jobs()), "城市"), {"成都": 2, "深圳": 3, "重庆": 1})

    def test_city_count_sort_order_is_deterministic(self) -> None:
        self.assertEqual(count_jobs_by_city(sample_jobs())["城市"].tolist(), ["深圳", "成都", "重庆"])

    def test_city_statistics_reject_missing_city_column(self) -> None:
        with self.assertRaisesRegex(ValueError, "城市"):
            count_jobs_by_city(pd.DataFrame({"技能": ["Python"]}))

    def test_invalid_city_cells_cannot_silently_disappear_from_statistics(self) -> None:
        df = sample_jobs()
        df.loc[0, "城市"] = "   "
        with self.assertRaisesRegex(ValueError, "P02"):
            count_jobs_by_city(df)


class SkillCountTests(unittest.TestCase):
    def test_all_cities_skill_count_by_jobs_not_tokens(self) -> None:
        self.assertEqual(count_map(count_skills(sample_jobs()), "技能"), {"Python": 3, "Agent": 2, "RAG": 1})

    def test_shenzhen_skill_counts_after_city_filter(self) -> None:
        self.assertEqual(count_map(count_skills(sample_jobs(), city="深圳"), "技能"), {"Python": 2, "Agent": 1, "RAG": 1})

    def test_duplicate_skill_inside_one_job_is_counted_once(self) -> None:
        df = pd.DataFrame({"城市": ["深圳"], "技能": ["Python;Python;Python"]})
        self.assertEqual(count_map(count_skills(df), "技能"), {"Python": 1})

    def test_whitespace_around_skill_tokens_is_removed(self) -> None:
        df = pd.DataFrame({"城市": ["成都"], "技能": [" Python ; RAG "]})
        self.assertEqual(count_map(count_skills(df), "技能"), {"Python": 1, "RAG": 1})

    def test_missing_and_empty_skill_tokens_are_ignored(self) -> None:
        df = pd.DataFrame({"城市": ["成都", "成都", "成都"], "技能": [None, " ; ; ", "Python;;RAG;"]})
        self.assertEqual(count_map(count_skills(df), "技能"), {"Python": 1, "RAG": 1})

    def test_missing_skill_column_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "技能"):
            count_skills(pd.DataFrame({"城市": ["深圳"]}))

    def test_unknown_city_returns_empty_table(self) -> None:
        result = count_skills(sample_jobs(), city="火星")
        self.assertTrue(result.empty)
        self.assertEqual(result.columns.tolist(), ["技能", "岗位数"])

    def test_two_jobs_with_same_dataframe_index_still_count_twice(self) -> None:
        df = pd.DataFrame({"城市": ["成都", "成都"], "技能": ["Python", "Python"]}, index=[7, 7])
        self.assertEqual(count_map(count_skills(df), "技能"), {"Python": 2})

    def test_skill_case_is_preserved_without_normalizing(self) -> None:
        df = pd.DataFrame({"城市": ["成都", "成都"], "技能": ["Python", "python"]})
        self.assertEqual(count_map(count_skills(df), "技能"), {"Python": 1, "python": 1})

    def test_original_dataframe_is_not_modified(self) -> None:
        df = sample_jobs()
        snapshot = df.copy(deep=True)
        result = count_skills(df)
        result.loc[0, "技能"] = "修改"
        pd.testing.assert_frame_equal(df, snapshot)


class ContractTests(unittest.TestCase):
    def test_non_dataframe_is_rejected(self) -> None:
        with self.assertRaises(TypeError):
            validate_input(["城市", "技能"], ("城市",))

    def test_empty_input_returns_structured_empty_results(self) -> None:
        df = pd.DataFrame(columns=["城市", "技能"])
        cities = count_jobs_by_city(df)
        skills = count_skills(df)
        self.assertTrue(cities.empty)
        self.assertTrue(skills.empty)
        self.assertEqual(cities.columns.tolist(), ["城市", "岗位数"])
        self.assertEqual(skills.columns.tolist(), ["技能", "岗位数"])


if __name__ == "__main__":
    unittest.main()
