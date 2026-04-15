# claude code memory Mechanism

claude code memory 是两套并行系统。

1. CLAUDE.md（你自己写的），用来放项目指令、编码规范、架构说明等。它有一整套层级结构——从组织级（managed policy）到用户级（`~/.claude/CLAUDE.md`）到项目级（`./CLAUDE.md`）再到本地个人级（`./CLAUDE.local.md`），启动时沿目录树向上逐级加载并拼接。还支持 `@path/to/file` 语法引入外部文件，以及 `.claude/rules/` 目录做按路径触发的条件规则。
2. Auto Memory（Claude 自己写的）

## Auto Memory

这是项目级别的的 memory

关于加载上限，MEMORY.md 的前 200 行或前 25KB，取先到者。

关于存储位置，每个项目的 auto memory 存在 `~/.claude/projects/<project>/memory/` 下，同一个 git 仓库的所有 worktree 和子目录共享同一个 memory 目录

第一层：MEMORY.md 索引 — 始终加载

每次对话开始时，MEMORY.md 的内容会自动注入到 context 中。可以在系统消息里看到它实际上已经被加载了：

第二层：具体记忆文件 — 按需读取

像 feedback_search_before_answer.md 这样的详细内容，不会自动加载。

只有当模型判断某条记忆和当前对话相关时，才会用 Read 工具去读取它。

