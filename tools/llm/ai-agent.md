# ai-agent

AI agent 一般指：模型不只会聊天，还能调用工具并执行动作（读文件、改代码、跑命令、循环迭代到完成目标）。



## agents.md

可以把 AGENTS.md 理解成：“写给 AI coding agent 看的项目说明书 / 工作规约”。

以 codex 为例它会在开始干活前先读取 `AGENTS.md`，把里面的内容当成任务上下文的一部分。所以它的作用不是给人类读文档本身，而是让 agent 先知道这个仓库的规则、偏好、流程和注意事项。

更直白一点，它通常用来告诉 agent 这些事：

- 这个仓库是干什么的
- 改代码前后应该跑哪些命令
- 哪些目录能改，哪些目录不要碰
- 代码风格、测试规范、提交流程
- 遇到什么情况必须先询问你
- 这个项目里的一些“隐性知识”与约定俗成规则 

所以它很像：

- 给 AI 的 `README`
- 给 AI 的“项目操作手册”

## Global AGENTS.md

1. 关于实事求是，在命令失败之后不要瞎编乱造

   ```markdown
   ## Working agreements
   
   - Never present unverified results as facts.
   - If a command, tool call, or fetch fails, explicitly report the failure.
   - Quote the relevant error snippet with secrets redacted.
   - Stop conclusions that depend on missing or unverified data.
   ```

   

# Skill

## local skill

一个简单的方案是，在 codex app 中，使用他的 skill creator，在他的帮助下来 create local skill。

这个本地的 sikll 会创建一个文件夹，其中可能包括下列文件

```shell
review\
├───agents
│   └───openai.yaml
├───references
│   ├───review-checklist.md
│   └───rewrite-examples.md
└───SKILL.md
```



## load in app skill

创建好了之后，这个skill其实是在本地的，还没有加载到 codex 中去，在windows 中这个路径是 `C:\Users\Windows 10\.codex\skills\<skill-name>`

你可以让 codex 帮你安装这个 skill.
