"""Minimal Streamlit UI: upload -> validate -> select -> submit -> display."""

from __future__ import annotations

from analysis_service import available_cities, compute_statistics, prepare_jobs


ALL_CITIES_LABEL = "全部城市"


def render_page(st) -> None:
    """Render interactions without duplicating the P02/P03 business logic."""
    st.title("招聘岗位技能分析")
    st.caption("上传 CSV、选择城市，最后点击“开始分析”统一提交。")

    source = st.file_uploader("上传招聘 CSV 文件", type=["csv"])
    if source is None:
        st.info("请先上传招聘 CSV 文件。")
        return

    try:
        cleaned = prepare_jobs(source)
    except (TypeError, ValueError) as exc:
        st.error(f"输入数据错误：{exc}")
        return

    if cleaned.empty:
        st.warning("CSV 没有符合清洗规则的岗位记录，无法生成统计结果。")
        return

    choices = [ALL_CITIES_LABEL, *available_cities(cleaned)]
    with st.form("analysis_form", enter_to_submit=False):
        selected_city = st.selectbox("选择城市", choices)
        submitted = st.form_submit_button("开始分析")

    if not submitted:
        st.caption("选好城市后，点击“开始分析”查看结果。")
        return

    try:
        city = None if selected_city == ALL_CITIES_LABEL else selected_city
        city_counts, skill_counts = compute_statistics(cleaned, city)
    except (TypeError, ValueError) as exc:
        st.error(f"统计失败：{exc}")
        return

    st.subheader("各城市岗位数量")
    st.dataframe(city_counts, hide_index=True)
    st.subheader(f"{selected_city}的技能需求")
    if skill_counts.empty:
        st.info("该范围内没有有效的技能记录。")
    else:
        st.dataframe(skill_counts, hide_index=True)


def main() -> None:
    import streamlit as st

    st.set_page_config(page_title="招聘岗位技能分析", layout="centered")
    render_page(st)


if __name__ == "__main__":
    main()
