# GitHub 发布前检查表

当前交付的是**准备发布的源码包**，不是已经发布的 GitHub 仓库。

## 已由开发窗口完成

- [x] 原有 P02/P03 业务模块保留并复用。
- [x] CSV 示例、无效 CSV 示例、README、测试、Windows BAT 和 uv 锁文件齐全。
- [x] Windows 用户示例数据验收证据已记录。
- [x] GitHub 自动化测试配置已加入（实际远程运行待验证）。
- [x] `.gitignore` 排除本地 `.venv`、字节码和敏感 Streamlit secrets。

## 发布前由项目所有者决定

- [ ] 仓库名称与公开/私人可见性。建议仓库名 `job-skill-analyzer`。
- [ ] 是否选择开源许可证；这会影响其他人能否合法复制和分发。
- [ ] 是否自行添加项目页面截图；发布前检查截图不含个人路径、账号或私密数据。
- [ ] 如果公开发布，确认示例 CSV 是非真实隐私数据，且 README 不夸大能力。

## 推荐的 VS Code 发布流程

1. 解压 ZIP，使用 VS Code 打开 `job-skill-analyzer` 文件夹。
2. 在“源代码管理”中初始化仓库；确认 `.venv` 未出现在待提交文件列表。
3. 在 VS Code 中提交当前源码，提交信息可写 `Initial job skill analyzer`。
4. 使用 VS Code 提供的“Publish to GitHub”功能，确认仓库名称和可见性后再发布。
5. 打开 GitHub 的 Actions 页面，查看 Linux/Windows 测试是否真正通过。此步骤完成前不要将 CI 状态写成通过。

GitHub 仓库提交和公开发布尚未执行；若授权能够直接操作你的 GitHub 仓库，可进一步自动处理这些机械性步骤。
