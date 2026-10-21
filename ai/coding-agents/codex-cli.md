# codex 使用指南

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

### AGENTS.md

Codex 会在每次启动时自动读取并合并一条“指令链”：

- 全局：`~/.codex/AGENTS.md`
- 项目：从 repo root（通常是 Git root）一路走到当前工作目录，每层目录最多取一个 `AGENTS.md`，并按“root → leaf”顺序依次注入。 

作用：把你每次都要重复说的“工作协议/目录说明/输出格式”固化下来。

## codex exec

codex exec 命令是 Codex CLI 的非交互模式。

适合脚本化的运行：给它一个 prompt，它执行任务并结束，而不是像直接运行 `codex` 那样进入一个持续对话的终端界面。

也就是说：

- `codex` = 交互式会话/TUI。
- `codex exec "任务"` = 一次性 agent 任务。跑完就退出

而且可以把多个 `codex exec` 当成多个独立任务去启动。 

每次 `codex exec` 都是一个独立的非交互 session：它可以持久化 session，支持 `codex exec resume [SESSION_ID]` 继续某个 exec 会话；
