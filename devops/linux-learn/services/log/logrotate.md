# logrotate 详解

logrotate 是 Linux 系统中一个用于管理日志文件的工具，它可以自动对日志进行轮转（rotation）、压缩、删除等操作。它本身是一个命令行工具，但通常是通过 cron 任务定期执行的。



# config file and directory

```
系统级别
├── /etc/cron.daily/logrotate     # 执行脚本（决定何时运行）
└── Logrotate配置
    ├── /etc/logrotate.conf       # 主配置文件（全局设置）
    └── /etc/logrotate.d/         # 应用特定配置目录
        ├── nginx                 # nginx的日志轮转配置
        ├── apache2              # apache的日志轮转配置
        └── mysql                # mysql的日志轮转配置
```

### `/etc/cron.daily/logrotate`

这是一个**执行脚本**，不是配置文件。它的作用是：

- 定义 logrotate 程序的运行时间
- 由 cron 每天自动执行
- 调用 logrotate 命令来处理日志轮转

```bash
#!/bin/sh
/usr/sbin/logrotate /etc/logrotate.conf
```

### `/etc/logrotate.conf`

这是 logrotate 的**主配置文件**，用于设置全局默认参数：

- 定义默认的轮转策略
- 包含其他配置文件
- 可以包含一些基本日志的轮转规则

```conf
# 全局默认设置
weekly
rotate 4
create
dateext
compress

# 包含其他配置文件
include /etc/logrotate.d
```

### `/etc/logrotate.d/` index

这个目录包含**各个应用的具体配置文件**：

- 每个应用一个配置文件
- 可以覆盖全局设置
- 更容易管理和维护

例如 nginx 的配置 `/etc/logrotate.d/nginx`：

```conf
/var/log/nginx/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 nginx nginx
    sharedscripts
    postrotate
        [ -f /var/run/nginx.pid ] && kill -USR1 `cat /var/run/nginx.pid`
    endscript
}
```

### 配置优先级

1. **最低优先级**：`/etc/logrotate.conf` 中的全局设置
2. **高优先级**：`/etc/logrotate.d/` 目录下的具体应用配置

### 工作流程示例

1. **每天**，cron 执行 `/etc/cron.daily/logrotate` 脚本

2. **脚本调用** logrotate 命令，并指定主配置文件：

   ```bash
   /usr/sbin/logrotate /etc/logrotate.conf
   ```

3. **logrotate 处理配置**：

   - 首先读取 `/etc/logrotate.conf` 的全局设置
   - 通过 `include /etc/logrotate.d` 加载应用特定配置
   - 按照配置执行日志轮转



### 实际例子

假设系统中同时运行着 nginx 和 mysql：

1. **全局配置** `/etc/logrotate.conf`：

```conf
# 全局默认设置
weekly
rotate 4
create
dateext
compress

# 包含其他配置
include /etc/logrotate.d
```

2. **Nginx 配置** `/etc/logrotate.d/nginx`：

```conf
/var/log/nginx/*.log {
    daily           # 覆盖全局的 weekly 设置
    rotate 14       # 覆盖全局的 rotate 4 设置
    compress
    delaycompress
    notifempty
    create 0640 nginx nginx
}
```

3. **MySQL 配置** `/etc/logrotate.d/mysql`：

```conf
/var/log/mysql/*.log {
    monthly         # 覆盖全局的 weekly 设置
    rotate 6        # 覆盖全局的 rotate 4 设置
    compress
    create 0640 mysql mysql
}
```



# Log Rotation

日志轮转是一个自动管理日志文件的过程，主要目的是防止单个日志文件过大，同时保留历史日志记录。简单来说，就是将当前正在写入的日志文件转移为备份文件，并创建新的空日志文件继续记录。

e.g. 假设有一个 nginx 访问日志文件 `access.log`：

1. **初始状态**

```
/var/log/nginx/
└── access.log    # 当前正在写入的日志文件
```

2. **第一次轮转后**

```
/var/log/nginx/
├── access.log        # 新的空日志文件（继续写入）
└── access.log.1      # 昨天的日志
```

3. **第二次轮转后**

```
/var/log/nginx/
├── access.log        # 新的空日志文件（继续写入）
├── access.log.1      # 昨天的日志
└── access.log.2.gz   # 前天的日志（已压缩）
```

4. **如此循环**

```
/var/log/nginx/
├── access.log        # 新的空日志文件（继续写入）
├── access.log.1      # 最新的旧日志
├── access.log.2.gz   # 压缩的旧日志
├── access.log.3.gz   # 更旧的日志
└── access.log.4.gz   # 最旧的日志
```

# logrotate grammer

e.g.

`logrotate.conf`

```
# 基本设置
weekly
rotate 4
create
dateext

# 错误处理
missingok
notifempty

# 压缩设置
compress
delaycompress

# 包含其他配置
include /etc/logrotate.d
```

nginx.log in `/etc/logrotate.d`

```
/var/log/nginx/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 nginx nginx
    sharedscripts
    postrotate
        [ -f /var/run/nginx.pid ] && kill -USR1 `cat /var/run/nginx.pid`
    endscript
}
```

## grammer

path match

```conf
# 匹配 /var/log/personal-website/ 目录下所有 .log 结尾的文件
/var/log/personal-website/*.log
```

**轮转周期选项**

```conf
daily    # 每天
weekly   # 每周
monthly  # 每月
yearly   # 每年
```

强制在指定时间点进行轮转的条件，不管文件大小一定轮转

file size

```conf
size 100M      # 当日志达到100M时轮转
minsize 1M     # 最小1M才轮转
maxsize 100M   # 最大100M就必须轮转
```

3. **文件创建和权限**
```conf
create 0644 root root  # 创建新文件的权限、用户和组
nocreate             # 不创建新文件
```

backup file control

二选一即可

```conf
rotate 5    # 最多保留5个备份
maxage 60   # 最多保留60天的备份
```

`maxage` 只会作用于已经轮转的日志文件（即备份文件），不会删除当前正在使用的活动日志文件。

**压缩选项**

```conf
compress         # 压缩
nocompress      # 不压缩
compresscmd     # 指定压缩命令
compressext     # 压缩文件扩展名
delaycompress   # 延迟压缩
```

6. **错误处理**
```conf
missingok      # 丢失日志文件不报错
nomissingok    # 丢失日志文件报错
notifempty     # 空文件不轮转
ifempty        # 空文件也轮转
```

7. **脚本执行**
```conf
sharedscripts  # 当有多个日志文件匹配时（如 *.log），postrotate 脚本只执行一次
prerotate      # 轮转前执行的脚本
    命令
endscript

postrotate     # 轮转后执行的脚本
    命令
endscript
```

8. **日期扩展**
```conf
dateext              # 使用日期作为后缀
dateformat -%Y%m%d   # 日期格式
```

