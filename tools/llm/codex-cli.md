# codex cli使用指南

下载 codex cli

```shell
npm i -g @openai/codex
# macos download
brew install codex
```

> [!note]
>
> 在用 npm 命令安装时需要注意全局 prefix 最好放到用户目下，而不是系统目录下，详见 [npm-guide](../npm/npm.md)

验证

```shell
which codex
codex --version
```

登录

```shell
# 查看登录状态
codex login status
# 打开网页登录
codex login
```



## AGENTS.md

Codex 会在每次启动时自动读取并合并一条“指令链”：

- 全局：`~/.codex/AGENTS.md`
- 项目：从 repo root（通常是 Git root）一路走到当前工作目录，每层目录最多取一个 `AGENTS.md`，并按“root → leaf”顺序依次注入。 

作用：把你每次都要重复说的“工作协议/目录说明/输出格式”固化下来。

## interactive mode

使用命令 `codex` 直接进入交互模式

<img src="./images/interactive-mode.png" alt="interactive mode" style="zoom:50%;" />

使用 `/` 可以设定和查看某些内容，比如说选择模型

<img src="./images/select.png" alt="codex cli select" style="zoom:50%;" />

实际上的命令不仅仅是上线显示的这些，比较常用的命令有

status

<img src="./images/status.png" alt="status" style="zoom:50%;" />

如果我们需要开启一段新对话，那么我们可以使用

- `/clear`：清屏 + 开新对话（从头开始聊）。
