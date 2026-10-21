## Before we beginning

为什么我们需要管理 agnets 的上下文？

因为目前的 llm 的 ctx 非常的有限，所以我们尽量要让正确的上下文进入 sesion，也就是让 agent 的注意力放在我们需要它关注的地方，说白了，就是不要让太多的无关信息淹没模型的注意力。

比如说下面的情况：

> 这里要举一个我自己的例子出来

我们应该只给 Agent 完成当前任务所需的精确信息，不多不少！对这一点控制得越好，Agent 的表现就越好。

## Context Engineering

当我们和一个 agent 协作的时候，往往是在一个 session 中展开的，但是 session 的上下文会随会话消失，repo 里的东西会留下来。

context engineering 就是管理这两者之间的信息流动。

做个比喻来说的话，类似于干木工：

- 开工前，从仓库把需要的图纸和材料搬上工作台 → 入口
- 干活时，台面就这么大，锯末刨花别堆上去 → 运行中
- 收工前，成品和半成品必须归位，因为台面明早会被清空 → 出口

分成三个方向：

### 入口：repo → session

让 agent 用最少的 token 建立对 repo 的正确认知。

- 文档分层（README 三层 + AGENTS 三层 + docs/ ）→ doc-layering.md
- 规则跟着目标仓库走 → cross-git-repo-in-one-session.md

### 运行中：session 内部上下文控制

防止中间产物污染 main session 的上下文。

- subagent：验证性的试验、网络的调查、log 的过滤和分析等，留在 subagent，只回来一个结论 → subagent.md

- skill：把重复摸索固化，避免每次都用 token 重新试错 → skill.md

### 出口：session → repo

会话中产生的状态，必须在 session 结束前落盘。

- commit：代码
- decisions.md：已经想清楚的结论
- handoff.md：还没成型、没有归宿的半成品 → handoff.md

这三件事做得越彻底，session 就越可以随手丢弃——理想状态是 `/clear` 之后， agent 靠 repo 自己就能恢复

## Reference

claude 官方博客发布的这一篇文章

[Maximizing the value of your Claude Code sessions | Claude by Anthropic](https://claude.com/blog/maximizing-the-value-of-your-claude-code-sessions)

以及这一篇x.com 上面的文章

https://x.com/systematicls/status/2028814227004395561

