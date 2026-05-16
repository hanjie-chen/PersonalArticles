---
Title: Git Command Quick Reference
SourceBlob: 3ec381dd72470d118d575c9e9391648953c4f05f
---

```
BriefIntroduction: Common Git commands, typical scenarios, and common pitfalls organized by workflow
```

<!-- split -->

After creating a new repository on GitHub, GitHub will show instructions for what to do next. What we need to do is follow the repository’s prompts to initialize the local repository and complete the first push.

<img src="./resources/images/new-repo.png" alt="new repository" style="zoom:50%;" />

# Local Workflow

## git status

Shows the current state of the repository.

## git add

I usually use `git add .` directly to stage everything. This command adds modified files to the staging area.

## git commit

```shell
git commit -m "add your specification of this commit"
```

Each commit records who made what changes and when, and allows you to return to that state later.

### commit id

- After each successful commit, Git generates a unique 40-character hexadecimal string, called a SHA-1 hash, as the ID of that commit.
- Even changing a single space will completely change the SHA ID. This guarantees that code history cannot be tampered with silently.
- When running commands or performing DevOps rollbacks, you usually only need to enter the first 7 characters of the SHA, such as `a1b2c3d`, to locate a commit precisely.

View historical commits and their corresponding SHA IDs:

``` shell
git log --oneline
```

If you forget the information from the previous commit, you can use:

```shell
git show
```

By default, this command shows the content of `HEAD`, which is the latest commit on the current branch. You can also append a specific SHA ID to view a historical commit: `git show <SHA>`

### git add + git commit

For tracked files: if these files were only modified and no new files need to be added, you can directly use `git commit -a -m "message"` to commit those changes. This command automatically commits modifications to all tracked files, without requiring a manual `git add` first.

For new files: you need to use `git add` to add them to the staging area, because Git only tracks files that have already been added to version control by default. Before new files are tracked, they must be added with `git add`. In this case, we can use the following command:

```bash
git add . && git commit -m "message"
```

# Remote Sync

## git push

Pushes local content to GitHub for synchronization.

### first push of a new branch

If this is a newly created local branch, meaning the remote repository does not have this branch yet, and you are pushing it to the remote repository for the first time, you need to include the `-u` option:

```shell
git push -u origin <branch-name>
```

This command does two things at the same time:

1. Creates a remote branch: creates a new branch with the same name in the remote repository, such as GitHub, and uploads the code.
2. Sets up tracking, also called upstream: binds the local branch to the remote branch.

If you do not include the `-u` option and only use `git push origin <branch-name>`, Git can still create the remote branch, but it will not establish the default tracking relationship. This means that future pushes cannot simply use the shorter `git push`; Git will report an error because it does not know which remote branch the local branch should be pushed to.

### push rejected

Sometimes, when using `git push`, you may encounter an error like this:

```shell
➜ git push
To github.com:hanjie-chen/Test-Website.git
 ! [rejected]        backend-development -> backend-development (fetch first)
error: failed to push some refs to 'github.com:hanjie-chen/Test-Website.git'
hint: Updates were rejected because the remote contains work that you do not
hint: have locally. This is usually caused by another repository pushing to
hint: the same ref. If you want to integrate the remote changes, use
hint: 'git pull' before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
```

This means the remote repository already contains commits that you do not have locally, so you need to run `git pull` first to synchronize the latest changes.

## git pull

Corresponding to `git push`, `git pull` is used to synchronize the latest changes from the remote repo, such as GitHub, to your local machine.

For example, you might develop the same project on multiple machines: an Azure VM, a local machine running Windows 10, and a MacBook Pro.

If you run `git push` on one of those machines, the other machines need to run `git pull` so their local code catches up with the latest remote state.

By default, when you run `git pull` on a branch, it only updates the current local branch. It does not automatically update other branches, although it usually refreshes information about remote-tracking branches.

### how git pull works

More precisely:

git pull = git fetch + git merge

- git fetch: gets the latest commit from the current remote branch
- git merge: tries to merge that commit into the current local branch

So the current local branch is actually updated. Other local branches do not automatically move forward, but information about remote-tracking branches is usually refreshed.

### divergent branches

Suppose we modified the latest code on the remote, such as GitHub, and also modified the local code and committed it with `git add + git commit`.

Even if the modified content does not conflict, when we run `git pull` locally, we may see the following message:

