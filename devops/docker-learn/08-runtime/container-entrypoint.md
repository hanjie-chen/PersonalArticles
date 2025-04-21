---
Title: 容器中的 PID 1、exec 和 crond 的那些坑
Author: 陈翰杰
Instructor: chatGPT 4o
CoverImage: 
RolloutDate: 
---

```
BriefIntroduction: 
容器中的 Entrypoint 与 PID 1 问题：以 Alpine crond 为例
在容器中运行服务时，我们经常会在 Dockerfile 或启动脚本中使用 `ENTRYPOINT` 或 `CMD` 来指定默认的启动命令。然而，如果我们直接使用 `exec crond -f` 启动 `crond`，可能会遇到如下报错：
setpgid: Operation not permitted
这个问题与 Linux 中的 PID 1 特性有关。本文将结合我的项目实践，讲解容器中与进程管理相关的一些坑和最佳实践。
```

<!-- split -->

# 背景：容器报错 `setpgid`

今天遇到一个问题，当我使用 `docker compose up` 的时候容器报错 `setpgid` 然后退出。详细情况如下

在我设计的一个容器中（基于 Alpine Linux 3.21），我运行一个同步 GitHub 仓库的脚本，并使用 `dcron` 来实现定时任务。出于“最小权限原则”，我没有使用 root 用户，而是创建了非特权用户 `appuser` 来运行容器。

这是容器的 dockerfile

```dockerfile
FROM alpine:3.21

# define the args for the user/group IDs, can pass these in compose.yml or docker run command
ARG USER_ID=1000
ARG GROUP_ID=1000

# install git, dcron, logrotate
RUN apk add --no-cache git dcron logrotate

# create a group(appgroup) and user(appuser) with args
RUN addgroup -g ${GROUP_ID} -S appgroup && \
    adduser -u ${USER_ID} -S appuser -G appgroup

# create log directory, change the dir owner to appuser
RUN mkdir -p /var/log/personal-website && \
    chown appuser:appgroup /var/log/personal-website

# create logrotate dir and copy file
COPY logrotate.conf /etc/logrotate.d/personal-website

# create working dir and set permission to appuser
RUN mkdir -p /articles-data && chown appuser:appgroup /articles-data
WORKDIR /articles-data

# copy the scripts, provide the permission, and set cron jobs
COPY --chown=appuser:appgroup update-articles.sh init.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/update-articles.sh && \
    chmod +x /usr/local/bin/init.sh

# let appuser have permission to run crontab, crond command
RUN chmod o+x /usr/bin/crontab &&\
    chmod u+s /usr/sbin/crond  &&\
    chmod o+x /usr/sbin/crond

# switch the non-root user to run the script
USER appuser

ENTRYPOINT ["/usr/local/bin/init.sh"]
```

然后这是我的 init.sh

```shell
#!/bin/sh
set -e

ARTICLES_DIR="/articles-data"
GIT_LOG="/var/log/personal-website/articles-sync.log"
CROND_LOG="/var/log/personal-website/crond.log"
GITHUB_REPO="${GITHUB_REPO:-https://github.com/hanjie-chen/PersonalArticles.git}"
REPO_BRANCH="${REPO_BRANCH:-main}"

# record the time
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INIT] $1" | tee -a "$GIT_LOG"
}
# record the repo and branch message
log_message "Using GITHUB_REPO: $GITHUB_REPO"
log_message "Using REPO_BRANCH: $REPO_BRANCH"

# confirm the log dir and files exist
for log_file in "$GIT_LOG" "$CROND_LOG"; do
    if [ ! -d "$(dirname "$log_file")" ]; then
        mkdir -p "$(dirname "$log_file")"
    fi
    if [ ! -f "$log_file" ]; then
        touch "$log_file"
        chmod 644 "$log_file"
    fi
done

# initial the repo or update the repo
if [ -z "$(ls -A $ARTICLES_DIR)" ]; then
    log_message "Initializing articles directory..."
    if ! git clone "$GITHUB_REPO" -b "$REPO_BRANCH" "$ARTICLES_DIR"; then
        log_message "Git clone failed"
        exit 1
    fi
    log_message "Repository cloned successfully"
else
    log_message "Articles directory exists, performing update..."
    if ! /usr/local/bin/update-articles.sh; then
        log_message "run update-articles.sh scripts failed"
        exit 1
    fi
fi

# Create a temporary crontab file
cat << EOF > /tmp/crontab
0 16 * * * /usr/local/bin/update-articles.sh >> /var/log/personal-website/articles-sync.log 2>&1
0 2 * * * /usr/sbin/logrotate /etc/logrotate.d/personal-website
EOF

# Install crontab for appuser, then delete it
crontab /tmp/crontab
rm /tmp/crontab

# 设置 umask
umask 022

# set crond as main process
exec crond -f -L "$CROND_LOG" -l 6
```

