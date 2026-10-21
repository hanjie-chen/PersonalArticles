# Git Remote 的 HTTPS 和 SSH：协议、代理与认证

因为在中国大陆使用 ssh 直连 github 非常慢，所以我在 `~/.ssh/config` 中给 github 走 ssh 配置了代理，结果发现也还是很慢，一次 `git push`：

```text
Writing objects: 100% (35/35), 17.79 MiB | 36.00 KiB/s, done.
```

后来做了一个实验发现，使用 ssh 的方式速度没有走 https 的方式快，但是走 ssh, https 这里两个东西是不同的认证，ssh 用的是 key,https 则是另外一个

Git 连接远程仓库时，`https://github.com/...` 和 `git@github.com:...` 不是同一条路径。它们使用不同的网络协议、不同的代理配置位置，也使用不同的认证方式。

## Mental Model

先看 remote：

```shell
git remote -v
```

常见输出有两类：

```text
origin  https://github.com/user/repo.git (fetch)
origin  https://github.com/user/repo.git (push)
```

或者：

```text
origin  git@github.com:user/repo.git (fetch)
origin  git@github.com:user/repo.git (push)
```

这一步很重要，因为 remote URL 决定 Git 使用 HTTPS 还是 SSH。

```text
https://github.com/user/repo.git
    -> HTTPS path
    -> HTTP/HTTPS proxy
    -> Git Credential Manager / token authentication

git@github.com:user/repo.git
    -> SSH path
    -> ssh client config
    -> SSH key authentication
```

## HTTPS Remote

HTTPS remote 长这样：

```text
https://github.com/user/repo.git
```

当 Git 使用 HTTPS remote 时，Git 底层通常通过 HTTP/HTTPS 连接 GitHub。代理配置一般来自两类地方。

第一类是环境变量：

```shell
HTTP_PROXY=http://127.0.0.1:7890
HTTPS_PROXY=http://127.0.0.1:7890
ALL_PROXY=socks5://127.0.0.1:7891
NO_PROXY=localhost,127.0.0.1
```

第二类是 Git 自己的配置：

```shell
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890
```

查看当前配置：

```shell
git config --show-origin --get-regexp '^http\..*proxy|^https\..*proxy'
```

取消 Git 显式代理配置：

```shell
git config --global --unset http.proxy
git config --global --unset https.proxy
```

如果没有显式配置 `http.proxy` 或 `https.proxy`，Git 的 HTTPS 请求仍然可能通过环境变量走代理。

### HTTPS Authentication

HTTPS remote 不使用 SSH key。

在 Git for Windows 里，常见认证方式是 Git Credential Manager。可以这样查看：

```shell
git config --show-origin --get-all credential.helper
git credential-manager --version
```

如果输出里有：

```text
credential.helper manager
```

说明 Git 会把 HTTPS 认证交给 Git Credential Manager。

第一次 push 或 fetch 私有仓库时，它可能打开 GitHub 登录窗口。登录完成后，Git Credential Manager 会把 GitHub 授权得到的 token 存到系统凭据管理器里。之后 Git 再访问 `https://github.com/...`，通常不需要每次重新登录。

在 Windows 上可以用下面的命令粗略查看是否有 GitHub 凭据：

```powershell
cmdkey /list | Select-String -Pattern 'git:https://github.com|github.com|GitHub'
```

这里的 token 不等于 SSH key。它是 HTTPS 认证用的凭据，由 Git Credential Manager 管理。

## SSH Remote

SSH remote 长这样：

```text
git@github.com:user/repo.git
```

当 Git 使用 SSH remote 时，Git 实际上会调用系统里的 `ssh` 客户端。这个路径不会使用 `HTTP_PROXY`、`HTTPS_PROXY`，也不会使用 `git config http.proxy` 或 `git config https.proxy`。

如果要让 SSH remote 走代理，需要配置 SSH 客户端，例如 `~/.ssh/config`：

```sshconfig
Host github.com
    User git
    ProxyCommand "C:/Program Files (x86)/Nmap/ncat.exe" --proxy 127.0.0.1:7890 --proxy-type http %h %p
```

查看 SSH 对 `github.com` 最终使用的配置：

```shell
ssh -G github.com
```

只看代理相关内容：

```shell
ssh -G github.com | Select-String -Pattern '^(hostname|user|port|proxycommand|proxyjump)'
```

如果 Git remote 还是 SSH，那么即使 shell 里有 `HTTP_PROXY` 和 `HTTPS_PROXY`，也不代表 `git push` 会使用这些 HTTP 代理环境变量。SSH 是否走代理，要看 SSH 自己的配置。

### SSH Authentication

SSH remote 使用 SSH key 认证。

常见流程是：

1. 本机生成 SSH key。
2. 把 public key 添加到 GitHub account settings。
3. Git push 时，SSH 客户端用 private key 证明自己拥有这个身份。

测试 GitHub SSH 认证：

```shell
ssh -T git@github.com
```

如果配置正确，GitHub 会返回类似：

```text
Hi user! You've successfully authenticated, but GitHub does not provide shell access.
```

这说明认证成功，但不代表这条 SSH 网络路径一定快。

## What We Measured

下载方向的测试结果：

```text
HTTPS + proxy: 476.88 KiB | 7.34 MiB/s
SSH + proxy:   476.89 KiB | 548 KiB/s
SSH direct:    476.88 KiB | 507 KiB/s
```

上传方向的测试结果：

```text
dry-run push:
HTTPS + proxy: 1.46s
SSH + proxy:   4.97s

real push, 2 MiB:
HTTPS + proxy: 3.62s
SSH + proxy:   65.58s

real push, 512 KiB:
HTTPS + proxy: 7.40s
SSH + proxy:   20.41s
```

有一个细节需要注意：`git push` 输出里的 `Writing objects` 速率不一定等于整个 push 的真实耗时。SSH 测试里，Git 显示对象写入速率并不总是很低，但整个命令耗时很长，说明慢可能发生在写包前后、协议协商、远端响应或网络链路的其他阶段。

最后把 remote 切成 HTTPS：

```shell
git remote set-url origin https://github.com/hanjie-chen/knowledge-base.git
```

验证：

```shell
git remote -v
git fetch --dry-run origin
```

## Switch Between HTTPS and SSH

切换到 HTTPS：

```shell
git remote set-url origin https://github.com/user/repo.git
```

切换回 SSH：

```shell
git remote set-url origin git@github.com:user/repo.git
```

切换之后检查：

```shell
git remote -v
git fetch --dry-run origin
```

如果已经切到 HTTPS，那么 `~/.ssh/config` 里的 `Host github.com` 不再影响这个仓库。但它仍然会影响电脑上其他使用 `git@github.com:...` 的仓库。
