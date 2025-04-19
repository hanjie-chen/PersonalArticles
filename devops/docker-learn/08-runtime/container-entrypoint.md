# Docker 容器中的 PID 1、exec 和 crond 的那些坑

预计的文章结构：
```makrdown
# Docker 容器中的 PID 1、exec 和 crond 的那些坑

## 一、背景：我的容器为何会报 setpgid 错误？
- 错误现象
- 初步排查过程

## 二、深入原理：容器中的 PID 1 有什么特别？
- signal 不转发
- setpgid 报错的原因
- 为何 exec 会出问题？

## 三、最佳实践：怎么优雅地解决？
- 方法一：去掉 exec（简单粗暴）
- 方法二：引入 tini（业界标准）

## 四、实战：我的 Dockerfile 最终长这样
- dockerfile 示例
- init.sh 示例
- 使用 tini 的配置方式

## 五、小结
- 容器内主进程管理的重要性
- tini 是什么，为什么推荐它
```

## 一、背景：我的容器为何会报 setpgid 错误？

今天遇到一个问题，首先这是我的 dockerfile

在我设计的一个容器中（基于 Alpine Linux 3.21），我运行一个同步 GitHub 仓库的脚本，并使用 `dcron` 来实现定时任务。出于“最小权限原则”，我没有使用 root 用户，而是创建了非特权用户 `appuser` 来运行容器。

