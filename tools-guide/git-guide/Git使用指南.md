---
Title: Git使用指南
Author: 陈翰杰
Instructor: GPT-4o, Sonnet3.5
CoverImage: ./images/cover_image.png
RolloutDate: 2024-08-26
Category: ToolGuide/GitGuide/GitUsage
---

```
BriefIntroduction: 
本人总结的git速查指南，一般来说是遇到问题 --> 问Sonnet3.5 --> 解决问题 --> 记录在这里
虽然有很多其他的 git 资料，但是自从LLM出现之后，我遇到问题一般直接提问LLM，爽的一批
```

<!-- split -->

![cover image](./images/cover_image.png)

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

另一种方式：

同时执行2个命令：

```bash
git add . && git commit -m "message"
```



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

# git merge

当我们在一个分支上开发，并且开发的差不多了之后，比如说一个功能开发完成了，或者开发到了某个阶段，那么我们就可以把这个分支上面开发的内容同步到main上面去。然后我们接着回到这个分支上继续开发。

这是我们需要进行的具体的步骤

**首先切换到 main 分支**：

```bash
git checkout main
```

**将分支的内容合并到 main**：

```bash
git merge <branch-name>
```

**推送更新后的 main 分支到远程仓库**（如果有远程仓库的话）：

```bash
git push origin main
```

**切换回分支继续开发**：

```bash
git checkout <branch-name>
```

### 完整操作示例

```bash
# 1. 确保当前分支的修改已经提交
git status

# 2. 切换到 main 分支
git checkout main

# 3. 合并 backend-development 分支
git merge backend-development

# 4. 如果有远程仓库，推送更新
git push origin main

# 5. 切换回 backend-development 继续开发
git checkout backend-development
```

# related remote repository

可以使用以下命令查看当前Git仓库关联的远程地址：

```bash
git remote -v
```

执行这个命令后，你会看到类似于以下的输出：

```
origin  https://github.com/username/repository.git (fetch)
origin  https://github.com/username/repository.git (push)
```

其中，`origin`是默认的远程名称，后面跟着的就是远程仓库的URL。如果你有多个远程仓库，都会在这里列出。



# rollback change

如果修改了文件，但是没有进行git add && git commit 例如这面这种状态

```bash
Plain@Linux-VM:~/Personal_Project/getting-started-todo-app$ git status
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   compose.yml

no changes added to commit (use "git add" and/or "git commit -a")
```

这种情况下回撤修改非常简单，可以直接使用 git 提示中显示的命令：

```bash
git restore compose.yml
```

需要注意的是：
1. 这个操作会直接丢弃你对 compose.yml 的所有修改
2. 这个操作无法撤销，所以在执行之前请确认你真的要放弃这些修改

如果你想在回撤之前查看具体修改了什么内容，可以使用：
```bash
git diff compose.yml
```

这样可以看到具体的修改内容，再决定是否要回撤修改。

# `.gitignore` file

当python程序运行的时候，会产生一些临时的文件，存放在本地路径的`__pycache__`文件夹中，但是当我们提交的时候并不希望这些临时文件被提交，这个时候，我们可以写一个`.gitignore`文件来忽略某些特定的文件



## Global ignore

为了方便，我一般使用全局的，这样子就不用每个repository都配置过去了，只需要进入`~`(user home directory)

然后创建一个`.gitignore`文件，并且配置git使用这个全局文件

```shell
cd ~
git config --global core.excludesfile ~/.gitignore
```



参考了经典`.gitignore` 方案，来自 [Some common .gitignore configurations](https://gist.github.com/octocat/9257657)

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
*.db

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

# Furture consider

尝试理解 Git 原理 [自己动手写 Git](https://wyag-zh.hanyujie.xyz/)
