<!-- source_blob: f71a0e36422d92ea4118a30d95741bb67dd681ba -->

After creating a new repository on GitHub, GitHub will prompt you with the next steps. What we need to do is follow those instructions to initialize the local repository and complete the first push.

<img src="./resources/images/new-repo.png" alt="new repo" style="zoom:50%;" />

# Local Workflow

## git status

You can use it to check the current status of the repository.

## git add

Of course, I usually just use `git add .` to stage everything. This command adds modified files to the staging area.

## git commit

```shell
git commit -m "add your specification of this commit"
```

Each commit records who made what changes and when, and allows you to return to that state later.

### commit id

- After each successful commit, Git generates a unique 40-character hexadecimal string (called a SHA-1 hash) as the ID of that commit.
- Even changing a single space will completely change the SHA ID. This ensures the integrity of the code history.
- When running commands or performing DevOps rollbacks, you usually only need the first 7 characters of the SHA (for example, `a1b2c3d`) to identify the commit precisely.

To view the commit history and corresponding SHA IDs:

``` shell
git log --oneline
```

If you forget the information from the most recent commit, you can use:

```shell
git show
```

By default, this command shows the contents of `HEAD` (the latest commit on the current branch). You can also append a specific SHA ID to inspect history: `git show <SHA>`

### git add + git commit

For tracked files: if these files were only modified and there are no new files to add, you can commit directly with `git commit -a -m "message"`. This command automatically includes modifications to all tracked files, so you do not need to run `git add` manually first.

For new files: you need to use `git add` to place them in the staging area, because Git only tracks files that have already been added to version control. New files must be added with `git add` before they are tracked. In that case, you can use the following command:

```bash
git add . && git commit -m "message"
```

# Remote Sync

## git push

Push local content to GitHub to synchronize it.

### first push of a new branch

If the branch was created locally (that is, the remote repository does not have this branch yet), and this is the first time you are pushing it to the remote repository, you need to include the `-u` option:

```shell
git push -u origin <branch-name>
```

This command does two things at once:

1. Create the branch on the remote: create a new branch with the same name on the remote repository (such as GitHub) and upload the code.
2. Establish tracking (Upstream): bind the local branch to the remote branch.

If you omit the `-u` option and only use `git push origin <branch-name>`, Git can still create the branch on the remote, but it will not establish the default tracking relationship. That means future pushes cannot use the shorter `git push` command directly, because Git will not know which remote branch the local branch should be pushed to.

### push rejected

Sometimes when we run `git push`, we may see an error like this:

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

This means the remote repository already has commits that your local repository does not have yet, so you need to run `git pull` first to sync the latest changes.

## git pull

Corresponding to `git push`, `git pull` is used to synchronize the latest changes from the remote repo (GitHub) to the local repository.

For example, when developing the same project on multiple machines: Azure VM, local machine (Windows 10), and MacBook Pro.

If you run `git push` on one machine, the others need to run `git pull` so the local code stays up to date with the remote.

By default, when you run `git pull` on a branch, it only updates the current local branch; it does not automatically update other local branches, though it usually refreshes the remote-tracking branch information.

### how git pull works

More precisely:

git pull = git fetch + git merge

- `git fetch`: get the latest commit from the current remote branch
- `git merge`: try to merge that commit into the current local branch

So the current local branch is actually updated, while other local branches do not move forward automatically, though the remote-tracking branch information is usually refreshed.

### divergent branches

When the latest code on the remote (GitHub) has been modified, and the local code has also been modified and committed (`git add` + `git commit`).

Even if the changes do not conflict, when you run `git pull` locally, you may see the following message:

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

Git is essentially "asking for your preference" here: since both the remote (GitHub) and local repository have different new commits (divergent branches), how would you like to combine them?

We can use rebase to move your local commits so they come after the remote commits.

Run this inside your repository directory:

```shell
$ git pull --rebase
Successfully rebased and updated refs/heads/main.
```

This does two things: first it pulls the remote updates, then it **replays** your local commits one by one on top of the latest commit in `origin/main`. If there are no conflicts, it will succeed directly.

After that, run `git push`.

# Git State Flow

To understand what the commands above do, it helps to think of Git as several different state areas.

```text
Working Directory     Staging Area       Local Repository    Remote Repository
       |                    |                   |                   |
       +----- git add ----->+                   |                   |
                            +--- git commit --->+                   |
                                                +---- git push ---->+
```

- `Working Directory`: where you are when editing files
- `Staging Area`: the area prepared for commit after running `git add`
- `Local Repository`: what is stored in the local repository after running `git commit`
- `Remote Repository`: what is stored on the remote after running `git push`

