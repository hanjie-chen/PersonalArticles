# server-guide

服务器如何按照我的喜好运行 SSH 服务？

在 server 端的许多 ssh 配置，只需要修改 `/etc/ssh/sshd_config` 文件即可

# ssh port

ssh 默认使用22号端口进行连接，有时候为了安全考虑，我们需要将其修改为其他的端口，为此我们需要修改 ssh 配置文件

以 root 权限打开 SSH 配置文件:

```javascript
sudo vim /etc/ssh/sshd_config
```

在文件中找到包含 `#Port 22` 的行,去掉前面的 `#` 号,将 `22` 修改为目的端口:

```javascript
Port <port-number>
```

重启 SSH 服务以使更改生效:

```javascript
sudo systemctl restart ssh
```

> [!note]
>
> 如果你使用了防火墙,需要允许新的端口通过防火墙。例如,如果你使用 UFW (Uncomplicated Firewall):
>
> ```javascript
> sudo ufw allow <port-number>/tcp
> ```

现在理论上你可以使用新的端口连接 SSH 了:

```javascript
ssh user@server_ip -p <port-number>
```

如果发现 ssh 依然使用旧的22号端口监听，那么我们继续排查

## 验证配置是否生效

首先我们查看 sshd 的实际配置 --> `sudo sshd -T | grep -i port`

```bash
Plain@Singapore-Linux-VM:~$ sudo sshd -T | grep -i port
port 10499
gatewayports no
```

它会输出当前 sshd 实际使用的端口。我们可以看到它能正确输出 `port 10499`，说明配置文件已被读到。

接着我们查看系统实际监听的端口 --> `sudo ss -tlpn | grep sshd`

```bash
Plain@Singapore-Linux-VM:~$ sudo ss -tlpn | grep sshd
LISTEN 0      4096               *:22              *:*    users:(("sshd",pid=2573,fd=3),("systemd",pid=1,fd=90))
```

它会输出 sshd 实际监听了哪些端口。

我们看到仍是 22，而不是 10499，就说明有其他机制在“截胡”端口使用。

让我们仔细看看这个命令的输出

```
LISTEN
  └── 状态字段：表示该套接字正处于“监听”状态，等待传入的连接

0
  └── 接收队列（Recv-Q）当前没有待处理的传入连接

4096
  └── 发送队列（Send-Q）这个数值通常用来指示连接队列的最大长度

*:22
  └── 本地地址和端口
         ├── * ：表示绑定到所有本地网络接口
         └── 22：表示监听的端口号（SSH 服务的默认端口）

*:* 
  └── 远程地址和端口
         └── 由于是监听状态，远程信息用通配符（*:*）表示接受任意来源的连接

users:(("sshd",pid=2573,fd=3),("systemd",pid=1,fd=90))
  └── 持有该监听套接字的进程信息：
         ├── ("sshd", pid=2573, fd=3)
         │      └── sshd：SSH 守护进程
         └── ("systemd", pid=1, fd=90)
                └── systemd：系统守护进程（PID 1），利用 socket activation 机制预先监听该端口
```

> [!important]
>
> socket activation（套接字激活） 是 systemd 提供的一种机制：
>
> 1. systemd 会先行监听一个或多个特定端口（或 UNIX Socket 等“套接字”）。
> 2. 当有连接请求到达这些端口时，systemd 才会启动或唤醒与之对应的服务。
>
> 这样做的好处是，只有在真正需要的时候，才会启动相应的服务进程，可以提升一定的系统效率；并且在一些依赖顺序复杂的场景下更灵活。

## systemd 排查

通过之前命令发现，系统守护进程在监听这个 22 号端口，让我们进一步确认是否是因为 socket activation 机制劫持了10499端口

是否启用了 ssh.socket --> `sudo systemctl status ssh.socket`

