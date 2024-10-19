# SSH 配置和使用笔记

## SSH 配置文件

SSH 配置文件通常位于用户主目录的 `.ssh` 文件夹中，文件名为 `config`。for example

```
Host github.com
  IdentityFile ~/.ssh/github_key

Host *
  AddKeysToAgent yes
```

- `Host github.com`: 指定针对特定主机（这里是github.com）的设置。
- `IdentityFile`: 指定连接到该主机时使用的SSH密钥文件。
- `Host *`: 应用于所有主机的通用设置。
- `AddKeysToAgent yes`: 当密钥首次被使用时，自动将其添加到SSH agent。

### SSH配置文件的其他选项

- `Hostname`: 指定要连接的实际主机名或IP地址。
- `User`: 指定登录用户名。
- `Port`: 指定SSH连接端口。

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

###### 
