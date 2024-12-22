# cron 定时任务

cron 是 Linux 系统中用于执行定时任务的守护进程，它可以让用户在固定的时间间隔执行指定的系统指令或 shell 脚本。

## crontab 命令
crontab 是管理 cron 任务的主要命令：
```bash
crontab -l  # 列出当前用户的定时任务
crontab -e  # 编辑定时任务
crontab -r  # 删除所有定时任务
```

## create cron task

以创建一个定时 git pull 的 task 为例，假设仓库在 `/home/user/myproject`

### Step 1

创建一个脚本文件来执行 task， 例如git pull 脚本

```bash
# 创建脚本文件
vim /home/user/git-pull-script.sh
```

```bash
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

```bash
# 添加执行权限
chmod +x /home/user/git-pull-script.sh
```

### Step 2

```bash
# 编辑 crontab 添加定时任务
crontab -e
```

```bash
# 每天 UTC+0 16点 执行脚本
0 16 * * * /home/user/git-pull-script.sh
```

### Step 3

检查 crontab 是否正确设置

```
crontab -l
```



## cron grammer

cron 表达式由 5 个时间字段和一个命令字段组成：
```
* * * * * command
│ │ │ │ │
│ │ │ │ └─ 星期几 (0-7, 0和7都表示周日)
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

for example

**每隔 5 分钟执行一次**

```bash
*/5 * * * * /path/to/script.sh
```

**每天凌晨 1 点执行**

```bash
0 1 * * * /path/to/script.sh
```

3. *每周一至周五的上午 8 点执行**
```bash
0 8 * * 1-5 /path/to/script.sh
```

4. **每月 1 号和 15 号的上午 10 点执行**
```bash
0 10 1,15 * * /path/to/script.sh
```



## system file
除了用户级的 crontab，系统还有以下特殊目录：
```
/etc/cron.d/      # 系统定时任务配置文件
/etc/cron.daily/  # 每天执行的脚本
/etc/cron.hourly/ # 每小时执行的脚本
/etc/cron.monthly/# 每月执行的脚本
/etc/cron.weekly/ # 每周执行的脚本
```





## 环境变量

cron 任务执行时的环境变量与普通 shell 不同，是在一个受限的环境中运行的，所以最好使用完整的路径，并将所有必要的环境变量都明确设置

如果需要使用特定的环境变量，可以在 crontab 中添加：

```bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
HOME=/home/user
# 然后再添加你的定时任务
0 16 * * * /home/user/git-pull-script.sh
```



## check system log

```bash
sudo tail -f /var/log/syslog | grep CRON
```

