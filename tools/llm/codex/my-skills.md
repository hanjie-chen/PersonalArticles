# Online Skills

ai 往往喜欢自己从 0 到 1 开始探索，写代码或者造轮子，在有些场景我们往往那个需要要求它探索是否已经存在现成的方案，比如说使用 skill installer 

这是我常用的用来提升效率的 skill

自动化浏览器操作：

- playwright-cli
- playwrithg-interactice

# Self define Skill

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



## load self-defin skill in codex app

创建好了之后，这个skill其实是在本地的，还没有加载到 codex 中去，在windows 中这个路径是 `C:\Users\Windows 10\.codex\skills\<skill-name>`

可以直接让 codex 帮你安装这个 skill.