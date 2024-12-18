# Linux group

group 是 Linux 系统中用于管理多个用户权限的一种机制。通过将用户分配到不同的组中，可以统一管理这些用户的访问权限。

组的类型

Primary Group：用户创建文件时默认使用的组

Supplementary Groups：用户所属的其他组

# group manage command

## `groups` command

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



## check group exist

可以使用 `cat /etc/group | grep <group-name>` 命令查看某个特定的组是否存在，例如，如果想要查看 docker group 是否存在

```bash
$cat /etc/group | grep docker
docker:x:993:
```

这个输出包含了4个字段，用冒号分隔：

`docker` group name

`x` 组密码占位符（现代系统通常使用影子密码系统，实际密码存储在别处）

`993` group ID (GID)

`<empty>` 最后一个空字段是组成员列表（当前是空的，说明没有用户被添加到这个组）

所以这个输出意味着 docker 组存在，但是目前没有任何用户被添加到这个组中

## add user to group

可以使用命令 `sudo usermod -aG <group-name> <username>` 将用户添加到 group 中，例如将 Plain 用户添加到 docker group 中

```bash
$ sudo usermod -aG docker Plain
$ cat /etc/group | grep docker
docker:x:993:Plain
```

`usermod` user modify 的缩写，修改用户账户属性的命令

`-a` 表示 append，即追加，如果不使用 `-a`，用户会从原来所属的其他组中被移除

`-G` 表示要修改的是用户组（Groups）

最终效果：保留用户 Plain 当前所在的所有组，将用户 Plain 添加到 docker 组

执行后，重新登录或运行 `newgrp docker`，然后再次运行 `groups` 命令，您应该就能看到 `docker` 组出现在列表中了。



> [!note]
>
> 将用户添加到 docker 组本质上是授予该用户 root 权限，因为用户可以使用 docker 命令来挂载任何目录并修改系统文件。
>
> 所以在这之后用户运行 docker 命令就无需添加 sudo

# activate group permission

## `newgrp` command

`newgrp <group-name>` 命令的作用是在当前会话中切换用户的 primary group 到指定的 group 而不需要注销并重新登录

### 工作原理

当 user 登录系统时，会获得一组初始的组成员资格

`newgrp` 命令会启动一个新的 shell，在这个新 shell 中将指定的 group 设置为 primary group，这个改变只影响新启动的 shell 会话

### 验证方式

可以通过以下方式观察 `newgrp` 的效果：

```bash
# 执行前
id
# 执行命令
newgrp docker
# 执行后
id
```

### 实际应用场景

先使用 `usermod -aG docker $USER` 将用户添加到 docker 组

然后使用 `newgrp docker` 立即激活这个组成员资格，这样就可以立即开始使用 docker 命令

> [!note]
>
> - `newgrp` 的效果只对当前终端会话有效
> - 完全注销并重新登录后，新的组成员资格会自动应用到所有新会话中
>
> 在长期使用中，建议完全注销并重新登录，但在需要立即使用新组权限的情况下，`newgrp` 是一个很好的临时解决方案。
>