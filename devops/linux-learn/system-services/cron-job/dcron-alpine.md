# Cron in Alpine Linux

如果 run alpine Linux 镜像，就会发现其实其实 alpine 自带 crontab 命令和一个简单的 crond (busybox)，

如果我们使用命令 `crontab -l` 查看，那么会得到这样子的结果

```shell
/ # crontab -l
# do daily/weekly/monthly maintenance
# min   hour    day     month   weekday command
*/15    *       *       *       *       run-parts /etc/periodic/15min
0       *       *       *       *       run-parts /etc/periodic/hourly
0       2       *       *       *       run-parts /etc/periodic/daily
0       3       *       *       6       run-parts /etc/periodic/weekly
0       5       1       *       *       run-parts /etc/periodic/monthly
```

这些默认 cron jobs 是 Alpine Linux 的系统维护任务，它们使用了 `run-parts` 命令来运行特定目录下的所有可执行文件

如果查看这些目录，就会发现他们是空的

```shell
/etc/periodic # tree
.
├── 15min
├── daily
├── hourly
├── monthly
└── weekly

5 directories, 0 files
```

如果想要添加自己的 cron jobs, 可以直接修改 `/etc/crontabs/root` 文件，这个文件是 `crontab -l` 命令的本质

> [!note]
>
> 这个 `/etc/crontabs/root` 文件，是 dcron 的系统级别文件，只有 root 权限才能写入
>
> 要尽量避免去写入这个文件，而是尽量使用用户级别的 `crontab` 来写入

```shell
/etc/crontabs # cat root
# do daily/weekly/monthly maintenance
# min   hour    day     month   weekday command
*/15    *       *       *       *       run-parts /etc/periodic/15min
0       *       *       *       *       run-parts /etc/periodic/hourly
0       2       *       *       *       run-parts /etc/periodic/daily
0       3       *       *       6       run-parts /etc/periodic/weekly
0       5       1       *       *       run-parts /etc/periodic/monthly
```

或者将自己的脚本放在对应的 periodic 目录即可



## crond in busybox

首先我们查看 alpine linux 中是否存在 crond

```shell
# which crond
/usr/sbin/crond
```

会发现其实存在，接着我们看看它来自哪里

```shell
# crond --help
BusyBox v1.37.0 (2025-01-17 18:12:01 UTC) multi-call binary.

Usage: crond [-fbS] [-l N] [-d N] [-L LOGFILE] [-c DIR]

        -f      Foreground
        -b      Background (default)
        -S      Log to syslog (default)
        -l N    Set log level. Most verbose 0, default 8
        -d N    Set log level, log to stderr
        -L FILE Log to FILE
        -c DIR  Cron dir. Default:/var/spool/cron/crontabs
```

说明这是 BusyBox 自带的 `crond`（极简实现）

## dcron (Dillon's Cron)

`dcron` 是一个特定的 cron 实现，由 Matt Dillon 编写

它是一个轻量级的 cron 守护进程实现，特别适合嵌入式系统和轻量级环境

## Dillon's Cron VS. busybox cron

这就引申出一个问题，那就是使用 `busybox` 自带的 `crond` 还是使用我们新安装的 `dcron`

### 选用 BusyBox 自带 `crond`：

- 适合 简单任务、极简容器（如定时 git pull）
- 不依赖日志系统，任务失败也不用详细排查
- 无需额外安装，占用更少空间



### 选用 `dcron`：

- 适合 正式部署环境 或 需要稳定日志记录/调试
- 想使用 Alpine 的 `/etc/periodic` 机制（依赖 run-parts）
- 更稳定、兼容性好，问题好排查



一句话原则：

- 想“能跑就行”：用 busybox 自带的
- 想“跑得稳、好排错”：就用 dcron

# 遗留问题：

但是这里会出现一个问题：

> 那就是如果我安装了 dcron, 那么当我使用命令：crond -f -l 8 的时候，我怎么知道启动的是哪一个 daemon 呢？是否会出现我安装了 dcron，但是当我使用命令 crond -f -l 8 的时候，运行的是 busybox 中的 crond 呢？
>
> 还需要继续调查一下

# How to use dcron in alpline linux

1. 首先需要安装 dcron 包：

```bash
apk add dcron
```

2. 然后可以编写定时任务：

```bash
# 使用 crontab 命令编辑
crontab -e

# 或直接编辑文件
echo "*/5 * * * * /my-script.sh" >> /etc/crontabs/root
```

3. 启动 crond 守护进程：

```bash
crond
```

### 在 Alpine Linux 中使用 dcron（以容器环境为例）

### 安装和配置：

```dockerfile
FROM alpine:3.19
RUN apk add --no-cache dcron
COPY crontab /etc/crontabs/root
CMD ["crond", "-f", "-d", "8"]
```

### 示例 crontab 文件：

```cron
*/5 * * * * /usr/local/bin/update-articles.sh >> /var/log/git-pull.log 2>&1
```

### 日志输出建议：

- 在 crontab 中使用重定向：捕获标准输出和错误信息
- 在脚本中写结构化日志：记录具体步骤与时间戳



