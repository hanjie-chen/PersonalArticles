# 重定向符号 (Redirection Operator)

## redirect append operator

在 shell 中，`>>` 被称为重定向追加符号 (redirection append operator)。它的作用是将命令的输出追加到一个文件中。具体来说:

- 如果该文件不存在，则创建该文件
- 如果该文件已存在，则将命令的输出追加到文件的末尾，而不是覆盖文件原有的内容

例如:

```bash
echo "Hello, world!" >> output.txt
```

这个命令会将 "Hello, world!" 追加写入到 output.txt 文件中。如果 output.txt 文件不存在，则会创建该文件。

## redirect operator

与 `>>` 对应的是 `>` 重定向符号，它会将命令的输出覆盖写入到文件中，而不是追加。例如:

```bash
echo "Hello, world!" > output.txt
```

这个命令会将 "Hello, world!" 写入到 output.txt 文件中，如果该文件已存在，则会覆盖文件原有的内容。所以 `>>` 和 `>` 的区别在于，`>>` 是追加写入，`>` 是覆盖写入。

## practice

在我们的 `init.sh` 脚本中，如果使用了以下方式添加定时任务：

```cpp
echo "0 16 * * * /usr/local/bin/update-articles.sh >> $GIT_LOG 2>&1" >> /etc/crontabs/root
echo "0 2 * * * /usr/sbin/logrotate /etc/logrotate.d/personal-website" >> /etc/crontabs/root
```

这里使用了 `>>` 操作符，这意味着每次运行脚本时，这些定时任务都会被添加到 `crontab` 文件的末尾。

如果容器多次启动（例如开启了 docker compose watch）或脚本多次运行，`crontab` 文件中就会累积多个相同的定时任务。结果是，在同一时间点上，多个相同的任务会同时运行，导致我们之前看到的 Git 锁冲突的问题。

```shell
==> /var/log/personal-website/articles-sync.log <==
[2025-01-12 16:00:01] [SYNC] Starting articles synchronization
[2025-01-12 16:00:01] [SYNC] Starting articles synchronization
[2025-01-12 16:00:01] [SYNC] Starting articles synchronization
From https://github.com/hanjie-chen/PersonalArticles
 * branch            main       -> FETCH_HEAD
From https://github.com/hanjie-chen/PersonalArticles
 * branch            main       -> FETCH_HEAD
From https://github.com/hanjie-chen/PersonalArticles
 * branch            main       -> FETCH_HEAD
   617341c..9b8e5a3  main       -> origin/main
error: cannot lock ref 'refs/remotes/origin/main': is at 9b8e5a39e084b47ddbd6e11eea80cc4accb35767 but expected 617341c8d28797bded2da6b6ec1e11be8112aa24
 ! 617341c..9b8e5a3  main       -> origin/main  (unable to update local ref)
error: cannot lock ref 'refs/remotes/origin/main': is at 9b8e5a39e084b47ddbd6e11eea80cc4accb35767 but expected 617341c8d28797bded2da6b6ec1e11be8112aa24
 ! 617341c..9b8e5a3  main       -> origin/main  (unable to update local ref)
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
[2025-01-12 16:00:01] [SYNC] Git pull failed
[2025-01-12 16:00:01] [SYNC] Git pull failed
[2025-01-12 16:00:01] [SYNC] Git pull failed
```

### resolution

为了防止定时任务被重复添加，我们需要确保每次脚本运行时，`crontab` 文件中的定时任务是唯一的，不会重复。这可以通过覆盖 `crontab` 文件来实现，而不是每次都向其中追加内容。

```shell
cat << EOF > /etc/crontabs/root
0 16 * * * /usr/local/bin/update-articles.sh >> $GIT_LOG 2>&1
0 2 * * * /usr/sbin/logrotate /etc/logrotate.d/personal-website
EOF
```

**`cat << EOF`**：表示开始一个 Here Document，接下来直到 `EOF` 之间的内容将作为 `cat` 命令的输入。

**`>` `/etc/crontabs/root`**：将 `cat` 命令的输出（即以上多行内容）**重定向**到 `/etc/crontabs/root` 文件。由于使用的是 `>`，这将**覆盖**文件中的原有内容。

**`EOF`**：表示 Here Document 的结束。



# 关于 `2>&1` 重定向

先看这个 bash 脚本

```
#!/bin/bash

# 记录时间
echo "=== Git pull started at $(date) ===" >> /home/user/git-pull.log

# 切换到仓库目录
cd /home/user/myproject

# 执行 git pull
/usr/bin/git pull >> /home/user/git-pull.log 2>&1

# 记录完成状态
echo "=== Git pull completed at $(date) ===" >> /home/user/git-pull.log
echo "----------------------------------------" >> /home/user/git-pull.log
```

在 Linux/Unix 系统中，每个进程默认都有三个标准流：

1. 标准输入（stdin）- 文件描述符为 0
2. 标准输出（stdout）- 文件描述符为 1
3. 标准错误（stderr）- 文件描述符为 2

在脚本中，`2>&1` 的具体含义是：

- `2>` 表示重定向标准错误（stderr）
- `&1` 表示引用标准输出（stdout）的文件描述符
- 组合起来就是：将标准错误重定向到标准输出所指向的位置

让我们分析你的具体例子：

```bash
/usr/bin/git pull >> /home/user/git-pull.log 2>&1
```

这行命令做了以下操作：

1. `>>` 将标准输出追加到 `/home/user/git-pull.log` 文件
2. `2>&1` 将标准错误也重定向到与标准输出相同的位置（即 git-pull.log）

这样做的好处是：

- 可以捕获所有输出，包括正常输出和错误信息
- 保证所有的日志信息都按照时间顺序记录在同一个文件中
- 不会遗漏任何错误信息

如果没有 `2>&1`：

- 正常输出会写入日志文件
- 错误信息会显示在终端上
- 可能会造成日志不完整

这是一个非常常用的重定向技巧，特别是在编写需要完整日志记录的脚本时。