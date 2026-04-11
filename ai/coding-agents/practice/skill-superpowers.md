# superpowers

source: [obra/superpowers: An agentic skills framework & software development methodology that works.](https://github.com/obra/superpowers)

superpowers = 给 coding agent 用的一套“开发工作流系统”。

普通 coding agent 往往会一上来就直接改代码，而 superpowers 想让 agent 先做对流程，再做对代码。

默认是：澄清需求/设计 → 写实施计划 → 实现 → 做测试和 review → 收尾验证。

## 它到底是什么

superpowers 里有一整套 skill，包括一个顶层 using-superpowers 作为总入口和使用指南。

> [!note]
>
> 它的作用不是直接干活，而是在任务开始前先检查有没有合适 skill ，提醒该不该用别的 skill，帮助路由到正确 skill

其他的 skill 分别对应设计、计划、调试、测试、评审、分支收尾等具体环节，可以将它们划分为看成三层：

### A. 思考层

- Brainstorming
- Writing Plans

### B. 执行层

- Executing Plans
- Subagent Driven Development
- Test Driven Development
- Using Git Worktrees

### C. 质量层

- Systematic Debugging
- Requesting Code Review
- Verification Before Completion
- Finishing A Development Branch

## download

在 github 仓库中，可以看到下载方式，对于 codex 来说，使用这句话

```text
Fetch and follow instructions from https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/.codex/INSTALL.md
```

Codex 启动时会扫描 `~/.agents/skills/`，读取 skill 的说明，然后在对话中按需触发。`using-superpowers` 这个总控 skill 会被自动发现，并负责把其他 skill 带起来。

# Learn superpowers

对于日常使用时，我们可以直接依赖自动触发（using-superpowers）

刚开始的时候，我们只需要了解一下 4 个最常用的 skill 

遇到重要任务时，再主动点名让它用某个 skill，这样更容易观察和学习这个 skill 的边界和风格。

用久了以后，再慢慢熟悉更多 skill

## 4 basic skills

刚开始的时候学习的时候，我们只需要认识这里 4 个常用 skill

- brainstorming 适合需求还不清楚、方案还没定、要一起设计，它的重点不是写代码，而是通过提问把你的想法收敛成一个更清楚的设计。
- writing-plans 这个非常重要。它负责把已经批准的设计拆成一小步一小步的实现任务。它会把工作拆成很小的 task，并带上文件路径、代码、验证步骤。
- systematic-debugging 适合排查 bug、定位根因，不想靠猜。
- test-driven-development 适合要比较严谨地新增/修改功能，它会强制 agent 走 RED-GREEN-REFACTOR，而不是先写一坨实现再补测试。

# Personal usage notes

## subagent-drive

当写完 plan 开始使用 Subagent-Driven 的时候，最好关闭 codex 的 fast mode(1.5 speed, 2 times usage) 不然很容易就把这个 5 hours limits 给消耗完。

> [!note]
>
> 像 `dispatching-parallel-agents` 和 `subagent-driven-development` 这类 skill，需要在 Codex 配置里开启 `multi_agent = true`

关于页面上小的改动，就不要开启 subagent-drive 模式，也不需要写什么 plan, 因为这里及其消耗额度和 token

原因是，他的 code review 会新开一个 subagent 来做，而主进程则是一个 manager 的类似职责