```bash
Plain@Singapore-Linux-VM:~$ sudo systemctl status ssh.socket
● ssh.socket - OpenBSD Secure Shell server socket
     Loaded: loaded (/usr/lib/systemd/system/ssh.socket; enabled; preset: enabled)
     Active: active (running) since Fri 2025-01-31 15:53:09 UTC; 14h ago
   Triggers: ● ssh.service
     Listen: [::]:22 (Stream)
      Tasks: 0 (limit: 9519)
     Memory: 8.0K (peak: 256.0K)
        CPU: 626us
     CGroup: /system.slice/ssh.socket

Jan 31 15:53:09 Singapore-Linux-VM systemd[1]: Listening on ssh.socket - OpenBSD Secure Sh>
lines 1-11/11 (END)
```

我们可以看到，`ssh.socket` 已经被 systemd “抓住”了 22 端口 (Listen: [::]:22)。

- 当 systemd 在 `ssh.socket` 中配置了 “ListenStream=22” 时，就会让 systemd 在 22 端口上监听，这时即使你在 `/etc/ssh/sshd_config` 中改为 Port 10499，也没有效果，因为 systemd 仍自动在 22 端口监听并触发 sshd。
- 使用 socket-based activation 时，sshd 启动后会直接从 systemd 继承套接字，而不需要再绑定 22 端口。这样就形成一个冲突：明明 sshd_config 写了 10499，但实际被 systemd 传进来的，是已经绑定好的 22 端口。

## 禁用并停止 ssh.socket

如果我们希望使用手动在 `sshd_config` 中指定的自定义端口，那么可以禁用 socket-based activation：

```javascript
sudo systemctl stop ssh.socket
sudo systemctl disable ssh.socket
```

确保 ssh 服务启用并启动，这样我们就不需要 socket 了，直接让 sshd 自己监听：

```javascript
sudo systemctl enable ssh
sudo systemctl start ssh
```

## root cause

当开启了 systemd 的 socket-based activation 功能时，systemd 会在 22 端口上先进行绑定和监听。

这样一来，sshd 在启动时就会直接“继承”这个已经打开好的套接字，完全不需要也不会去执行“bind(Port 10499)”的操作。

因此，即使你在 `sshd_config` 中配置了 `Port 10499`，对于绑定端口的部分，它其实被 systemd“绕过”了，`sshd` 并不会去检查 `sshd_config` 里写的端口，而是被动地接受 systemd 分配的 22 端口的套接字。

在没有 socket-based activation 的常规模式下：

1. sshd 读取 `/etc/ssh/sshd_config` 中的 `Port 10499`。
2. 然后再由 sshd 自己调用 `bind()` 到 10499 端口并开始监听。
3. 这时 `sshd -T | grep -i port` 和 `netstat`（或 `ss`）显示出来的端口就会一致。

# Welcome message

当我们使用原生的 ubuntu 系统的时候，会发现欢迎信息一大堆，但是真正有用的信息不多，如下所示

```bash
Welcome to Ubuntu 20.04.6 LTS (GNU/Linux 5.15.0-1064-azure x86_64)

Documentation:  https://help.ubuntu.com
Management:     https://landscape.canonical.com
Support:        https://ubuntu.com/pro
System information as of Mon Jun  3 10:03:27 UTC 2024

System load:  0.16               Processes:             127
Usage of /:   22.6% of 28.89GB   Users logged in:       0
Memory usage: 20%                IPv4 address for eth0: 10.0.2.4
Swap usage:   0%


Strictly confined Kubernetes makes edge and IoT secure. Learn how MicroK8s
just raised the bar for easy, resilient and secure K8s cluster deployment.

Expanded Security Maintenance for Applications is not enabled.

0 updates can be applied immediately.

2 additional security updates can be applied with ESM Apps.
Learn more about enabling ESM Apps service at https://ubuntu.com/esm

Last login: Fri May 31 07:41:57 2024 from 10.0.1.4
```

如果我们想要定制这个欢迎界面信息，应该怎么办呢？