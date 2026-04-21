# Knowledge Base

这是我的个人知识库，也是博客网站的内容来源仓库。仓库中的内容主要使用 Markdown 编写，遵循路径即分类

## What This Repository Is

这个仓库主要承担两件事：

- 作为个人知识库，持续整理可复用的主题知识、经验和笔记
- 作为网站内容仓库，为博客或文档站点提供可发布的内容来源

## How To Navigate

这个仓库把路径当作文章的分类。

每一层目录都表示一个更具体的主题范围，从而把更多上下文交给目录路径表达，使得文件名尽量简短

例如：`ai/coding-agents/codex/codex-cli.md`

如果你是第一次进入这个仓库，通常可以从顶层主题目录开始，再顺着目录 `README.md` 往下阅读。

## Content Organization

除了本 `README.md`，部分目录也会有自己的 `README.md`。

它通常是该目录的入口页，用来：

- 列出下面有哪些子主题或子目录
- 记录少量值得先知道的 notes 或 guiding ideas

在命名上，尽量让目录承载主题语义，让文件名保持简短。

## Article Layout

文章目录通常会把正文和附属资源放在一起管理。常见形式如下：

```text
articles-dir/
├── example-1.md
├── example-2.md
└── resources/
    ├── images/
    └── i18n/
        ├── example-1-en.md
        └── example-2-en.md
```

一般来说：

- `resources/images/` 用于存放与文章对应的图片等资源文件
- `resources/i18n/` 用于存放主文档的翻译 sidecar

有些目录如果只有图片资源，也可能直接使用 `images/`，不一定强制引入完整的 `resources/` 结构。重点是让文章与其附属资源保持清晰、稳定、容易定位的关系。

## Special Directories

这个仓库里有一些特殊目录（用于模板、工具和维护）

`__template__/` 用于存放文章模板或内容骨架。

`.githooks/` 用于存放这个仓库的 Git hooks。

`.kb-tools/` 用于存放这个仓库的辅助工具和脚本。如果要使用或修改其中的工具，请优先阅读对应子目录下的 `README.md`。

## Repository Setup

如果你要在本地维护这个仓库，建议先完成以下最小配置。

Enable case-sensitive paths on Windows:

```shell
git config core.ignorecase false
```

Configure Git hooks path:

```shell
git config core.hooksPath .githooks
```

同时需要保证命令行中可以正常运行：

```shell
python3 --version
codex exec # .kb-tools/translator 使用
```

## Publishing

Push 到 `main` 的内容变更会触发网站内容同步。具体规则见 `.kb-tools/website_sync/` 和 `.github/workflows/`。
