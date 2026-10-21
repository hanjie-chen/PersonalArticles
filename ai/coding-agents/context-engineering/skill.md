# Skill

核心：把重复的工作流程化

例如，要使用 github, 读取 PR, review 代码，那么 github 相关的 mcp 和 skill 就是必备的

如果没有这些 skill, 那么模型就会花费大量的上下文来寻找最终能够解决的方案，浪费 token 和 conext windows, 为了避免重复错误的尝试才需要 skill

## rule

随着 agent 能力越来越强，skills 需要遵循一个原则，less is more

越少的 skill 越好

当你的 skill 越来越多，就意味着你的上下文被占用的越多。如果一个 skill 可以帮你解决特定的问题。

### 为什么 skill 越少越好

因为现在的模型 agent 能力越来越强了，

我之前使用过 superpowers 使用 codex 配合 gpt-5.4, gpt-5.5 效果感觉不错，虽然有点耗费额度，但是代码效果很好。

但是当 openai 更新到了 gpt-5.6-sol 的时候，我尝试不使用 superpowers 结果发现，代码质量依旧很好，而且耗费的额度还变少了。

想想也是，像 openai, anthropic 这样子的公司，不仅自己的员工在大量的使用 agent，而且可以看到哪些 skills 被大量的使用，那么为啥他们不直接把这些skill炼化到模型中呢？

不仅如此，甚至还有很多关于 coding agent 的插件、使用技巧、解决方案，都会被这些公司一一手编到他们自己的产品中去，而且速度极快。

所以我们根本不需要额外安装任何东西，只需要使用这些基础模型公司原生的产品即可。

所以，每当基础模型公司做一次大规模的更新的时候，我们都要重新思考一下应该如何与 coding agent 协作，看看 global agents.md, skills 等上下文是否要做一些优化，以免旧的内容降低效率



## Reference

https://x.com/systematicls/status/2028814227004395561
