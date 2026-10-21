## background

当我们在一个 git repo 中启动了一个 coding agent session，但是我们最后发现如果它需要去修改另外一个 git repo(有自己的 agents.md, readme.md) 的内容的时候。

我们应该如何让 agent 遵守另外一个 repo 的规则（README.md, AGENTS.md）呢？

是写一份 handoff.md, 然后在另外一个 repo 中启动 session 吗？

## 从第一性原理出发

一个 coding agent session，剥到最底层就三样东西：启动目录、加载的规则、对话记忆。而问题的根源可以用一句话说清：

> 规则是跟着 session 的启动位置加载的，但工作是跟着被修改的文件发生的。这两个锚点一旦分离，就有风险。（这句话需要修改一下，读取来有点怪，但是我能明白是什么意思）

session 锚在 A repo，工作发生在 B repo，于是 B repo 的规矩（AGETNS.md, README.md）有没有被遵守就取决于 agent 的临场发挥。

那么从原理上讲，规则到底应该跟谁走？我觉得可以借用法律里的一个概念：属地原则。出国旅行，遵守的是所在国的法律，而不是把本国法律随身携带到处适用。

所以：规则属于代码，不属于 session。谁的地盘，就守谁的规矩，无论你从哪里出发。

一旦确定这一条规则，我们就能够解决这个问题：

从哪里启动 session ？

> 只要改哪个仓库就加载哪个仓库的规则是有保障的，那么从 `projects/` 启动（视野广，适合跨仓库调查和排障）和从单个仓库启动（上下文精准，适合专注开发）都是安全的，你可以按当天的任务性质随便选，不需要立一个永久性的规矩。

## 如何落实这条规则？

将其写入 global agents.md

```markdown
## Cross-Repository Work

- Repository-specific rules follow the target repository, not the session: before planning or making changes in any Git repository, identify the target repository and read every applicable AGENTS.md from its root to the target path, plus the root README and relevant subsystem documentation, even when the session started elsewhere.
- When work spans repositories, state which repositories are affected and track each repository's Git state separately; when changes depend on one another, decide the order of changes and verification before modifying any of them.
```

