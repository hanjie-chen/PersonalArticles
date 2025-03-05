# SSH Agent

SSH Agent 用于存储解密后的私钥（在内存中缓存已解密的私钥），使得只需要只输入一次 passparsh，就可以在会话期间重复使用



如何判断是否需要 SSH Agent？

如果私钥没有密码保护，不需要 SSH Agent，SSH 可以直接读取私钥文件

如果您的私钥有密码保护，没有 SSH Agent 每次使用 SSH 连接时都需要输入密码，有 SSH Agent 只需在添加密钥到 Agent 时输入一次密码



# windows ssh-agent setting

查看 ssh agent 服务

```powershell
Get-Service ssh-agent
```

启动服务

```powershell
Start-Service ssh-agent
```

如果需要，设置为自动启动

```powershell
Set-Service -Name ssh-agent -StartupType Automatic
```

添加 ssh key 到 ssh agnet

```powershell
ssh-add C:\Users\<username>\.ssh\github-ssh-key
```

查看已经添加的 ssh key

```powershell
ssh-add -l
```



# linux ssh-agent setting

首先查看 ssh-agnet 是否已经启动

```shell
echo $SSH_AGENT_PID
```

如果 `ssh-agent` 运行中，会显示其进程 ID (PID)；如果没有运行，则输出为空。

如果显示为空，那么使用下面的命令启动 ssh-agent

```bash
eval "$(ssh-agent -s)"
```

添加你的 SSH 私钥：

```bash
ssh-add ~/.ssh/<ssh-key-filename> 
```



## 持久化

为了实现持久化，你可以将这些命令添加到你的 shell 配置文件中。根据你使用的 shell，可以是：

对于 Bash（~/.bashrc 或 ~/.bash_profile）：
```bash
if [ -z "$SSH_AUTH_SOCK" ] ; then
    eval "$(ssh-agent -s)"
    ssh-add ~/.ssh/<ssh-key-name>
fi
```

保存文件后，重新加载配置：

```bash
source ~/.bashrc  # 如果使用 bash
```

这样设置后，每次打开新的终端会话时，ssh-agent 都会自动启动，并且会添加你的 SSH 密钥。
