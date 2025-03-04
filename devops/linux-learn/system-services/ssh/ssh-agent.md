# SSH Agent

SSH Agent 用于存储解密后的私钥（在内存中缓存已解密的私钥），使得只需要只输入一次 passparsh，就可以在会话期间重复使用



## 是否需要 SSH Agent？

**如果您的私钥没有密码保护**:

- 不需要 SSH Agent，SSH 可以直接读取私钥文件

**如果您的私钥有密码保护**（推荐的安全做法）:

- 没有 SSH Agent：每次使用 SSH 连接时都需要输入密码
- 有 SSH Agent：只需在添加密钥到 Agent 时输入一次密码



# windows ssh-agent setting

查看 SSH Agnet 服务

```powershell
# 检查服务状态
Get-Service ssh-agent

# 如果需要，设置为自动启动
Set-Service -Name ssh-agent -StartupType Automatic

# 启动服务
Start-Service ssh-agent
```

添加 ssh key 到 ssh agnet

```powershell
ssh-add C:\Users\<username>\.ssh\github-ssh-key
```





# Linux 启动ssh-agent

要启动 ssh-agent 并实现持久化，你可以按照以下步骤操作：

1. 首先启动 ssh-agent：
```bash
eval "$(ssh-agent -s)"
```

2. 添加你的 SSH 私钥：
```bash
ssh-add ~/.ssh/id_rsa  # 或者你的私钥路径
```

3. 为了实现持久化，你可以将这些命令添加到你的 shell 配置文件中。根据你使用的 shell，可以是：

对于 Bash（~/.bashrc 或 ~/.bash_profile）：
```bash
if [ -z "$SSH_AUTH_SOCK" ] ; then
    eval "$(ssh-agent -s)"
    ssh-add ~/.ssh/id_rsa
fi
```

对于 Zsh（~/.zshrc）：
```bash
if [ -z "$SSH_AUTH_SOCK" ] ; then
    eval "$(ssh-agent -s)"
    ssh-add ~/.ssh/id_rsa
fi
```

4. 保存文件后，重新加载配置：
```bash
source ~/.bashrc  # 如果使用 bash
# 或
source ~/.zshrc   # 如果使用 zsh
```

这样设置后，每次打开新的终端会话时，ssh-agent 都会自动启动，并且会添加你的 SSH 密钥。

注意：
- 确保你的 SSH 私钥文件权限正确（通常应该是 600）
- 如果你的私钥文件不是默认的 `id_rsa`，需要相应修改路径
- 如果你不想每次都自动添加密钥，可以去掉 `ssh-add` 那一行，需要时手动添加

如果遇到权限问题，可以检查并设置正确的权限：
```bash
chmod 600 ~/.ssh/id_rsa
```
