# claude-code

下载 claude code

[Quickstart - Claude Code Docs](https://code.claude.com/docs/en/quickstart)

windows 上面只需要一行代码

```powershell
irm https://claude.ai/install.ps1 | iex
```

# command

/model: 切换模型和思考强度



## CLAUDE.md

一个好的 claude.md 需要包含这些内容

 1. 项目一句话简介 — 让cc秒懂这是什么
  2. 目录结构 + 每个文件夹的用途 — 让cc需要找什么就去哪里，不用乱翻
  3. 关键设定文件索引 — 按需读取
  4. 当前进度 — 做到那里，现在在解决什么问题

# claude code 配置

claude code 模型权限、默认模式、项目规则、hooks、sandbox 等正式配置主要放在 `settings.json`，

而 per-project state（包括 allowed tools、trust settings） 放在 `~/.claude.json`。

如果你想手动配 Claude Code，主要看这三层：

- 用户级：`~/.claude/settings.json`，对所有项目生效
- 项目级：`<repo>/.claude/settings.json`，会随 git 分享给团队
- 本地项目级：`<repo>/.claude/settings.local.json`，只在你本机这个仓库生效，且会被 git ignore

优先级是 Local > Project > User。