From this perspective, `git add`, `git commit`, and `git push` each move content one step forward, while `git pull` synchronizes the latest state from the remote repository back to the local one.

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

`git branch -a` shows all branches (local and remote).

```shell
➜ git branch -a
* main
  remotes/origin/HEAD -> origin/main
  remotes/origin/backend-development
  remotes/origin/main
```

> [!note]
>
> After `git clone`, Git also brings the remote branch information to the local repository, but by default it only checks out the remote repository's default branch (usually `main`).
>
> So when you run `git branch`, you will usually only see the `main` branch, while `git branch -r` will show the remote branches.

## Switch Branch

The `git checkout <branch-name>` command first looks for a local branch named `branch-name`. If it finds one, it switches to that branch.

If it does not find a local branch, it looks for a remote branch named `branch-name`. If it finds one, it creates a local branch with the same name, sets up tracking, and then switches to that new local branch.

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

The `git checkout -b <branch-name>` command creates a new branch and then immediately switches to it (if the branch already exists, Git will report an error).

In fact, this command is shorthand for `git branch <branch-name>` plus `git checkout <branch-name>`.

The new branch is based on the branch you are currently on. For example, if you are currently on `main`, then the new branch `branch-name` is created from `main`.

### First Push to Remote

After creating a branch, it only exists locally. The remote still does not have a corresponding branch, so the first time you need to use this command to push it to the remote:

```shell
git push -u origin <branch-name>
```

If you think typing the branch name every time is too troublesome, you can configure Git's push behavior:

```bash
git config --global push.default current
```

After setting this, whenever you run `git push`, Git will automatically push to the remote branch with the same name (and create it if it does not exist).

## Parallel Branch Work

Suppose we run into the following situation:

We are developing on the `main` branch and talking to a coding agent (such as Codex or Claude Code). That agent may run for a long time, so we do not need to watch it constantly.

But meanwhile, if we also want to check or modify something on another branch like `k8s-lab`, what should we do?

If two sessions share the same Git working directory, then directly running this in the current directory:

```shell
git checkout k8s-lab
```

will switch the files in that directory to the state of the `k8s-lab` branch. As a result, the working directory relied on by the agent session running on the `main` branch will also change, which may disrupt its context or runtime environment.

> [!note]
>
> This also explains why tmux cannot truly solve this problem.
>
> tmux only opens multiple terminal sessions. If those terminals operate on the same Git directory, then as soon as one terminal runs `git checkout`, the directory state seen by the others changes as well, because they share the same working directory.

In that case, you can use the `git worktree` command.

It creates another independent working directory under the same Git repository, and usually checks that directory out to a specific branch.

For example:

```text
repo
├── website/          -> main
└── website-k8s/      -> k8s-lab
```

This way:

- `website/` is currently checked out to `main`
- `website-k8s/` is currently checked out to `k8s-lab`

So one coding agent session can continue running on the `main` branch;

while we ourselves can enter another worktree and inspect or modify code on the `k8s-lab` branch without affecting the first one.

You can think of a worktree as expanding one branch into an independent working directory.

In the earlier Git State Flow, `Working Directory` represented "where you are when editing files"; `git worktree` can be understood as allowing the same repository to have multiple independent `Working Directory` instances at the same time.

> [!note]
>
> By default, the same branch cannot be checked out in two worktrees at the same time.

How to use it:

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

If that worktree still has uncommitted changes, Git may refuse to remove it by default.

## Merge Branch

When we develop on a branch and the work is mostly done, for example when a feature has been completed or development has reached a certain stage, we can synchronize the changes from that branch back into `main`.

The steps are as follows.

First, switch to the `main` branch:

```bash
git checkout main
```

Merge the branch into `main`:

```bash
git merge <branch-name> -m "merge message"
```

Push the updated `main` branch to the remote repository (if there is one):

```bash
git push origin main
```

## Delete Branch

After a branch has finished development and been merged into the `main` branch, we may choose to delete it to keep the repository tidy.

First, delete the local branch.

### Delete Local Branch

Use the `-d` option (lowercase `d`) to safely delete a branch that has already been merged into the current branch:

```bash
git branch -d <branch-name>
```

For example: `git branch -d backend-development`

If the branch has not been merged yet, Git will warn you and prevent deletion.

Force-delete a local branch:

If you are sure you want to delete an unmerged branch, you can use the `-D` option (uppercase `D`) to force deletion:

```bash
git branch -D <branch-name>
```

> [!note]
>
> Using `git branch -d <branch-name>` only deletes the local branch. It does not affect the branch on the remote repository (Remote/GitHub) at all.

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

In this case, reverting the change is very simple. You can directly use the command shown in Git's hint:

```bash
git restore compose.yml
```

Please note:

