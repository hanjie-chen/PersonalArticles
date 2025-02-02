# Key-based authentication

当我们使用ssh连接到一台远程服务器的时候，需要输出 username, passoword 来进行登录

但是这样子可能会遇到一些安全问题，比如说一台有 public ip 的 server 可能会遇到，密码爆破攻击这样子，为了安全考虑，我们可以使用 ssh key 验证



## 生成 ssh key

```bash
ssh-keygen -t rsa -b 4096 -C "note" -f ~/.ssh/<key-filename>
```

这里的 `-f` 参数指定输出文件名，这样就会生成 `~/.ssh/<key-filename>`（私钥） 和 `~/.ssh/<key-filename>.pub`（公钥）

生成过程中可以选择是否给私钥加 passphrase（密码短语）。如果加了，在登录时需要输入 passphrase

一般来说我们写的注释，通常记录在公钥文件的结尾处，可以直接打开 `.pub` 文件查看

对于文件名，我们最好起一个有意义的名字，例如 `Singapore_Linux_VM_SSH_Key` 

e.g.

```shell
➜ .ssh  ssh-keygen -t rsa -b 4096 -C "Singapore Linux VM" -f ./Singapore_Linux_VM_SSH_Key
Generating public/private rsa key pair.
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in ./Singapore_Linux_VM_SSH_Key
Your public key has been saved in ./Singapore_Linux_VM_SSH_Key.pub
The key fingerprint is:
SHA256:lcVNmuQlFiyBm6FMZfzL+0uhLVWzftlGcURFXz/t5w8 Singapore Linux VM
The key's randomart image is:
+---[RSA 4096]----+
|       oo..+*+ooB|
|      ..+ .*o=..=|
|     o . =o.+ oo=|
|      o o..  . ++|
|        S. .o . +|
|          o+ o o+|
|          o.o E.=|
|          .o   +.|
|           .o.  .|
+----[SHA256]-----+
```



## 添加ssh key

既然已经生成了 ssh key, 我们就需要将 public key 添加到 remote server中去

使用命令

```shell
ssh-copy-id -p <ssh-port> -i ~/.ssh/Singapore_Linux_VM_SSH_Key.pub <username>@<remote-server-ip>
```

如果使用默认的 22 号端口，可以省略 `-p <ssh-port>` 参数

e.g.

```shell
$ ssh-copy-id -p <ssh-port> -i ./Singapore_Linux_VM_SSH_Key.pub Plain@<remote-server-ip>
/usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "./Singapore_Linux_VM_SSH_Key.pub"
/usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
/usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
Plain@<remote-server-ip>'s password:

Number of key(s) added: 1

Now try logging into the machine, with:   "ssh -p <ssh-port> 'Plain@<remote-server-ip>'"
and check to make sure that only the key(s) you wanted were added.
```



## 使用 ssh key 登录

如果我们直接用 `ssh username@remote-server-ip`，SSH 默认会仅尝试 `id_rsa` 这样默认命名的密钥

所以我们需要在命令行临时指定：

```javascript
ssh -i ~/.ssh/id_rsa_remote_server username@remote-server-ip
```

当然为了方便起见，我们往往在 `~/.ssh/config` 中添加配置，让 SSH 自动知道该请求要用哪个 key，举例：

```javascript
Host remote-server
    HostName remote-server-ip
    User username
    IdentityFile ~/.ssh/id_rsa_remote_server
```

然后只要 `ssh remote-server` 即可自动使用该密钥。



## `ssh-copy-id` 不可用？

如果你使用 windows powershell, 大概率找不到这个命令，这个时候，我们需要手动将 public key 复制到远程服务器上面

打开并且复制本地公钥内容(`ssh-rsa AAAA... Singapore Linux VM` 包括开头的 `ssh-rsa` 到最后的注释部分）

SSH 登录到远程服务器（使用密码验证）此时会提示你输入远程主机密码。

将复制的公钥追加到服务器上的authorized_keys，在远程服务器上，执行：

```javascript
cd ~/.ssh
echo "这里粘贴你的公钥整行内容" >> authorized_keys
```

确保多行公钥之间使用回车分隔即可。

验证是否可用，在本地退出服务器 (`exit` 或 `Ctrl+D`) 后，重新使用公钥登录：

```javascript
ssh -i .\Singapore_Linux_VM_SSH_Key Plain@104.215.254.81
```

如果一切配置正确且没有私钥加密口令，那么应当无需再输入服务器密码即可登录。
