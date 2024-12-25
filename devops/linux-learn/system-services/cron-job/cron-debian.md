# cron 定时任务

cron 是 Linux 系统中用于执行定时任务的守护进程，它可以让用户在固定的时间间隔执行指定的系统指令或 shell 脚本。

## crontab 命令
crontab 是管理 cron 任务的主要命令：
```bash
crontab -l  # 列出当前用户的定时任务
crontab -e  # 编辑定时任务
crontab -r  # 删除所有定时任务
```

## create cron task (in interactive mode)

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

# create cron jobs (non interactive mode)

我来详细解释一下在非交互式环境下如何设置 cron jobs，这在自动化部署和容器化环境中特别有用。

## 直接写入 crontab 文件

可以使用 `crontab` 命令的重定向功能来添加 cron jobs：

```bash
echo "* * * * * /your/command" | crontab -
```

这里的 `-` 表示从标准输入读取内容。

## 使用文件导入

1. 首先创建一个包含 cron 配置的文件：
```bash
echo "* * * * * /your/command" > mycron
```

2. 然后将文件导入到 crontab：
```bash
crontab mycron
```

## 在 Dockerfile 中设置 cron jobs

在 Dockerfile 中设置 cron jobs 有几种常见方法：

#### 方法1：使用文件复制

```dockerfile
# 创建 cron 文件
COPY my-crontab /etc/cron.d/my-crontab

# 设置权限
RUN chmod 0644 /etc/cron.d/my-crontab

# 应用 cron 任务
RUN crontab /etc/cron.d/my-crontab
```

#### 方法2：直接在 Dockerfile 中写入

```dockerfile
RUN echo "* * * * * /your/command" > /etc/cron.d/my-crontab \
    && chmod 0644 /etc/cron.d/my-crontab \
    && crontab /etc/cron.d/my-crontab
```

### 4. 其他注意事项

1. **权限设置**：
   - cron 文件通常需要 0644 权限
   - 确保执行的脚本有适当的执行权限

2. **容器环境特殊考虑**：
   - 需要确保 cron 守护进程在容器中运行
   - 通常需要在容器启动命令中包含启动 cron 服务：
     ```dockerfile
     CMD ["cron", "-f"]
     ```
     或者在启动脚本中包含：
     ```bash
     service cron start
     ```

3. **完整的 Dockerfile 示例**：
```dockerfile
FROM ubuntu:20.04

# 安装 cron
RUN apt-get update && apt-get -y install cron

# 创建 cron 任务
RUN echo "* * * * * root echo 'Hello world' >> /var/log/cron.log 2>&1" > /etc/cron.d/hello-cron

# 给予适当权限
RUN chmod 0644 /etc/cron.d/hello-cron

# 创建日志文件
RUN touch /var/log/cron.log

# 应用 cron 任务
RUN crontab /etc/cron.d/hello-cron

# 启动 cron 服务
CMD ["cron", "-f"]
```

4. **查看当前 cron 任务**：
```bash
crontab -l
```

5. **删除所有 cron 任务**：
```bash
crontab -r
```

### 使用建议

2. 在容器环境中，确保所需的环境变量都正确设置
3. 考虑添加日志输出以便调试
4. 测试 cron 任务时，可以先在较短的时间间隔内测试
5. 确保时区设置正确，特别是在容器环境中

这些方法让你能够在自动化脚本、CI/CD 流程或容器化环境中轻松设置 cron jobs，而不需要交互式编辑器。选择哪种方法主要取决于你的具体使用场景和需求。

# cron grammer

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

### for example

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



# system file
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