1. This operation will directly discard all modifications to `compose.yml`
2. This operation cannot be undone, so make sure you really want to abandon those changes before running it

If you want to see exactly what was changed before rolling it back, you can use:

```bash
git diff compose.yml
```

This lets you review the actual changes first, then decide whether to revert them.

If the change has already entered the staging area, `git restore <file>` is no longer enough, and you need to use another method to handle staged changes.

## git reset

`git reset` is used to move the current state back to a certain point.

### reset to last commit

If you only want to discard local changes that have not been committed yet, you can use:

```bash
git reset --hard HEAD
```

Here:

- `HEAD` points to the latest commit on the current branch
- `--hard` means resetting both the `Working Directory` and the `Staging Area`

So this command clears changes in the working directory and staging area, but it does not move the local branch back to an earlier commit.

### reset to remote branch

If you want to discard all local changes and local commits, and keep only the latest state from the remote repository, you can use:

```bash
git fetch origin
git reset --hard origin/main
```

Here:

- `git fetch origin` retrieves the latest state from the remote, but does not merge automatically
- `origin/main` points to the latest position of the `main` branch on the remote repository
- `git reset --hard origin/main` forcibly resets the current branch to match the remote branch

This means it will clear:

- changes in the `Working Directory`
- changes in the `Staging Area`
- local commits in the `Local Repository` that have not been pushed yet

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
> For now, you can think of this as downloading the remote repository to your local machine, but it is more complete than an ordinary download because it also brings down the Git history and repository metadata.

If we want to specify the folder name, we can add a folder path directly to the end of the `git clone` command. e.g.

```bash
git clone https://github.com/hanjie-chen/PersonalArticles.git ./articles-data
```

> [!note]
>
> If the target directory already exists, it usually must be empty.

### Shallow Clone

Sometimes we only need the current code of a repo (for example, for a knowledge base repo) and do not need its history. In that case, we can use this command to fetch only the current contents:

```shell
git clone --depth 1 [url]
```

By default, `git clone` downloads the entire history of the repository, from the "first line of code" to the current code.

`--depth 1` tells Git: "I only want the state of the latest commit. I do not want any earlier history."

This can reduce storage pressure caused by historical revisions.

### HTTPS vs. SSH

There are two ways to `git clone`: one uses HTTPS, and the other uses SSH. e.g.

```bash
git clone https://github.com/hanjie-chen/PersonalArticles.git
git clone git@github.com:hanjie-chen/PersonalArticles.git
```

The difference between these two methods is the authentication method:

- HTTPS: when you need to `git push`, extra authentication is required, such as browser login or a token
- SSH: relies on a local SSH key and the corresponding GitHub public key configuration

In general, the second option is preferred: configure an SSH key and use Git that way.

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

Here, `origin` is the default remote name, followed by the remote repository URL. If you have multiple remote repositories, they will all be listed here.

### Change Remote URL

If the repository name on GitHub changes, or if you want to switch the remote from HTTPS to SSH, you can use the following command to change the remote repository URL:

```shell
git remote set-url origin https://github.com/username/new-repo-name.git
# or
git remote set-url origin git@github.com:username/new-repo-name.git
```

# Appendix

## .gitignore file

Sometimes we do not want to commit every file to the remote repo. For example, when running a Python program, temporary files such as `__pycache__` are generated, and we usually do not want to commit those temporary files.

In that case, we can write a `.gitignore` file to ignore specific files.

### Global ignore

For convenience, I usually use a global ignore file, so I do not need to configure one in every repository. I just need to go to `~` (the user home directory),

then create a `.gitignore` file and configure Git to use this global file.

```shell
cd ~
git config --global core.excludesfile ~/.gitignore
```

### personal `.gitignore`

```gitignore
# python auto generated file
__pycache__/
*.pyc

# local environment, such as token, password etc
.env
# nging basic auth user-password file
.htpasswd

# pytest-cov file
.coverage

# ignore tf related file
# terraform cahce file
.terraform/
# terraform status file
terraform.tfstate
# sensitive data
terraform.tfvars
```

## case sensitivity(windows)

In Windows, the file system is case-insensitive. That means files such as `apg-multi-waf.md` and `apg-multi-waf.MD` are treated as the same file.

But in Linux, file names are case-sensitive. I personally also prefer case sensitivity. Although you cannot change the entire Windows operating system to be case-sensitive, for Git on Windows you can configure it.

First, use the following command to check whether the current repository is case-sensitive:

```powershell
> git config core.ignorecase
true
```

If it is `true`, that means case-insensitive behavior is enabled, so you need to set it to `false`:

```powershell
> git config core.ignorecase false
```

After that, it can be recognized correctly:

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
