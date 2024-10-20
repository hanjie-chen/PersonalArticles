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

# 分支管理checkout

当你想要基于当前的版本开发下一个版本，或者存粹是希望不想要污染现在已经开发好的版本，可以基于现在已有的代码开启一条新的分支，继续开发

比如说我现在以及把前端开发好了，想要开发后端，可以创建一条新的分支，并且切换到这个分支。例如

`git checkout -b checkend-development`

## 命令详解

1. `checkout`: 这是Git的一个子命令,通常用于切换分支或恢复工作树文件。在这个上下文中,它被用来创建一个新分支并切换到该分支。
2. `-b`: 这是`checkout`命令的一个选项(option)。
   - 当与`checkout`一起使用时,`-b`表示"创建一个新分支"。
   - 如果没有`-b`选项,`checkout`只会切换到一个已存在的分支。
   - 使用`-b`选项,Git会创建新分支,然后立即切换到这个新创建的分支（如果该分支已经存在,Git会报错）

然后可以使用命令`git branch` 查看所有分支以及当前分支

## 切换分支

使用命令`git checkout main`切换回到main分支



## 删除分支

非常好的问题！在 Git 中删除分支是一个常见的操作，特别是当某个功能开发完成并合并到主分支后。以下是删除 Git 分支的几种方法：

1. 删除本地分支：

   使用 `-d` 选项（小写的 d）可以安全地删除已经合并到当前分支的分支：

   ```
   git branch -d <branch-name>
   ```

   例如：`git branch -d checkend-development`

   如果分支还没有被合并，Git 会给出警告并阻止删除。

2. 强制删除本地分支：

   如果你确定要删除一个未合并的分支，可以使用 `-D` 选项（大写的 D）强制删除：

   ```
   git branch -D <branch-name>
   ```

   例如：`git branch -D checkend-development`

   请谨慎使用此选项，因为它会无条件地删除分支，即使该分支包含未合并的更改。

3. 删除远程分支：

   如果你想删除远程仓库中的分支，可以使用以下命令：

   ```
   git push origin --delete <branch-name>
   ```

   或者使用这个较短的语法：

   ```
   git push origin :分支名称
   ```

   例如：`git push origin --delete checkend-development`

4. 删除所有已合并的本地分支：

   如果你想一次性删除所有已经合并到当前分支的本地分支，可以使用这个命令：

   ```
   git branch --merged | grep -v "\*" | xargs -n 1 git branch -d
   ```

   这个命令会列出所有已合并的分支，排除当前分支（带星号的），然后删除它们。

注意事项：

- 在删除分支之前，请确保你已经切换到其他分支（通常是主分支）。
- 删除分支是不可逆的操作，请确保你真的不再需要这个分支了。
- 如果分支包含未推送或未合并的更改，Git 会警告你。
- 删除远程分支需要你有适当的权限。

最后，一个好习惯是在删除分支之前，先检查一下分支列表：

```
git branch      # 查看本地分支
git branch -r   # 查看远程分支
git branch -a   # 查看所有分支（本地和远程）
```

这样可以确保你删除的是正确的分支。如果你有任何其他关于 Git 分支管理的问题，欢迎继续询问！

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

## python auto generated file
__pycache__/
*.pyc
```

# Git pull

好的，我来为您解释如何使用git pull强制覆盖本地未提交的修改。这个操作需要谨慎使用，因为它会丢失您本地的所有未提交更改。以下是步骤：

1. 首先，确保您在正确的分支上：
   ```
   git checkout <your-branch>
   ```

2. 然后，使用以下命令强制覆盖本地更改：
   ```
   git fetch --all
   git reset --hard origin/<your-branch>
   ```

这里的步骤解释：

- `git fetch --all` 从远程仓库获取所有最新的提交，但不会合并或修改您的本地文件。
- `git reset --hard origin/<your-branch>` 将您当前分支的本地文件强制重置为远程分支的状态。

请注意，这个操作是不可逆的。它会丢弃所有本地未提交的更改，包括暂存的和未暂存的更改。您的本地分支将与远程分支完全一致。

如果您只想更新某些文件而不是整个分支，可以使用以下命令：

```
git checkout origin/<your-branch> -- <path/to/file>
```

这将仅覆盖指定的文件，而不影响其他文件。

最后，我想强调一下，在执行这些操作之前，如果您的本地更改可能有价值，最好先创建一个备份或使用 `git stash` 来保存您的更改。这样，如果您之后发现需要这些更改，还可以恢复它们。

您是否需要我进一步解释这些命令或git的工作原理？

# Reference

[^1]: [Some common .gitignore configurations (github.com)](https://gist.github.com/octocat/9257657)

