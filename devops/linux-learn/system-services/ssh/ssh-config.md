# SSH client 配置文件

ssh 配置文件一般默认路径是 `~/.ssh/config` 这个文件本质上是一个SSH 客户端的全局配置文件，支持许多的功能

不过我们先来看看他最基础，也是用的最多的功能：简化连接命令，将复杂的将复杂的 ssh 命令参数转化为一个 host



在配置文件中添加主机配置后，可直接通过 `ssh <hostname>` 快速登录，无需每次都输入 `ssh user@host -p port`

一个经典的主机配置例如

```
# Read more about SSH config files: https://linux.die.net/man/5/ssh_config
Host Azure-Linux-VM
    HostName <public-ip/private-ip>
    User <username>
    Port <ssh-port>
    IdentityFile ~/.ssh/id_rsa
```

我们需要运行 `ssh Azure-Linux-VM` 即可

在 vscode 的 remote-ssh 插件中使用 `Remote-SSH: Open SSH Configuration File...` 同样编辑的就是这个文件



## 为不同主机指定私钥

例如为个人服务器和公司服务器使用不同密钥。GitHub 或 GitLab 配置不同密钥。

```
Host github.com
  User git
  IdentityFile ~/.ssh/github_key  # GitHub 专用密钥

Host company-server
  HostName example.com
  User dev
  IdentityFile ~/.ssh/work_key    # 公司服务器密钥
```



> [!important]
>
> 注意 ssh config 不支持直接配置密码



# lost connection

有时候我们会遇到一个问题：`client_loop: send disconnect: Connection reset`

通常不是 SSH config 本身的问题，而是 网络连接不稳定 或 远程主机主动断开连接 所导致的。我们可以从几个方面来排查：



### 🔍 排查方向

#### 1. **检查本地 SSH 设置**

在本地 SSH config 文件中（通常在 `~/.ssh/config`），你可以尝试添加以下配置：

```ssh
Host SG-Linux-VM
    HostName <your.vm.ip.or.dns>
    User Plain
    IdentityFile ~/.ssh/Singapore_Linux_VM_SSH_Key
    ServerAliveInterval 30
    ServerAliveCountMax 5
```

解释：

- `ServerAliveInterval 30`：每 30 秒向服务器发送一个 "keep-alive" 数据包。
- `ServerAliveCountMax 5`：如果连续 5 次都没有回应，SSH 客户端才断开连接。

这个设置可以 避免空闲时被 Azure 或其他中间网关断开连接。



#### 2. **检查服务器端 SSH 设置**

在 VM 的 `/etc/ssh/sshd_config` 中，确保包含以下配置（需要 `sudo` 权限修改）：

```conf
ClientAliveInterval 30
ClientAliveCountMax 5
```

执行后别忘了重启 SSH 服务：

```bash
sudo systemctl restart ssh
```



# git config

当我们使用 ssh-keygen 生成一个用于和  github 验证的 ssh key 的时候（并且已经把 public key 上传到 github ssh key zhogn），如果我们的起的名字是 customerized 的，那么当我们使用命令 

```bash
ssh -T git@github.com
```

就会发现失败

```
PS C:\Users\Plain\articles> ssh -T git@github.com
git@github.com: Permission denied (publickey).
```

