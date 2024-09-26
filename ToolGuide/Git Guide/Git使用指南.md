---
Title: Git使用指南
Author: 陈翰杰
Instructor: GPT-4o, Sonnet
CoverImage: ./image/cover_image.jpg
RolloutDate: 2024-08-26
UltimateModifiedDate:
Category: XXX
---

```
BriefIntroduction: 
git速查指南
```

<!-- split -->

![cover image](./image/cover_image.jpeg)

# 写在前面/Before we beginning

git 速查指南

# Title: Git使用指南

当在github上面新建完成一个仓库之后，github会提示你如何进行下一步操作。而我们需要做的部分就是更新仓库，然后推送到github上面。

# 3个基础命令

## git add

当然我一般直接使用`git add .`全都提交，这个命令的作用是将修改过的文件添加到暂存区（staging area）。

## git commit

将暂存区的变更提交到本地仓库，提交（commit）是Git中的一个核心概念，代表了一个项目历史中的一个点。每次提交都会记录下谁在什么时间做了什么更改，并允许你回到这个状态或者比较不同提交之间的差异。`git commit`命令实际上创建了一个快照，它包含了暂存区中所有文件的一个特定状态。

更具体的使用需要`git commit -m "add your specification of this commit"` 这个玩意是必须填的，用来追踪每次提交的目的

## git push

推送到github上面同步

## git add + git commit = ?

`git add`和`git commit`可以合并为`git commit -a -m "your message"`

不过这个会提交所有的修改，当然对我这种一直都是用`git add .`的人来说，没差了

note:

- **对于新文件**: 需要使用`git add`将它们添加到暂存区，因为Git默认只跟踪已经添加到版本控制中的文件。新文件在被跟踪之前，必须先通过`git add`命令添加。

- **对于已被跟踪的文件**: 如果这些文件只是进行了修改，而没有新文件需要添加，那么可以直接使用`git commit -a -m "message"`来提交这些更改。这个命令会自动将所有已被跟踪文件的修改提交，而不需要先手动`git add`它们。

所以，`git add`主要用于将新文件或目录添加到版本控制中，而`git commit -a`则用于提交已经在版本控制中的文件的修改。

# 分支管理

当你想要基于当前的版本开发下一个版本，或者存粹是希望不想要污染现在已经开发好的版本，可以基于现在已有的代码开启一条新的分支，继续开发

比如说我现在以及把前端开发好了，想要开发后端，可以创建一条新的分支，并且切换到这个分支。例如

`git checkout -b checkend-development`



# Git ignore

当python程序运行的时候，会产生一些临时的文件，存放在本地路径的`__pycache__`文件夹中，但是当我们提交的时候并不希望这些临时文件被提交，这个时候，我们可以写一个`.gitignore`文件来忽略某些特定的文件



## Global ignore

为了方便，我一般使用全局的，这样子就不用每个repository都配置过去了，只需要进入`~`(user home directory)

然后创建一个`.gitignore`文件，并且配置git使用这个全局文件

```shell
cd ~
git config --global core.excludesfile ~/.gitignore
```



经典`.gitignore` 方案，来自github[^1]

```python
# Compiled source #
###################
*.com
*.class
*.dll
*.exe
*.o
*.so

# Packages #
############
# it's better to unpack these files and commit the raw source
# git has its own built in compression methods
*.7z
*.dmg
*.gz
*.iso
*.jar
*.rar
*.tar
*.zip

# Logs and databases #
######################
*.log
*.sql
*.sqlite

# OS generated files #
######################
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
```



# Reference

[^1]: [Some common .gitignore configurations (github.com)](https://gist.github.com/octocat/9257657)

