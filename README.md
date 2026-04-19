# Knowledge Base

这是我的个人知识库，同时也是博客网站的内容来源仓库。使用 markdown 语法编写

## Repository Structure

这个仓库把路径当作 taxonomy。

- 每一层目录都表示一个更具体的主题范围。
- 路径表达的是“属于什么主题”。
- 文件名尽量简短，把大部分上下文交给目录路径表达。

例如：

- `ai/coding-agents/codex/codex-cli.md`
- `code/python/package/flask/basic.md`

## Directory README

除了 project root `README.md`，某些目录也有自己的 `README.md`。

它是这个目录的入口页，包含内容：

- 说明这个目录的主题范围
- 列出下面有哪些子主题或子目录
- 给出阅读入口或常见跳转路径
- 记录少量值得先知道的 observations, notes, or guiding ideas

如果一段内容明确属于某个分类，但暂时还不值得单独写成完整文章，可以先放在对应目录的 `README.md` 中，而不是硬拆成一篇独立文章。

## File Organization

目前的文章目录有两种格式

```
articles-dir/
├───resources/
│   ├───i18n/
│   │   └───example-en.md
│   └───images/
└───example.md
```

一般来说，文章目录下会有同级 `resources/` 文件夹，用于存放这篇文章的附属文件。

例如：

- `resources/images/` 用于存放图片
- `resources/i18n/` 用于存放主文档的翻译稿

有些文件夹如果只有图片的话，则是一个直接的 `images` 文件夹

## Special Directories

`.<folder-name>` 格式的目录不会出现在 Typora 的目录树中，`__<folder-name>__` 格式的目录会出现在 Typora 的目录树中。

这样可以把“需要看到的模板”和“只用于仓库运行的辅助目录”区分开。

### `__template__/`

根目录下的 `__template__/` 用来存放文章模板。

### `.githooks/`

`.githooks/` 用来存放这个仓库的 Git hooks。当前有一个 hook，会在 commit 前检查图片文件扩展名是否为大写；如果是，则自动改成小写。

### `.kb-tools/`

`.kb-tools/` 用来存放这个仓库的辅助工具。

目前翻译相关工具位于 `.kb-tools/translator/`。

如果要使用或修改翻译工具，请先阅读 `.kb-tools/translator/README.md`。

## Repository Setup

Enable case-sensitive paths on Windows:

```shell
git config core.ignorecase false
```

Configure Git hooks path:

```shell
git config core.hooksPath .githooks
```

需要保证命令行中可以正常运行：

```shell
python3 --version
```

## Website Sync

Push 到 `main` 时，这个仓库可以通过 GitHub Actions 触发 `website` 仓库的 content-sync workflow。

这个触发器只针对可能影响发布结果的内容变更，例如文章正文、翻译 sidecar、图片与资源文件；而 `README.md`、`AGENTS.md`、`.githooks/`、`.kb-tools/`、`__template__/` 等文档和工具目录改动，本身不会触发网站同步。
