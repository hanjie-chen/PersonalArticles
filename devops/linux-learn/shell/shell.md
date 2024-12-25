shell 和 bash 的关系：

- `sh`（Bourne Shell）是由 Stephen Bourne 在 1979 年为 Unix 开发的原始 shell
- `bash`（Bourne Again Shell）是 `sh` 的增强版本，由 GNU 项目开发，发布于 1989 年



在现代 Linux 系统中，`/bin/sh` 通常是指向某个具体 shell 实现的符号链接，可能指向：
- bash
- dash
- ash（BusyBox 中的实现，Alpine 使用这个）
- 其他 shell 实现



# system vs user

当我们使用命令 `ls -l /bin/sh` 查看默认的shell的时候，就会发现，对于 ubuntu 则是 dash

```shell
Plain@Linux-VM:~$ ls -l /bin/sh
lrwxrwxrwx 1 root root 4 Jun 14  2024 /bin/sh -> dash
```

而当我们 echo SHELL 变量的时候，则是bash

```shell
Plain@Linux-VM:~$ echo $SHELL
/bin/bash
```

这是为什么呢？，因为这里的两个 shell 是用于不同目的的：

**登录 Shell（$SHELL）- bash**

- 这是用户登录时使用的交互式 shell
- 通常配置在 `/etc/passwd` 中
- 提供更丰富的交互特性（命令历史、自动补全等）

**系统 Shell（/bin/sh）- dash**

- 这是系统脚本使用的默认 shell
- 主要用于执行脚本
- 更轻量级，启动更快
- 在您的系统中是 `/bin/dash`

验证方法：
```bash
# 查看当前用户的默认 shell
cat /etc/passwd | grep $USER

# 查看系统 shell
ls -l /bin/sh

# 查看当前使用的 shell
echo $SHELL
```

为什么要这样设计？
1. **性能考虑**
   - `dash` 更轻量级，启动更快
   - 系统脚本使用 `dash` 可以提高系统启动速度
   - 大多数系统脚本只需要基本的 POSIX shell 功能

2. **用户体验**
   - `bash` 提供更好的交互体验
   - 包含命令历史、自动补全等特性
   - 适合日常使用和交互式操作

3. **实际应用**
```bash
# 脚本中使用 dash
#!/bin/sh           # 使用系统默认 shell（dash）
echo "Hello World"

# 脚本中明确使用 bash
#!/bin/bash         # 明确使用 bash
echo "Hello World"

# 交互式使用
$ bash             # 启动交互式 bash shell
```

所以总结：
- `/bin/sh -> dash`：用于系统脚本，追求效率
- `$SHELL = /bin/bash`：用于用户交互，追求功能丰富
- 这种设计既保证了系统脚本的高效执行，又不影响用户的使用体验

这也是为什么在写脚本时，如果不需要 bash 特有的功能，建议使用 `#!/bin/sh`，这样可以在不同系统上获得更好的兼容性和性能。如果需要 bash 特有功能，才使用 `#!/bin/bash`。