```shell
$ git pull
remote: Enumerating objects: 20, done.
remote: Counting objects: 100% (20/20), done.
remote: Compressing objects: 100% (13/13), done.
remote: Total 13 (delta 7), reused 0 (delta 0), pack-reused 0 (from 0)
Unpacking objects: 100% (13/13), 4.71 KiB | 344.00 KiB/s, done.
From github.com:hanjie-chen/website
   0b18d4f..55d30e5  main       -> origin/main
 * [new tag]         v0.1.0     -> v0.1.0
hint: You have divergent branches and need to specify how to reconcile them.
hint: You can do so by running one of the following commands sometime before
hint: your next pull:
hint:
hint:   git config pull.rebase false  # merge
hint:   git config pull.rebase true   # rebase
hint:   git config pull.ff only       # fast-forward only
hint:
hint: You can replace "git config" with "git config --global" to set a default
hint: preference for all repositories. You can also pass --rebase, --no-rebase,
hint: or --ff-only on the command line to override the configured default per
hint: invocation.
fatal: Need to specify how to reconcile divergent branches.
```

Git is asking for your preference: since the remote branch, such as GitHub, and the local branch both have different new commits, how do you want to combine them?

We can use rebase to move your local commits after the remote commits.

Run this inside your repository directory:

```shell
$ git pull --rebase
Successfully rebased and updated refs/heads/main.
```

This does two things: first it pulls remote updates, then it **replays** your local commits one by one after the latest commit from `origin/main`. If there are truly no conflicts, it will succeed directly.

After it succeeds, run `git push`.

# Git State Flow

To understand what the previous commands do, first think of Git as several different state areas.

```text
Working Directory     Staging Area       Local Repository    Remote Repository
       |                    |                   |                   |
       +----- git add ----->+                   |                   |
                            +--- git commit --->+                   |
                                                +---- git push ---->+
```

- `Working Directory`: where you edit files
- `Staging Area`: the area prepared for commit after running `git add`
- `Local Repository`: the content saved in the local repository after running `git commit`
- `Remote Repository`: the content saved on the remote after running `git push`

From this perspective, `git add`, `git commit`, and `git push` each move content one layer forward, while `git pull` synchronizes the latest state from the remote repository back to local.

# Branch Management

## List Branches

`git branch` shows local branches.

```shell
➜ git branch
* main
```

`git branch -r` shows remote branches.

```shell
➜ git branch -r
  origin/HEAD -> origin/main
  origin/backend-development
  origin/main
```

`git branch -a` shows all branches, both local and remote.

```shell
➜ git branch -a
* main
  remotes/origin/HEAD -> origin/main
  remotes/origin/backend-development
  remotes/origin/main
```

> [!note]
>
> After `git clone`, Git brings remote branch information into local storage, but by default it only checks out the default branch of the remote repository, usually `main`.
>
> So when you run `git branch`, you usually only see the `main` branch, while `git branch -r` shows remote branches.

## Switch Branch

The `git checkout <branch-name>` command first looks for a local branch named `branch-name`. If it finds one, it switches to that branch.

If it does not find a local branch, it looks for a remote branch named `branch-name`. If it finds one, it creates a local branch with the same name, establishes a tracking relationship, and then switches to that new local branch.

e.g.

```shell
➜ git branch
* main
➜ git branch -r
  origin/HEAD -> origin/main
  origin/backend-development
  origin/main
➜ git checkout backend-development
Switched to a new branch 'backend-development'
branch 'backend-development' set up to track 'origin/backend-development'.
```

## Create Branch

The `git checkout -b <branch-name>` command creates a new branch and immediately switches to that newly created branch. If the branch already exists, Git will report an error.

In fact, this command is shorthand for `git branch <branch-name>` and `git checkout <branch-name>`.

The newly created branch is based on the branch you are currently on. For example, if you are currently on the `main` branch, then the new branch `branch-name` will be created based on `main`.

### First Push to Remote

After we create a branch, it only exists locally. The remote does not have this branch yet, so the first time we need to use this command to push it to the remote:

```shell
git push -u origin <branch-name>
```

If you think writing the branch name every time is too troublesome, you can configure Git’s push behavior:

```bash
git config --global push.default current
```

After this setting, whenever you run `git push`, Git will automatically push to a remote branch with the same name, creating it if it does not exist.

## Parallel Branch Work

Suppose we run into this situation:

We are developing on the main branch and talking with a coding agent, such as Codex or Claude Code. This agent may run for a long time, so we do not need to keep watching it.

But at the same time, if we want to inspect or modify something on another branch, such as `k8s-lab`, what should we do?

If both sessions share the same Git working directory, then running this directly in the current directory:

```shell
git checkout k8s-lab
```

