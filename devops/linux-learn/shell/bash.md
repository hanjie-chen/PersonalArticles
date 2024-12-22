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