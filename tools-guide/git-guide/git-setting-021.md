# background

从 0 开始的 git 设置指南，其实也不是非常的 0 基础，至少需要一个 github 账号，懂一些 ssh，其中 ssh 的部分可以看我之前写的关于 ssh 的文章

当你拿到一台空白的 windows machine 的时候，应该如何设置 git 呢？



# download git

为了方便，我们直接打开 cmd 使用 winget 下来 git

```cmd
winget install --id Git.Git
```

这会自动帮你下载最新版本的 git

> [!note]
>
> 如果使用 cmd 安装完成之后，使用 `git --version` 命令显示没有找到，那么新开一个 cmd 或者 powershell 一般就能看到



# ssh key generate

为了使用 ssh-key 连接上 github , 我们的 windows machine 至少需要 1 个 ssh-key

```powershell
cd ~/.ssh
ssh-keygen -t rsa -b 4096 -C "note" -f <key-filename>
```

> [!note]
>
> 这里使用 cd 命令提前进入 `~/.ssh` 目录，因为有些 powershell 在使用 ssh-keygen 命令的时候不会识别 `~`

然后将 `<key-filename>.pub` 文件中的内容复制到 github 账号 settings 中的 `SSH and GPG keys` 中，记得起一个可以用于辨识这台 windows machine 的名字

# ssh config

这是你虽然生成了 ssh key, 并且在 github 上面配置了你的公钥，但是这个时候，如果你使用下面的命令去测试，大概率依然会失败

```bash
ssh -T github.com
```

因为实际上 ssh 不知道他要去找那个 key

当运行 `ssh -T git@github.com` 而不指定密钥时，SSH 客户端会按照以下顺序查找并尝试使用密钥：

1. SSH Agent 中已加载的密钥
2. 默认位置的密钥文件（通常是 `~/.ssh/id_rsa`、`~/.ssh/id_dsa`、`~/.ssh/id_ecdsa`、`~/.ssh/id_ed25519`）

这个时候如果指定 ssh key

```bash
ssh -i C:\Users\<username>\.ssh\github-ssh-key -T git@github.com
```

反而会成功，因为 ssh 这时才知道使用什么 key 去和 github 进行验证

我们可以在 `~/.ssh` 目录下创建 config 文件，告诉 ssh 选择哪个 key

```
Host github.com
  HostName github.com
  User git
  IdentityFile C:/Users/<username>/.ssh/github-ssh-key
  IdentitiesOnly yes
```



# ssh agent

如果配置我们对 ssh key 配置了 passphrase 那么，最好将其加入到 ssh agent 中，这样子我们只需要输入一遍 passphrase即可，后面ssh agent 会帮我们加载密钥

```powershell
# 检查服务状态
Get-Service ssh-agent

# 如果需要，设置为自动启动
Set-Service -Name ssh-agent -StartupType Automatic

# 启动服务
Start-Service ssh-agent
```

添加 ssh key 到 ssh agent

```powershell
ssh-add C:\Users\<username>\.ssh\<ssh-key-name>
```

查看已经添加的 ssh key

```powershell
ssh-add -l
```

是否需要在 git bash 中添加 ssh-agent 呢？我尝试了似乎在 git bash 中 add ssh agent 然后在 git bash 中 git push没问题

# download github repository

这是，我们就可以使用 git clone 下载 github repository 了

```bash
git clone git@github.com:hanjie-chen/PersonalArticles.git
```

这样，就可以正常的使用 git 命令了

> [!note]
>
> 只有在 `ssh -T git@githu.com` 命令验证成功之后才能 `git clone git@github.com:....` 类型的仓库，因为实际上他也是进行 ssh 验证的。
>
> 但是如果是 `git clone https://github.com/...` 则无需 ssh 验证，但是当你 git push 的时候，会弹出一个方框让你进行 github 账号登录和验证

如果之前不小心 git clone https 的，可以使用 `git remote set-url origin` 命令重置为 ssh url