will switch the files in that directory to the state of the `k8s-lab` branch. As a result, the working directory that the agent session running on the main branch depends on will also be changed, which may disrupt its context or runtime environment.

> [!note]
>
> This also explains why tmux cannot truly solve this problem.
>
> tmux only opens multiple terminal sessions. If those terminals all operate on the same Git directory, then as soon as one terminal runs `git checkout`, the directory state seen by the other terminals changes too, because they share the same working directory.

This is where the `git worktree` command can be used.

It creates another independent working directory under the same Git repository, and usually checks out that directory to a specific branch.

For example:

```text
repo
├── website/          -> main
└── website-k8s/      -> k8s-lab
```

In this setup:

- the `website/` worktree is currently checked out on `main`
- the `website-k8s/` worktree is currently checked out on `k8s-lab`

So one coding agent session can continue running on the main branch;

while we can enter another worktree to inspect or modify code on the `k8s-lab` branch without affecting the former.

You can understand a worktree as expanding a branch into an independent working directory.

In the earlier Git State Flow, Working Directory means “where you edit files”; `git worktree` can be understood as allowing the same repository to have multiple independent Working Directories at the same time.

> [!note]
>
> By default, the same branch cannot be checked out into two worktrees at the same time.

Usage:

Create a new worktree:

```shell
git worktree add ../website-k8s k8s-lab
```

- Create a new directory at `../website-k8s`
- Check out that directory to `k8s-lab`

That is, `git worktree add <path> <branch>`.

View the worktree list:

```shell
git worktree list
```

Remove a worktree:

```shell
git worktree remove ../website-k8s
```

If this worktree still contains uncommitted changes, Git may refuse to remove it by default.

## Merge Branch

When we develop on a branch and the work is mostly done, such as when a feature is complete or has reached a certain stage, we can synchronize the content developed on that branch back to `main`.

The steps are as follows.

First switch to the main branch:

```bash
git checkout main
```

Merge the branch content into main:

```bash
git merge <branch-name> -m "merge message"
```

Push the updated main branch to the remote repository, if there is one:

```bash
git push origin main
```

## Delete Branch

After a branch has finished development and has been merged into the main branch, we can delete it to keep the repository clean.

First, delete the local branch.

### Delete Local Branch

Use the `-d` option, lowercase d, to safely delete a branch that has already been merged into the current branch:

```bash
git branch -d <branch-name>
```

For example: `git branch -d backend-development`

If the branch has not been merged yet, Git will warn you and prevent the deletion.

Force-delete a local branch:

If you are sure you want to delete an unmerged branch, you can use the `-D` option, uppercase D, to force the deletion:

```bash
git branch -D <branch-name>
```

> [!note]
>
> Using `git branch -d <branch-name>` only deletes the local branch. It does not affect the branch on the remote repository, such as GitHub, at all.

Next, delete the remote branch.

### Delete Remote Branch

Use the following command:

```bash
git push origin --delete <branch-name>
```

# Rollback

## git restore

If you modified a file but have not run `git add`, e.g.

```bash
$ git status
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   compose.yml

no changes added to commit (use "git add" and/or "git commit -a")
```

In this case, reverting the modification is very simple. You can directly use the command shown in Git’s hint:

```bash
git restore compose.yml
```

Note that:

1. This operation directly discards all modifications to `compose.yml`
2. This operation cannot be undone, so confirm that you really want to discard these changes before running it

If you want to check what exactly was changed before reverting, you can use:

```bash
git diff compose.yml
```

This lets you see the specific changes first, then decide whether to revert them.

If the modification has already entered the staging area, `git restore <file>` is not enough. You need to handle staged changes in another way.

## git reset

`git reset` is used to move the current state back to a certain position.

### reset to last commit

If you only want to discard local changes that have not been committed yet, you can use:

```bash
git reset --hard HEAD
```

Where:

- `HEAD` points to the latest commit on the current branch
- `--hard` means resetting both the Working Directory and the Staging Area

So this command clears changes in the working directory and staging area, but it does not move the local branch back to an earlier commit.

### reset to remote branch

If you want to discard all local modifications and local commits, keeping only the latest state from the remote repository, you can use:

```bash
git fetch origin
git reset --hard origin/main
```

Where:

- `git fetch origin` gets the latest remote state, but does not automatically merge it
- `origin/main` points to the latest position of the `main` branch in the remote repository
- `git reset --hard origin/main` forcibly resets the current branch to the state of the remote branch

This means it clears:

