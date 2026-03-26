# Cron Job

cron 是 Linux 系统中用于执行定时任务的守护进程，它可以让用户在固定的时间间隔执行指定的系统指令或 shell 脚本。



## crontab command

`crontab` 是用于创建、编辑、查看和删除定时任务的命令行工具，用户通过 `crontab` 来定义定时任务。`crontab` 可以理解为“任务清单”的编辑器。

常用命令：

```bash
crontab -l  # 列出当前用户的定时任务
crontab -e  # 编辑当前用户的定时任务
crontab -r  # 删除当前用户的定时任务
```

### `crontab -u` command

用于以指定用户的身份编辑或管理定时任务（cron jobs）。这个命令通常需要 root 权限，因为普通用户只能管理自己的定时任务。

```bash
crontab -u <username> <operation> # 指定用户身份执行操作
```

`<operation>`：可以是 `-l`（列出）、`-e`（编辑）、`-r`（删除）。

例如，查看用户 `alice` 的定时任务列表：

```bash
sudo crontab -u alice -l
```

### `crontab <crontab-file>` command

```bash
crontab <crontab-file>
```

这个命令会把整个 `your-crontab-file` 的内容，作为当前用户的 crontab 来替换掉。

例如

```bash
cat <<EOF > /tmp/mycron
0 12 * * * echo "Hello from cron" >> /tmp/cron-test.log
EOF

crontab /tmp/mycron
```

- 上面会让当前用户每天中午 12 点执行一条 echo 命令。
- 原来通过 `crontab -e` 写的任务会被覆盖掉！

> [!note]
>
> 会完全覆盖当前用户原来的 crontab 内容！
>
> 如果你只是想“追加”任务，得先读出旧的，再加上新内容：
>
> ```bash
> crontab -l > mycron.old
> echo "0 12 * * * echo 'new task'" >> mycron.old
> crontab mycron.old
> ```
>
> 文件必须是标准 crontab 语法的格式，不支持 `crontab -e` 里某些特殊注释风格（比如 `@reboot` 等不是所有系统都支持）。
>
> 不要加 shebang（#!/bin/bash），这个文件不是脚本，是纯粹的定时任务列表。



## crond

`crond` 是系统后台的守护进程，负责定时检查 crontab 文件，并在指定时间点执行任务。

可以理解为：crontab 提供计划表，crond 是真正安排任务执行的“工人”。



## Cron in different OS

| 发行版        | 实现名称 | 特点                        |
| ------------- | -------- | --------------------------- |
| Alpine Linux  | dcron    | 轻量、资源占用小            |
| Debian/Ubuntu | cron     | 功能完整、稳定性高          |
| CentOS/RHEL   | cronie   | 企业特性强、支持 SELinux 等 |

配置文件位置对比：

```bash
# Alpine (dcron)
/etc/crontabs/root

# Debian/Ubuntu (cron)
/var/spool/cron/crontabs/
/etc/crontab

# CentOS (cronie)
/var/spool/cron/
/etc/cron.d/
```

基本的 crontab 语法在所有实现中都是兼容的，但高级特性可能不同

这些不同的 cron 实现都能完成基本的定时任务功能，选择哪个主要取决于你的具体需求和使用的 OS。在容器环境中，Alpine 的 dcron 因其轻量级特性通常是个不错的选择。

# cron expression syntax

cron 表达式由 5 个时间字段和一个命令字段组成：

```shell
* * * * * command
│ │ │ │ │
│ │ │ │ └─ 星期几 (0-7, 0 和 7 都表示周日)
│ │ │ └─── 月份 (1-12)
│ │ └───── 日期 (1-31)
│ └─────── 小时 (0-23)
└───────── 分钟 (0-59)
```

### 特殊字符说明：

- `*`: 表示任意值
- `,`: 表示列举，如 `1,3,5`
- `-`: 表示范围，如 `1-5`
- `/`: 表示间隔，如 `*/5`

### for example

每隔 5 分钟执行一次

```bash
*/5 * * * * /path/to/script.sh
```

每天凌晨 1 点执行

```bash
0 1 * * * /path/to/script.sh
```

每周一至周五的上午 8 点执行

```bash
0 8 * * 1-5 /path/to/script.sh
```

每月 1 号和 15 号的上午 10 点执行

```bash
0 10 1,15 * * /path/to/script.sh
```

## crontab 空格对齐

如果直接编辑 cron 配置文件， 例如使用echo 命令+ `>>` 重定向

```shell
echo "0 16 * * * /usr/local/bin/update-articles.sh" >> /etc/crontabs/root
```

就会发现可能和原来的格式并不相同

```shell
/usr/local/bin # crontab -l
# do daily/weekly/monthly maintenance
# min   hour    day     month   weekday command
*/15    *       *       *       *       run-parts /etc/periodic/15min
0       *       *       *       *       run-parts /etc/periodic/hourly
0       2       *       *       *       run-parts /etc/periodic/daily
0       3       *       *       6       run-parts /etc/periodic/weekly
0       5       1       *       *       run-parts /etc/periodic/monthly

0 16 * * * /usr/local/bin/update-articles.sh
```

但是 crontab 中的空格对齐不会影响执行。crontab 只关心字段之间是否有空格分隔，而不在意具体有多少个空格。以下这些写法都是等效的：

```bash
# 这些写法都是完全等效的
0 16 * * * /usr/local/bin/update-articles.sh
0     16          *    *    *     /usr/local/bin/update-articles.sh
0	16	*	*	*	/usr/local/bin/update-articles.sh  # 使用 tab
```

那些对齐的注释行（带有 # 的行）只是为了提高可读性，不影响实际执行。crontab 实际解析时会：

1. 忽略空行和注释行（以 # 开头的行）
2. 将每行按空格或制表符分割成 6 个字段（分钟、小时、日、月、星期、命令）
3. 只要字段之间有分隔符即可，分隔符的数量不重要

# system file

除了用户级的 crontab，系统还有以下特殊目录：

```
/etc/cron.d/      # 系统定时任务配置文件
/etc/cron.daily/  # 每天执行的脚本
/etc/cron.hourly/ # 每小时执行的脚本
/etc/cron.monthly/# 每月执行的脚本
/etc/cron.weekly/ # 每周执行的脚本
```



## check system log

```bash
sudo tail -f /var/log/syslog | grep CRON
```

# best practice

尽量使用用户级别的 cron jobs 而不要去修改系统级别的 cron 文件
