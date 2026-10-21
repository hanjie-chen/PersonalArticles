把探索过程交给 subagent，让 main session 留着 context windows 处理目标和判断。

# Subagent

我们使用 coding agent 时，有些中间步骤会产生很多的噪声。

例如，为了排查一个问题，可能需要翻日志、读文件、尝试几个不同的假设。最后真正有用的，可能只有一个简洁的结论，但整个探索过程却相当的耗费上下文。

这个时候，我们可以把这部分工作交给 subagent，让它完成任务，再把有用的结果带回来。main session 则继续负责目标、决策和最后的整合。

### when to use?

什么时候使用 subagent 呢？我倾向于把边界清晰、可以独立完成的工作交给 subagent。

例如，程序连接服务失败，需要分别检查配置、DNS 和代理。可以让 subagent 负责其中一项调查，再由 main session 综合判断。

但如果下一步做什么，必须依赖上一步的结果，拆开之后就要不断解释和同步，留在 main session 中可能更省事。

所以，只有分出去有收益的任务才使用 subagent，而不是每个任务都使用。

### what to bring back?

subagent 应该带回来什么结果？

如果让 subagent 调查代理是否导致连接失败，而它只回来一句：`是代理的问题`

main session 其实很难判断这个结论是否可靠。但如果把所有日志都贴回来，又失去了隔离过程信息的意义。

有用的回报可以很短：

`同一请求，直连成功，经过代理失败，重复测试结果一致。因此目前更怀疑代理链路。还没区分是节点问题还是本机代理配置问题。测试记录保存在 xxx，需要时可以继续检查。`

也就是：结论、关键证据，以及还没弄清楚的地方。

main session 不必读完整个探索过程，但需要知道判断从哪里来。

## Configure subagent

### enable subagent in codex/chatgpt

在 codex 中的系统提示词中，有一句类似的表述：除非 user, agents.md, skill 主动要求使用 subagent 否则就绝不使用。

所以为了开启 subagent 我一般在 [global AGENTS.md](https://github.com/hanjie-chen/personal-config/blob/main/codex/AGENTS.md) 中添加如下的 rule:

```markdown
## Subagents

- Use subagents for bounded, independent work when parallelism or context isolation would materially help, especially for noisy investigations and experiments; keep trivial or tightly coupled work in the main agent.
- Keep goals, decisions, and final synthesis in the main agent; require subagents to return concise evidence and conclusions.
- When a subagent completes its task, collect its result, then close its thread to release the slot; use a fresh subagent for unrelated work.
```

### custom subagent model

使用 subagent 可以节省 main session 的上下文，使得我们可以聊的更久一些。

但是 subagent 也需要读材料和完成工作，这个时候往往消耗的总的 token 会更多。

在 codex/chatgpt 中，如果什么都不设置，subagent 会继承 parent agent 的模型和 reasoning effort。也就是说主 agent 是 gpt-6-astra 的话，派三个 subagent 出去就是三个 astra 同时在跑。

$20 的订阅直接见底了。

但 subagent 干的活——读代码、找调用点、翻日志、跑实验——大多不需要主 agent 那个档位的能力。所以可以为 subagent 设置低一档的模型，主 agent 保持不动。

例如：

```toml
model = "gpt-6-astra"
model_reasoning_effort = "medium"

[agents]
default_subagent_model = "gpt-5.6-terra"
default_subagent_reasoning_effort = "medium"
```

这段配置让主 agent 使用 Astra，子 agent 默认使用 Terra Medium。

source: https://github.com/hanjie-chen/personal-config/blob/main/codex/config.shared.toml

### keep simple first

不过，子任务不一定简单。

找一个明确函数的位置，与调查一个难以复现的 bug，虽然都需要读代码，对模型的要求却不同。可以先把要求明确、结果容易检查的工作交给较便宜的模型，再观察效果。

如果经常需要主 agent 重做，省下的额度也可能花在返工上。

刚开始不用急着设计很多角色和模型档位。例如

```
主 agent（orchestrate / 判断 / 综合）
     ├── Terra Medium  → 分析 / debug / review
     └── Luna Low      → grep / search / scan
```

先用一个默认子 agent 模型，先进行实践和观察，看看效果先。