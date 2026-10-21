# Knowledge Base

写给我自己看的笔记。

更多包含自己的思考和实践的整理，而不是完整的教程，因为通用的知识不会时直接问 AI 就行了，更快，更方便。

所有笔记（包括草稿）都会同步到我的[个人网站](https://hanjie-chen.com/)。

## Navigation

原则：路径即分类。

每一级目录都表示更具体的主题。内容的分类只由路径表达，文件名保留路径尚未提供的信息；移动文件即重新分类，不额外维护分类信息。例如：`tools/git/commands.md`。

目录树是人和 AI agent 共用的导航入口。当前的顶层主题目录：

- `ai/` — AI 相关：LLM、coding agents、自动化平台
- `cloud-infra/` — 云平台（Azure / GCP / Cloudflare）与 IaC（Terraform / Ansible）
- `code/` — 编程语言、算法与工程实践
- `devops/` — Docker、Kubernetes 等
- `machine-setup/` — 个人机器配置：Windows / Linux / 网络
- `personal-growth/` — 非技术类：生活经验、理财、世界观
- `tools/` — 日常工具指南：Vim、PowerShell、PowerToys 等
- `web-dev/` — Web 开发：前端、后端、安全

部分目录包含自己的 `README.md`，作为该目录的入口，用于介绍子主题以及需要了解的 notes 或 guiding ideas。首次浏览时，可以先选择一个顶层主题，再沿目录中的 `README.md` 继续阅读。

## Content Resources

草稿只有图片资源时，可以直接使用 `images/`，不必预先创建完整的资源结构。

整理好的笔记统一使用以下结构：

```text
content-dir/
├── example-1.md
├── example-2.md
└── resources/
    └── images/
```

- `resources/images/` 存放正文使用的图片等资源

## Special Directories

- `__template__/` — 笔记模板；写笔记时参考 `note.md` 的格式，它也用来测试 Markdown 渲染效果
- `.githooks/` — 存放仓库管理的 Git hooks

## Setup

配置仓库的 Git hooks：

```shell
git config core.hooksPath .githooks
```

验证配置：

```shell
git config --get core.hooksPath
```

在 Windows 上，让 Git 区分路径大小写：

```shell
git config core.ignorecase false
```

Git hooks 依赖 Python 3。确保以下命令可以正常运行：

```shell
python3 --version
```

## Publishing

每次 push 到 `main`，GitHub Actions 都会通知 [website](https://github.com/hanjie-chen/website) 执行内容同步；哪些文件算笔记由 website 决定。workflow 说明见 [GitHub workflows README](.github/workflows/README.md)。
