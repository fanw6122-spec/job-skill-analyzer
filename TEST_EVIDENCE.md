# W01-P03-P2 — 测试与交付证据

## 开发方式

1. 从用户已验收的 P02-P1 与 P03-P1 ZIP 取回正式练习源码。
2. 先编写 12 项集成及界面测试；未实现时，`analysis_service` 导入失败（预期 RED）。
3. 新增 `analysis_service.py`、`streamlit_app.py`；只扩展 P02 CSV 读取函数的参数类型提示，使其说明支持文件流，其他 P02/P03 核心逻辑未改。
4. 再次执行旧、新自动化测试（GREEN）。

## 本开发环境实测

- 环境：Linux / CPython 3.12.14 / `uv` / 项目独立 `.venv`。
- 依赖：`pandas==2.2.3`、`streamlit==1.55.0`，由本项目 `uv.lock` 固定。
- `uv run --no-sync python -m unittest discover -s tests -v`：**40 项通过，0 失败**。
  - P02 既有测试：12 项。
  - P03-P1 既有测试：16 项。
  - P03-P2 新增集成测试：6 项。
  - P03-P2 新增页面逻辑测试：6 项。
- `uv run --no-sync python demo.py`：**通过**。
  - 示例 CSV 原始 8 条，清洗后 4 条。
  - 城市统计：深圳 2、成都 1、重庆 1。
  - 深圳技能：Python 2、Agent 1。
- `uv run --no-sync python smoke_test_streamlit.py`：**通过**。
  - 真实 Streamlit `AppTest` 执行页面脚本（未上传状态）未出现异常。
  - 启动本地 HTTP 服务器，健康检查端点返回 HTTP 200。

## 证据边界

- 页面输入、提交、结果显示等业务交互通过受控假 UI 执行单元测试；非真实人工点击。
- Streamlit AppTest 覆盖无上传的初始页面执行及真实框架调用；HTTP 健康检查验证服务能够启动。
- **Windows 实际验收已完成（2026-11-09）：**用户提供了 Windows CPython 3.12.13 + uv 项目本地 `.venv` 的运行日志，显示 40 项测试全部通过，CLI 演示通过、Streamlit 脚本检查通过、本地 HTTP 健康检查通过。
- 用户另提供了两张浏览器页面截图，确认上传 `sample_jobs.csv`、选择“深圳”，并显示全体城市岗位数量（深圳 2、成都 1、重庆 1）与深圳技能数量（Python 2、Agent 1），与测试预期一致。
- 图片仅作为当前验收对话中的证据，不在本发布包中附带截图或用户本地路径。
- Windows 浏览器已验证示例流程，**尚未验证大规模真实招聘数据、所有 CSV 编码与异常输入的人工界面操作**。
- `.github/workflows/tests.yml` 仅新增配置，尚无实际 GitHub 工作流运行结果。
