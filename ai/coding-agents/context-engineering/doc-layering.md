在我们使用 coding agent 的时候，我们应该如何让 AI 理解一个复杂的 project，然后按照我们的协作规定上手修改？

其实问题可以分成两部分：

1. 让 AI 读懂项目
2. 让 AI 知道如何修改

## Understand the project

为了让 AI 更快读懂项目，我目前觉得最有效的方法，是把文档分成三个层次：

- project root README.md
- sub-folder README.md
- project root docs/

### project root README.md

> project root README.md 后续简写为 README(root)

在我们的设计中 project root AGENTS.md 的第一个条目，永远都是 [read first](https://github.com/hanjie-chen/personal-config/blob/main/codex/AGENTS.code.example.md):

```markdown
## Read First

Start with the root `README.md`. Before planning or making non-trivial changes in a subsystem, read its nearest `README.md` and any `AGENTS.md` files on the path from the repository root to the target files.
```

这一条 rule 意味着 README(root) 一定会被阅读，甚至被 ai 反复阅读。根据这一点可以推导出：它应该优先包含稳定的信息。

而于此同时，这个文件，也是我进入项目的入口（虽然是自己的项目，但是总会遗忘某些部分）

所以，我们的 README(root) 怎么写，非常的重要，因为这个文件即是人的入口，也是 ai 的入口

我们的标准是：无论接下来要修改哪个模块，阅读这份文件对读者有帮助吗？

按照这个标准，README(root) 至少需要回答三个问题：

1. 开头：这是什么项目？（项目简介）
2. 代码在哪里？（仓库 ）
3. 如何运行这个仓库中的代码？

还有一些可选的内容：

1. 项目的总体架构图 / network traffic flow 等

### sub-folder README.md

对于那些本身拥有独立子系统逻辑的目录，我们可以在目录下单独放一份 README.md，用来解释：

- 这个子系统的职责是什么
- 入口文件在哪里
- 关键文件分别做什么
- 常见改动通常落在哪些文件上

如果把这些内容都堆到 project root README.md 里，根 README 很快就会膨胀；把说明下沉到各自目录，可以让根 README 保持轻量。

代价也很明显：当目录结构或子系统逻辑变化时，对应的 sub-folder README.md 也要一起维护。

同时这里的 README.md 主要是给 ai 读和维护的，所以最好和代码对齐使用纯英文。

### project root docs/

当一份文档同时跨越多个目录，或者本身就是较长的专题说明时，更适合放到 docs/ 目录里。

比如：

1. 跨多个子系统的架构文档
2. 线上故障排查 runbook
3. 设计决策记录（ADR）

## Modify the project

当我们解决了“让 AI 读懂 project”这个问题之后，下一步就是让 AI 知道该如何安全地修改它。

这时就需要另一类文档：agent instruction file，比如 Codex 使用 AGENTS.md，Claude Code 使用 CLAUDE.md。接下来我们以 AGENTS.md 为例。

AGENTS.md 和 README.md 的区分：

- README.md：这是什么项目，怎么跑，结构大概怎样
- AGENTS.md：如果现在要动这个仓库，应该先看哪里、遵守什么约束、不要踩哪些坑，也就是行动指南。

而 AGENTS.md 也分为三层

- global AGENTS.md
- project root AGENTS.md
- sub-floder AGENTS.md

### global AGENTS.md

通用协作偏好，跨仓库都成立。

### project root AGENTS.md

这个 repo 的跨子系统规则。

### sub-folder AGENTS.md

只放该目录独有的约束；行为说明优先放 README.md，流程约束才放 AGENTS.md。