可以看到在 `init.sh` 最后一行中，我尝试使用如下方式启动 `crond`：

```shell
exec crond -f -L "$CROND_LOG" -l 6
```

但是当我使用 `docker compose up` 的时候，articles-sync container 发生了如下的报错

```shell
articles-sync      | setpgid: Operation not permitted
articles-sync exited with code 1
```

## resolution

咨询了 gpt4o 之后，他的建议是使用 `tini` 或者干脆删除 `exec`

这2中方案我都尝试，都有效，但这是为什么呢？



# 深入原理：容器中的 PID 1 有什么特别？

这个问题背后的核心，其实是跟 Linux & container 中 PID 1（即主进程）如何处理子进程 & 信号 有关，而不是你写的 shell 或 `crond` 本身的逻辑问题。

我们来一波深层解析：为什么 `exec` 会出问题，而 `tini` 或普通调用没事？

## 使用 `exec` 带来的问题

```sh
exec crond -f ...
```

`exec` 指令会把当前 shell（比如 `init.sh`）替换成 `crond`，让它成为容器的 PID 1；

接着就会进入到 `crond` 初始化

## `crond` 初始化逻辑

`crond` 在启动时会尝试执行一套「传统守护进程」初始化逻辑：

它通常会做这些事（简化守护进程标准流程）：

1. `fork()` 一个子进程 → 主进程退出 → 子进程成为“孤儿”进程（由 PID 1 管理）
2. `setsid()` → 脱离控制终端，成为新的 session leader
3. `setpgid()` → 设置自己的进程组（pgid）
4. `chdir("/")`、关闭标准输入输出等，彻底“脱离用户空间”

但是在容器里：它本来就是 PID 1（没有爹可以“脱身”给）

如果不是 root 权限，又试图调用 `setpgid()` 或 `setsid()`，就会遇到：

```shell
setpgid: Operation not permitted
```

这是 POSIX/Linux 的安全限制：只有某些权限进程（尤其是 非 PID 1 或 root）才能做这些操作。

这是因为在 container 中 PID 1 的进程非常特别



## PID 1 在容器中的“特权”与陷阱

容器内的第一个进程（PID 1）具有特殊行为：

1. 不会继承 Linux 默认信号处理逻辑（例如 SIGTERM）
2. 不会自动 reap 僵尸子进程
3. 有些系统调用行为（如 `setpgid`）在非特权用户下执行时会失败

在这个案例中：

非特权用户 `appuser` 运行 `crond -f` ， `crond` 默认会尝试设定自己的进程组（`setpgid(0, 0)`）然而，因为它是容器中的 PID 1 且不是 root，这个系统调用会被拒绝，导致失败退出



# 最佳实践：怎么优雅地解决？



## 方法一：去掉 exec（简单粗暴）

原来：

```sh
exec crond -f -L "$CROND_LOG"
```

修改为：

```sh
crond -f -L "$CROND_LOG"
```

这样，`crond` 就是子进程，shell 脚本成为容器的 PID 1

### 原理

让 shell 脚本继续作为 PID 1，而 `crond` 是它的子进程，crond 就不会尝试去处理自己变成“会话领导者”等操作。

也就是说，它会表现得更乖巧，不触发 setpgid 的高权限要求。



## 方法二：引入 tini（业界标准）

`tini` 是一个专为容器设计的最小 init system，它能：

1. 作为 PID 1，替你做信号转发和子进程管理（reap zombies）；
2. 不会像 shell 脚本那样半吊子处理容器生命周期；
3. 确保你交给它的 app（如 `init.sh`）在一个正确、安全的“容器环境”里运行。

也就是说，你可以放心地 `exec crond`，因为 tini 在上层兜底处理了容器的“初始化”逻辑。





## 总结对比：`exec` vs `非 exec` vs `tini`

| 方法                | 是否为 PID 1          | 是否推荐    | 原因                            |
| ------------------- | --------------------- | ----------- | ------------------------------- |
| `exec crond`        | 是                    | ❌ 不推荐    | 容易触发 `setpgid` 等权限错误   |
| `crond`（不 exec）  | 否                    | ✅ 可接受    | 避免让 `crond` 成为 PID 1，稳定 |
| `tini + exec crond` | 否（PID 1 是 `tini`） | ✅✅ 强烈推荐 | 最标准、安全的容器启动方式      |



# 实战：我的 Dockerfile 最终长这样

Dockerfile 加这一行安装 tini：

```dockerfile
RUN apk add --no-cache tini
```

然后在 Dockerfile 结尾加：

```dockerfile
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["/usr/local/bin/init.sh"]
```

这样你就能安心用 `exec crond` 了，而且容器生命周期也更优雅。



# continue

https://chatgpt.com/share/68066773-3260-800a-ab15-acd74b910cb2

