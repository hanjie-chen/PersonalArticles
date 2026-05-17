# .gitignore file

有时候我们并不需要所有的文件都提交到 remote repo 中去，比如说 python 程序运行时，产生的临时文件（ `__pycache__` ）我们并不希望这些临时文件被提交

这个时候，我们可以写一个 .gitignore 文件来忽略某些特定的文件

### Global ignore

为了方便，我一般使用全局的，这样子就不用每个 repository 都配置过去了，只需要进入 `~`(user home directory)

然后创建一个 `.gitignore` 文件，并且配置 git 使用这个全局文件

```shell
cd ~
git config --global core.excludesfile ~/.gitignore
```

### personal `.gitignore`

在我的个人配置仓库中: https://github.com/hanjie-chen/personal-config/blob/main/git/.gitignore

## case sensitivity(windows)

在 windows OS 中，大小写不敏感，也就是说对于文件 `apg-multi-waf.md` 和 `apg-multi-waf.MD` 会被认为是同一个文件

但是在 Linux, 则是大小写敏感的，我个人也倾向于大小写敏感的，虽然无法修改整个 windows 操作系统为大小写敏感，但是对于 windows git, 我们可以设置

首先我们使用下面的命令查看目前仓库是否为大小写敏感

```powershell
> git config core.ignorecase
true
```

如果为 true 那么就意味着大小写不敏感，需要设置为 false

```powershell
> git config core.ignorecase false
```

然后就可以准确识别了

```powershell
> ls

    Directory: C:\Users\Plain\PersonalArticles\azure

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a---            1/9/2025  1:04 AM           1108 apg-multi-waf.md

> mv .\apg-multi-waf.md .\apg-multi-waf.MD
> git status
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add/rm <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        deleted:    apg-multi-waf.md

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        apg-multi-waf.MD

no changes added to commit (use "git add" and/or "git commit -a")
```