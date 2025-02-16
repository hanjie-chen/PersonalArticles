# SSH 配置文件

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

在vscode 的 remote-ssh 插件中使用 `Remote-SSH: Open SSH Configuration File...` 同样编辑的就是这个文件



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