```dockerfile
FROM alpine:3.21

# define the args for the user/group IDs, can pass these in compose.yml or docker run command
ARG USER_ID=1000
ARG GROUP_ID=1000

# install git, dcron, logrotate, tini
RUN apk add --no-cache git dcron logrotate tini

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

然后这时我的 init.sh

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

在 `init.sh` 中，我尝试使用如下方式启动 crond：

```shell
exec crond -f -L "$CROND_LOG" -l 6
```



但是当我使用 `docker compose up` 的时候报错，发生了如下的报错

```shell
articles-sync      | setpgid: Operation not permitted
articles-sync exited with code 1
```



这个问题背后的核心，其实是跟 Linux 中 PID 1（即主进程）如何处理子进程 & 信号 有关，而不是你写的 shell 或 `crond` 本身的逻辑问题。

我们来一波深层解析：为什么 `exec` 会出问题，而 `tini` 或普通调用没事？



## 🧠 背后原理：PID 1 在容器中的“特权”与陷阱

在 Linux 里：

- 每个进程都有一个父进程，负责“收尸”（回收资源）；

- 如果你用了 `exec`，你会把当前 shell（比如 `init.sh`）替换成 `crond`，让它成为容器的 PID 1；

- 但！！在容器里，**PID 1 是一个特别的存在**：

  > 它不会自动转发信号、不会自动 reap 子进程，甚至可能没有完整的权限去做某些系统调用，比如 `setpgid()`。

而 `crond` 是一个老派的守护进程，**它会尝试做一些跟会话/进程组相关的操作**（比如设置它自己为新的会话组 leader、detach terminal、重定向 fd 等），这些操作在 root 以外或者非正常 PID 1 环境下会触发报错。

------

## 💥 使用 `exec` 带来的问题

```sh
exec crond -f ...
```

- 这条命令会让 `crond` 变成 **PID 1**；

- `crond` 作为 PID 1 时执行 `setpgid()`（设置进程组 ID）就可能报：

  ```
  setpgid: Operation not permitted
  ```

  因为它没有 fork 一个子进程，而自己是容器的最顶层。

------

## ✅ 为什么 **去掉 `exec`** 就好了？

当你：

```sh
crond -f ...
```

你让 shell 脚本继续作为 PID 1，而 `crond` 是它的子进程，crond 就不会尝试去处理自己变成“会话领导者”等操作。

也就是说，它会表现得 **更乖巧，不触发 setpgid 的高权限要求**。

------

## 🛟 为什么 **使用 `tini`** 能彻底解决这类问题？

`tini` 是一个超级轻量的 init system，它能：

1. **作为 PID 1**，替你做信号转发和子进程管理（reap zombies）；
2. 不会像 shell 脚本那样半吊子处理容器生命周期；
3. 确保你交给它的 app（如 `init.sh`）在一个正确、安全的“容器环境”里运行。

也就是说，**你可以放心地 `exec crond`，因为 tini 在上层兜底处理了容器的“初始化”逻辑。**

------

## 📊 总结对比：`exec` vs `非 exec` vs `tini`

| 方法                | 是否为 PID 1          | 是否推荐    | 原因                            |
| ------------------- | --------------------- | ----------- | ------------------------------- |
| `exec crond`        | 是                    | ❌ 不推荐    | 容易触发 `setpgid` 等权限错误   |
| `crond`（不 exec）  | 否                    | ✅ 可接受    | 避免让 `crond` 成为 PID 1，稳定 |
| `tini + exec crond` | 否（PID 1 是 `tini`） | ✅✅ 强烈推荐 | 最标准、安全的容器启动方式      |

------

## 🧪 你该怎么选？

| 场景                                       | 建议                               |
| ------------------------------------------ | ---------------------------------- |
| 想稳定跑 `cron` + 非 root 用户             | ✅ 加 `tini` 最安全                 |
| 脚本里就一两个命令，不想额外加 tini        | ✅ 不用 `exec`，让 shell 管理子进程 |
| 想优雅处理容器退出、信号转发（SIGTERM 等） | ✅ `tini` 是行业标准                |

------

## ✅ 如何加 tini（最终建议）

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



# 容器中的 Entrypoint 与 PID 1 问题：以 Alpine crond 为例

在容器中运行服务时，我们经常会在 Dockerfile 或启动脚本中使用 `ENTRYPOINT` 或 `CMD` 来指定默认的启动命令。然而，如果我们直接使用 `exec crond -f` 启动 `crond`，可能会遇到如下报错：

```
setpgid: Operation not permitted
```

这个问题与 Linux 中的 **PID 1 特性** 有关。本文将结合我的项目实践，讲解容器中与进程管理相关的一些坑和最佳实践。

## 原因分析：PID 1 与信号管理

### 容器内的第一个进程（PID 1）具有特殊行为：

1. **不会继承 Linux 默认信号处理逻辑**（例如 SIGTERM）
2. **不会自动 reap 僵尸子进程**
3. **有些系统调用行为（如 `setpgid`）在非特权用户下执行时会失败**

在我的案例中：

- 非特权用户 `appuser` 运行 `crond -f`
- `crond` 默认会尝试设定自己的进程组（`setpgid(0, 0)`）
- 然而，因为它是容器中的 **PID 1 且不是 root**，这个系统调用会被拒绝，导致失败退出

------

## 解决方案

### ✅ 方法一：**不要使用 `exec`**

原来：

```sh
exec crond -f -L "$CROND_LOG"
```

修改为：

```sh
crond -f -L "$CROND_LOG"
```

- 这样，`crond` 就是子进程，不是 PID 1
- shell 脚本成为容器的 PID 1，问题解决
- 缺点：shell 脚本要负责转发信号 & reap 僵尸进程

### ✅ 方法二：**使用 tini 或 dumb-init**

tini 是一个专为容器设计的最小 init system，可以正确处理信号、僵尸进程、`setpgid` 等问题。

在 Dockerfile 中加一行安装 tini，并修改 ENTRYPOINT：

```Dockerfile
RUN apk add --no-cache tini
ENTRYPOINT ["/sbin/tini", "--", "/usr/local/bin/init.sh"]
```

使用 tini 后：

- 容器内 PID 1 是 tini
- `init.sh` 成为子进程
- `crond` 也不会是 PID 1
- 所有信号和子进程管理问题都自动解决

------

## 总结：容器内进程管理建议

| 问题                               | 原因                             | 解决方式                 |
| ---------------------------------- | -------------------------------- | ------------------------ |
| `setpgid: Operation not permitted` | 非 root PID 1 尝试设置进程组失败 | 使用 tini，或不使用 exec |
| 容器收到 SIGTERM 不退出            | PID 1 默认不处理信号             | 用 tini，或自己转发信号  |
| 僵尸进程积累                       | PID 1 不 reap 子进程             | 用 tini，或 trap SIGCHLD |

