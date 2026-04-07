# superpowers

source: [obra/superpowers: An agentic skills framework & software development methodology that works.](https://github.com/obra/superpowers)

superpowers = 给 coding agent 用的一套“开发工作流系统”。

普通 coding agent 往往会一上来就直接改代码，而 superpowers 想让 agent 先做对流程，再做对代码。

默认推的路线是：先澄清需求/设计 → 再写实施计划 → 再实现 → 中间做测试和 review → 最后收尾验证。

## download

对于 codex 来说，使用这句话

```text
Fetch and follow instructions from https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/.codex/INSTALL.md
```

Codex 启动时会扫描 `~/.agents/skills/`，读取 skill 的说明，然后在对话中按需触发。`using-superpowers` 这个总控 skill 会被自动发现，并负责把其他 skill 带起来。

## 它到底是什么

仓库里有一整套 skill，包括一个顶层 using-superpowers 作为总入口和使用指南。它的作用不是直接干活，而是在任何任务开始前先检查有没有合适 skill ，提醒该不该用别的 skill，帮助路由到正确 skill

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

## 如何使用它

### 用法一：显式点名

最稳，最适合刚开始学习。可以直接说：

```text
Use brainstorming to refine this feature idea first.
Use systematic debugging to investigate this bug.
Use writing-plans before implementation.
Use test-driven-development for this change.
```

这种方式的好处是：你能清楚地看到“这个 skill 到底在干嘛”。

### 用法二：用自然任务语言触发

这是以后更自然的用法。比如你说：

```text
Help me plan this feature before coding.
Let's debug this issue systematically.
Please create a step-by-step implementation plan.
Let's work in a separate worktree for this feature.
```

# Learn superpowers

对于日常使用，或者刚开始使用时，先依赖“自动触发”（using-powershell skill），了解一下 4 个最常用的 skill 

遇到重要任务时，再主动点名让它用某个 skill，这样更容易观察和学习这个 skill 的边界和风格。

用久了以后，再慢慢熟悉更多 skill

## basic skills

刚开始的时候学习的时候，我们只需要认识这里 4 个常用 skill

- brainstorming 适合需求还不清楚、方案还没定、要一起设计，它的重点不是写代码，而是通过提问把你的想法收敛成一个更清楚的设计。
- writing-plans 这个非常重要。它负责把已经批准的设计拆成一小步一小步的实现任务。它会把工作拆成很小的 task，并带上文件路径、代码、验证步骤。
- systematic-debugging 适合排查 bug、定位根因，不想靠猜。
- test-driven-development 适合要比较严谨地新增/修改功能，它会强制 agent 走 RED-GREEN-REFACTOR，而不是先写一坨实现再补测试。

平时就用下面这个心法：

- 不确定需求：先说 `用 brainstorming`
- 准备动手：说 `先写 plan`
- 遇到 bug：说 `用 systematic-debugging`
- 要严谨实现：说 `按 TDD 来`

一个很实用的原则：如果任务会花 10 分钟以上，或者改动有风险，就主动点名 skill。如果只是小改文案、小修模板、小问题解释，可以先让我自动判断。
