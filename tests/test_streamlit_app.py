"""Test the Streamlit page at its UI boundary without a real browser."""

from __future__ import annotations

import io
import unittest
from unittest.mock import patch

import streamlit_app


SAMPLE = (
    "岗位编号,城市,岗位名称,技能\n"
    "001,深圳,工程师,Python;RAG;Python\n"
    "002,成都,分析师,RAG\n"
    "003,深圳,开发工程师,Python\n"
)


class FakePage:
    def __init__(self, upload: io.BytesIO | None, *, chosen_city: str = "深圳", submit: bool = False):
        self.upload = upload
        self.chosen_city = chosen_city
        self.submit = submit
        self.messages: list[tuple[str, str]] = []
        self.tables = []
        self.options = []
        self.form_parameters = {}

    def title(self, value):
        self.messages.append(("title", value))

    def caption(self, value):
        self.messages.append(("caption", value))

    def info(self, value):
        self.messages.append(("info", value))

    def error(self, value):
        self.messages.append(("error", value))

    def warning(self, value):
        self.messages.append(("warning", value))

    def subheader(self, value):
        self.messages.append(("subheader", value))

    def file_uploader(self, label, **kwargs):
        self.asserted_upload_type = kwargs.get("type")
        return self.upload

    def form(self, key, **kwargs):
        self.form_parameters = {"key": key, **kwargs}
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def selectbox(self, label, options):
        self.options = list(options)
        return self.chosen_city

    def form_submit_button(self, label, **kwargs):
        return self.submit

    def dataframe(self, value, **kwargs):
        self.tables.append(value.copy())


def uploaded(text: str) -> io.BytesIO:
    return io.BytesIO(text.encode("utf-8-sig"))


class StreamlitPageTests(unittest.TestCase):
    def test_no_upload_prompts_without_running_statistics(self) -> None:
        ui = FakePage(None)
        with patch.object(streamlit_app, "compute_statistics") as compute:
            streamlit_app.render_page(ui)
            compute.assert_not_called()
        self.assertEqual(ui.tables, [])
        self.assertIn("info", [kind for kind, _ in ui.messages])

    def test_selecting_city_before_submit_does_not_run_statistics(self) -> None:
        ui = FakePage(uploaded(SAMPLE), submit=False)
        with patch.object(streamlit_app, "compute_statistics") as compute:
            streamlit_app.render_page(ui)
            compute.assert_not_called()
        self.assertEqual(ui.tables, [])
        self.assertEqual(ui.options, ["全部城市", "成都", "深圳"])
        self.assertEqual(ui.form_parameters["enter_to_submit"], False)

    def test_submitting_shenzhen_displays_two_real_statistic_tables(self) -> None:
        ui = FakePage(uploaded(SAMPLE), chosen_city="深圳", submit=True)
        streamlit_app.render_page(ui)
        self.assertEqual(len(ui.tables), 2)
        city_counts, skill_counts = ui.tables
        self.assertEqual(dict(zip(city_counts["城市"], city_counts["岗位数"])), {"深圳": 2, "成都": 1})
        self.assertEqual(dict(zip(skill_counts["技能"], skill_counts["岗位数"])), {"Python": 2, "RAG": 1})

    def test_submitting_all_cities_includes_all_jobs(self) -> None:
        ui = FakePage(uploaded(SAMPLE), chosen_city="全部城市", submit=True)
        streamlit_app.render_page(ui)
        self.assertEqual(dict(zip(ui.tables[1]["技能"], ui.tables[1]["岗位数"])), {"Python": 2, "RAG": 2})

    def test_missing_required_column_shows_error_and_no_statistics(self) -> None:
        ui = FakePage(uploaded("岗位编号,岗位名称,技能\n001,工程师,Python\n"), submit=True)
        with patch.object(streamlit_app, "compute_statistics") as compute:
            streamlit_app.render_page(ui)
            compute.assert_not_called()
        self.assertIn("error", [kind for kind, _ in ui.messages])
        self.assertEqual(ui.tables, [])

    def test_empty_csv_shows_clear_error(self) -> None:
        ui = FakePage(uploaded(""), submit=True)
        streamlit_app.render_page(ui)
        self.assertIn("error", [kind for kind, _ in ui.messages])
        self.assertEqual(ui.tables, [])


if __name__ == "__main__":
    unittest.main()
