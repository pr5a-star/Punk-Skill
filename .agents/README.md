# Codex 项目技能

在此仓库中启动 Codex 时，从 `.agents/skills/` 发现以下三个项目技能：

- `punk-cover` → `../../skills/punk-cover`
- `punk-avatar` → `../../skills/punk-avatar`
- `punk-ip-video-cover` → `../../skills/punk-ip-video-cover`

这些目录是 Git 跟踪的相对符号链接，原始 `skills/` 是唯一维护来源；不复制或修改技能设计规则。各技能的 `SKILL.md`、`agents/`、`references/`、内部风格与许可文件均沿用原目录，后续新增资源也自动可用。

`.agents/styles` → `../styles` 保留共用风格路径的兼容性：即使读取工具先按 `.agents/skills/{name}` 对 `../../styles/` 做路径规范化，也能读取根目录的同一份风格库。直接解析技能符号链接时则继续使用原始路径。`punk-ip-video-cover` 的内部 `styles/` 不受影响。

请完整克隆仓库并保留 Git 符号链接（`core.symlinks=true`，系统须支持符号链接），不要只复制 `.agents/`。项目输出仍按原技能规则保存在当前工作目录的 `punk-assets/` 下。