- Modifications in the Working Directory
- Modifications in the Staging Area
- Local commits in the Local Repository that have not yet been pushed

### rollback scope

```text
Working Directory 	  Staging Area 	 local repository     remote repository
   (edit file) ------> (git add) ----> (git commit) -------> (git push)    
|_________________|________________|
        git reset --hard HEAD
|_________________|________________|___________________|
                git reset --hard origin/main               
```

# Remote Repository

## Clone Repository

If we want to clone a remote repository locally, we can use the `git clone [url]` command. e.g.

```shell
git clone https://github.com/hanjie-chen/PersonalArticles.git
```

This command creates a local folder with the same name, then downloads the contents of the remote repo into it.

```shell
~ # git clone https://github.com/hanjie-chen/PersonalArticles.git
Cloning into 'PersonalArticles'...
remote: Enumerating objects: 1329, done.
remote: Counting objects: 100% (478/478), done.
remote: Compressing objects: 100% (357/357), done.
remote: Total 1329 (delta 166), reused 401 (delta 101), pack-reused 851 (from 1)
Receiving objects: 100% (1329/1329), 110.04 MiB | 39.59 MiB/s, done.
Resolving deltas: 100% (416/416), done.
~ # ls
PersonalArticles
```

> [!note]
>
> For now, you can understand this as downloading a remote repository locally, but it is more complete than a normal download because it also brings down Git history and repository information.

If we want to specify the folder, we can directly add the folder path to the end of the `git clone` command. e.g.

```bash
git clone https://github.com/hanjie-chen/PersonalArticles.git ./articles-data
```

> [!note]
>
> If the target directory already exists, it usually must be an empty directory.

### Shallow Clone

Sometimes, we only need to download the current code of a repo, such as for a knowledge base repo, and do not need its historical information. We can use this command to fetch only the current content:

```shell
git clone --depth 1 [url]
```

The default `git clone` downloads the full history of changes from the “first line of code” to the current code.

`--depth 1` tells Git: “I only want the state of the latest commit. I do not want any previous history.”

This can reduce storage pressure caused by historical changes.

### HTTPS vs. SSH

There are two ways to run `git clone`: one uses HTTPS, and the other uses SSH. e.g.

```bash
git clone https://github.com/hanjie-chen/PersonalArticles.git
git clone git@github.com:hanjie-chen/PersonalArticles.git
```

The difference between these two methods lies in the authentication method:

- HTTPS: when you need to run `git push`, additional authentication is required, such as browser login or a token
- SSH: relies on a local SSH key and GitHub public key configuration

Generally, choose the second method: configure an SSH key and use Git via SSH.

## Manage Remote

### View Remote

You can use the following command to view the remote addresses associated with the current Git repository:

```bash
git remote -v
```

After running this command, you will see output similar to the following:

```
origin  https://github.com/username/repository.git (fetch)
origin  https://github.com/username/repository.git (push)
```

Here, `origin` is the default remote name, followed by the URL of the remote repository. If you have multiple remote repositories, they will all be listed here.

### Change Remote URL

If the repository name on GitHub has changed, or if you want to switch the remote from HTTPS to SSH, you can use the following command to modify the remote repository URL:

```shell
git remote set-url origin https://github.com/username/new-repo-name.git
# or
git remote set-url origin git@github.com:username/new-repo-name.git
```

# Appendix

## .gitignore file

Sometimes we do not need to commit all files to the remote repo. For example, temporary files generated when running Python programs, such as `__pycache__`, should not be committed.

In this case, we can write a `.gitignore` file to ignore certain specific files.

### Global ignore

For convenience, I usually use a global ignore file. This way, I do not need to configure every repository separately. I only need to enter `~`, the user home directory.

Then create a `.gitignore` file and configure Git to use this global file:

```shell
cd ~
git config --global core.excludesfile ~/.gitignore
```

### personal `.gitignore`

In my personal configuration repository: https://github.com/hanjie-chen/personal-config/blob/main/git/.gitignore

## case sensitivity(windows)

In Windows OS, paths are case-insensitive. This means files like `apg-multi-waf.md` and `apg-multi-waf.MD` are considered the same file.

Linux, however, is case-sensitive. I personally also prefer case sensitivity. Although we cannot make the entire Windows operating system case-sensitive, we can configure Windows Git.

First, use the following command to check whether the current repository is case-sensitive:

```powershell
> git config core.ignorecase
true
```

If the result is `true`, it means the repository is case-insensitive and needs to be set to `false`:

```powershell
> git config core.ignorecase false
```

Then Git can recognize case differences accurately:

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
