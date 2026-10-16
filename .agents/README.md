# Codex 项目技能

`.agents/skills/` 中安装三个实体现成目录，供在本仓库中启动的 Codex 发现：

- `punk-cover/`
- `punk-avatar/`
- `punk-ip-video-cover/`

每个目录完整复制对应 `skills/{name}/`，包括原文 `SKILL.md`、`agents/`、`references/`、内部风格与许可文件。原始 `skills/` 和根目录 `styles/` 仍是唯一维护来源；安装副本不单独编辑设计规则。

`.agents/styles/` 是根目录 `styles/` 的完整实体副本，使封面与头像技能中原有的 `../../styles/{style-id}/...` 路径继续有效。风格目录中以 `styles/...` 表示的仓库级资源，在安装布局下对应 `.agents/styles/...`。视频封面的内部 `styles/`、相对于文件的 Markdown 链接与许可文件保持原有布局。

## 完整性检查与维护

从仓库根目录运行（Python 3.9+，安装 PyYAML）：

```sh
python scripts/validate-codex-install.py
node scripts/validate-punk-cover.mjs
node scripts/validate-punk-avatar.mjs
git diff --check
```

验证器比较文件清单与 SHA-256，拒绝符号链接或不同步副本，检查技能 YAML 必要字段、Agent 配置及本地资源路径。修改原始技能或风格后，需重新完整复制相应目录到 `.agents/`，然后运行检查；新增资源不会自动同步。

请保留完整仓库布局，或整体保留 `.agents/skills/` 与 `.agents/styles/` 的相对层级；不要单独复制一个依赖共用风格库的技能目录。安装布局不依赖符号链接支持。项目输出仍遵循原技能规则，保存在当前工作目录的 `punk-assets/` 下。

安装后应在本仓库目录重新启动 Codex 工作阶段，再检查原生技能清单。本验证器验证静态安装结构，不保证现有工作阶段会即时重新扫描，也不代替宿主的技能加载验证。
