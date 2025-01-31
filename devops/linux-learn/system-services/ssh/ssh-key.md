# SSH 配置和使用笔记

## SSH Agent

SSH Agent 用于存储解密后的私钥，使得用户不需要每次使用密钥时都输入密码短语。

手动添加密钥的命令：
```
ssh-add ~/.ssh/your_key_file
```

如何自动添加密钥：

1. 在shell启动文件中添加：
   ```
   ssh-add ~/.ssh/github_key 2>/dev/null
   ```
2. 在SSH配置文件中设置（如1.2中的示例）。

## SSH Agent 持久化

### macOS
- macOS默认启用SSH Agent持久化。
- 检查方法：
  ```
  launchctl list | grep ssh-agent
  ```

### Linux
- 通常不默认启用持久化。
- 检查SSH Agent是否运行：
  ```
  echo $SSH_AGENT_PID
  ```
- 持久化通常需要通过桌面环境或启动脚本配置。

### Windows
- Git for Windows通常在启动时自动运行ssh-agent。
- WSL可能需要手动配置自动启动。

## 测试SSH配置

使用如下命令测试与github的连接

```
ssh -T git@github.com
```

## 进阶主题

### 多个GitHub账户的配置
如果需要在同一台机器上使用多个GitHub账户，可以使用类似以下的配置：
```
Host github-personal
  HostName github.com
  User git
  IdentityFile ~/.ssh/personal_github_key

Host github-work
  HostName github.com
  User git
  IdentityFile ~/.ssh/work_github_key
```

### SSH Agent转发
允许在远程服务器上使用本地SSH密钥：
```
Host example-server
  HostName example.com
  ForwardAgent yes
```

注意：启用Agent转发可能带来安全风险，使用时需谨慎。

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
