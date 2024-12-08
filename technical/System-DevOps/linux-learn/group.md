# Linux group





## `group` command

`groups` 命令默认显示当前登录用户所属的所有用户组 for example

```bash
$ groups
Plain adm dialout cdrom floppy sudo audio dip video plugdev netdev lxd
```

`Plain` 这是您的主要用户组，通常与用户名相同

`adm` 系统管理组，可以查看系统日志

`dialout` 允许访问串行端口设备

`cdrom` 允许访问光驱设备

`floppy` 允许访问软盘驱动器

`sudo` 允许使用 sudo 命令执行管理员权限的操作

`audio` 允许访问音频设备

`dip` 允许配置网络接口

`video` 允许访问视频设备

`plugdev` 允许访问可移动设备

`netdev` 允许管理网络设备

`lxd` 允许使用 LXD 容器管理系统



# 查看某个特定的 group 是否存在

可以使用 `cat /etc/group | grep <group-name>` 命令，例如，如果想要查看 docker group 是否存在

```bash
$cat /etc/group | grep docker
docker:x:993:
```

这个输出包含了4个字段，用冒号分隔：

`docker` group name

`x` 组密码占位符（现代系统通常使用影子密码系统，实际密码存储在别处）

`993` group ID (GID)

`<empty>` 最后一个空字段是组成员列表（当前是空的，说明没有用户被添加到这个组）

所以这个输出意味着 docker 组确实存在，但是目前没有任何用户被添加到这个组中

# 添加用户到某一个 group

可以使用命令 `sudo usermod -aG <group-name> <username>` 将用户添加到 group 中，例如将 Plain 用户添加到 docker group 中

```bash
$ sudo usermod -aG docker Plain
$ cat /etc/group | grep docker
docker:x:993:Plain
```

`usermod` - 修改用户账户的命令

`-a` 表示 append，即追加，如果不使用 `-a`，用户会从原来所属的其他组中被移除

`-G` 表示要修改的是用户组（Groups）



执行后，重新登录或运行 `newgrp docker`，然后再次运行 `groups` 命令，您应该就能看到 `docker` 组出现在列表中了。



> [!note]
>
> 将用户添加到 docker 组本质上是授予该用户 root 权限，因为用户可以使用 docker 命令来挂载任何目录并修改系统文件。
>
> 所以在这之后用户运行 docker 命令就无需添加 sudo

# 关于 `newgrp`

`newgrp docker` 命令的作用是在当前会话中切换用户的主要组（primary group）到指定的组（这里是 docker 组），而不需要完全注销并重新登录。让我详细解释一下：

### 工作原理

1. **临时切换主组**
   - 当您登录系统时，您会获得一组初始的组成员资格
   - `newgrp` 命令会启动一个新的 shell，在这个新 shell 中将指定的组（docker）设置为您的主要组
   - 这个改变只影响新启动的 shell 会话

2. **立即生效**
   - 通常添加用户到新组（通过 `usermod -aG`）后需要重新登录才能生效
   - 使用 `newgrp` 可以立即在当前会话中应用新的组权限，而不需要注销重新登录

### 验证方式

您可以通过以下方式观察 `newgrp` 的效果：

1. 执行前：
```bash
id
# 查看当前组信息
```

2. 执行 `newgrp docker`

3. 执行后：
```bash
id
# 可以看到 docker 组已经生效
```

### 实际应用场景

在您的情况下：
1. 您先使用 `usermod -aG docker $USER` 将用户添加到 docker 组
2. 然后使用 `newgrp docker` 立即激活这个组成员资格
3. 这样您就可以立即开始使用 docker 命令，而不需要注销重新登录

需要注意的是：
- `newgrp` 的效果只对当前终端会话有效
- 如果您打开新的终端窗口，可能需要再次运行 `newgrp docker` 或直接重新登录
- 完全注销并重新登录后，新的组成员资格会自动应用到所有新会话中

这就是为什么在长期使用中，建议完全注销并重新登录，但在需要立即使用新组权限的情况下，`newgrp` 是一个很好的临时解决方案。

# `sudo usermod -aG docker Plain`：

### 命令拆解

1. **sudo**
   - 以超级用户（root）权限运行后面的命令
   - 修改用户属性需要管理员权限

2. **usermod**
   - user modify 的缩写
   - 这是一个用于修改用户账户属性的命令
   - 可以修改用户名、家目录、shell、组成员资格等

3. **-aG** 参数
   - 这里组合了两个参数：
     - `-a`：append（追加）的意思，表示添加到组，而不是替换现有的组
     - `-G`：指定要添加的附加组（supplementary groups）
   - 重要：如果不使用 `-a`，只使用 `-G`，会删除用户原有的所有附加组！

4. **docker**
   - 要添加用户到的目标组名

5. **Plain**
   - 要修改的用户名

### 实际效果

这个命令会：
1. 保留用户 Plain 当前所在的所有组
2. 将用户 Plain 添加到 docker 组
3. 不会影响用户的主组（primary group）

### 对比不同用法

1. 错误用法（危险！）：
```bash
sudo usermod -G docker Plain  # 没有 -a 参数
```
这会删除用户 Plain 的所有现有附加组，只保留 docker 组

2. 正确用法：
```bash
sudo usermod -aG docker Plain  # 有 -a 参数
```
这会保留所有现有组，并添加 docker 组

### 验证方法

执行命令前后可以使用以下命令验证效果：
```bash
# 查看用户的组成员资格
groups Plain

# 或者使用 id 命令查看更详细信息
id Plain

# 直接查看 /etc/group 文件中的 docker 组
grep docker /etc/group
```

### 注意事项

1. 需要 sudo 权限执行
2. 必须使用 `-a` 参数来追加组
3. 修改后需要：
   - 使用 `newgrp docker` 立即在当前会话生效
   - 或者注销并重新登录使所有会话生效
4. 可以同时添加多个组：
```bash
sudo usermod -aG docker,group2,group3 Plain
```

这就是为什么这个命令被广泛用于 Docker 安装后的权限配置 - 它安全且有效地将用户添加到 docker 组，使其能够不使用 sudo 就运行 docker 命令。