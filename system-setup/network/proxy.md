*reference*: [安装 - Hysteria 2](https://v2.hysteria.network/zh/docs/getting-started/Installation/)

[搭建自己的代理服务器 | 桶装幺蛾子](https://hi.bug-barrel.top/posts/4f6adc86c6/)



考虑 client 使用nekoray,因为这篇文章推荐 [「不道德」的 Hysteria2 协议 | 桶装幺蛾子](https://hi.bug-barrel.top/posts/a4d39aa41c/) 如果仅仅使用 windows proxy的话无法实现 TUN 模式

还需要看看 Hysteria 2 的文档 [完整服务端配置 - Hysteria 2](https://v2.hysteria.network/zh/docs/advanced/Full-Server-Config/#_6)

nekoray github [MatsuriDayo/nekoray: Qt based cross-platform GUI proxy configuration manager (backend: sing-box)](https://github.com/MatsuriDayo/nekoray)

# Client 配置



# config.yml 中的 acme

ACME（Automatic Certificate Management Environment）是一种由 Let's Encrypt 推出的自动化证书管理协议，用于简化 HTTPS 证书（TLS/SSL）的申请、颁发、续期和吊销的过程。通过 ACME 协议，服务器端软件（例如 Nginx、Caddy、HAProxy 或一些代理程序）可以自动向证书颁发机构（CA，如 Let’s Encrypt）申请并获取域名的 TLS/SSL 证书。通俗理解：

- 如果你使用了 ACME 自动获取证书功能，系统会根据配置中的域名信息，自动和证书颁发机构（CA）通信，然后在后台完成验证、申请并下载对应的证书，无需人工到 CA 网站去手动生成和粘贴证书。
- 之后，程序还会定期检测证书是否临近过期，如果即将过期会自动更新证书，保持证书长期有效，省去频繁换证的麻烦。

#### **主要流程:**

1. 域名验证

   ：ACME 需要先验证域名的所有权。常见的验证方式包括：

   - **HTTP-01**：自动让服务器在指定的路由下返回特定验证文件，以供 CA 访问验证。
   - **DNS-01**：在你的 DNS 记录里添加特定的 TXT 记录，让 CA 验证你对域名的所有权。

2. **申请证书**：验证通过后，CA 会为你签发证书，并将证书返回给服务器。

3. **自动更新**：快到证书有效期时，由同样的流程去续期保证证书不过期。

可以在配置文件中使用，类似于下面的配置

```javascript
acme:
  domains:
    - your.domain.net 
  email: your@email.com
```

这表明程序会使用 ACME 协议，并根据填写的域名和邮箱自动向 CA 申请证书，并在本地生成证书文件（或内存中加载），从而实现 HTTPS 加密。



# Server 配置



下面为你解释下 `auth` 配置块里的 `password` 是做什么用的：

1. `auth` 中的 `password` 属于 Hysteria 自身的认证配置

在 Hysteria 中，`auth` 部分主要用于**客户端和服务端之间的认证**。也就是说，这个 `password` 并不是给 Let’s Encrypt 用的，而是**Hysteria 为了区分合法客户端或实现加密**而进行的“用户名-密码”方式认证（或其他认证方式）。所以在你的配置文件里：

```yaml
auth:
  type: password
  password: Se7RAuFZ8Lzg 
```

- `type: password` 表示使用 **密码认证**。
- `password: Se7RAuFZ8Lzg` 就是实际的“密钥”，当客户端连接到服务端时，需要提供相同的密码才能通过认证。





## 1. Hysteria 使用 QUIC 协议，端口是 UDP

- 日志里已经显示：

  ```javascript
  server up and running {"listen": ":443"}
  ```

  这行表示它在UDP 的 443 端口上侦听，提供基于 QUIC 的传输服务。
  
- 你所执行的命令：

  

  ```javascript
  ss -tlnp
  ```
  
  只会列出 TCP 监听端口（

  ```
  -t
  ```

   

  代表 TCP）。因此你在列表里找不到 443 端口很正常。

------

## 2. 如何查看 UDP 端口监听

改用：

```javascript
sudo ss -ulnp | grep hysteria
```

或直接把参数合并，看所有 TCP+UDP 端口：

```javascript
sudo ss -tulnp
```

就能看到 **UDP** 443 (以及其它 udp 端口) 的监听状态。



### 1. 确保 Hysteria 客户端在本地已经运行

先确认你的 **Hysteria 客户端**已成功启动，并且日志里显示它正监听以下端口（默认示例）：

```javascript
HTTP proxy server listening {"addr": "127.0.0.1:8080"}
SOCKS5 server listening {"addr": "127.0.0.1:1080"}
```

这意味着：

- **HTTP 代理地址**：`127.0.0.1` 端口 `8080`
- **SOCKS5 代理地址**：`127.0.0.1` 端口 `1080`

------

### 2. 打开 Windows 代理设置

1. Win10/Win11 

   常规步骤：

   - 点击 Windows 开始菜单 → **“设置 (Settings)”**
   - 进入 **“网络和 Internet (Network & Internet)”**
   - 在左侧或上方找到 **“代理 (Proxy)”** 选项并点击进入
   
2. 在“代理”设置页面，通常会见到两部分：

   - **自动代理设置** (Automatic proxy setup)
   - **手动代理设置** (Manual proxy setup)

------

### 3. 手动设置代理 (HTTP)

如果你想使用 HTTP 代理 方式，即将所有 TCP 流量通过 HTTP Proxy 转发，可以在 手动代理设置 里进行：

1. 在 “使用代理服务器 (Use a proxy server)” 处点击“开 (On)”
2. 服务器 (Address) 填写： `127.0.0.1`
3. 端口 (Port) 填写： `8080`
4. 点击 “保存 (Save)” 确认。

## Windows “系统代理” 并不一定对所有程序生效

- 当你在 Windows 设置里指定 “系统代理: 127.0.0.1:8080” 后，大部分 **WinInet** 或 **WinHTTP** API 调用的程序（例如 IE、Edge、Chrome、提示遵循系统代理的应用）会自动走该代理。
- **然而**，像 `curl` 这样的命令行工具，往往**并不**默认读取 Windows GUI 层的系统代理设置；它更常使用环境变量 `HTTP_PROXY` / `HTTPS_PROXY`，或者`--proxy` 命令行参数。
- 结果就是，浏览器能正常走代理访问 Google，但 `curl` 并没有自动套用代理设置，依旧在 **直接访问** Google （所以被 GFW 或网络屏蔽，导致超时无法连接）。







# 某些软件 proxy 设置

steam 可以设置代理，但是需要进入大屏幕状态，才能在设置中看到网络设置



# Ubuntu Linux 全局代理

通过在 Ubuntu 上安装并配置 **redsocks**，再利用 **iptables** 将所有出站的 TCP 流量重定向到 redsocks 监听的端口，由 redsocks 将它们转发到目标代理服务器（HTTP 或 SOCKS5）。这种方式能较好地实现“本机全部流量”走代理，但要谨慎设置白名单，避免把 SSH 等重要流量也一并重定向

下面给出一个基于当前 Hysteria2 客户端（提供 SOCKS5 代理在 127.0.0.1:1080）的示例配置，帮助你通过 redsocks + iptables 将全局的 TCP 流量重定向到 Hysteria2 的代理接口，从而实现全局代理。

## 安装 redsocks

如果尚未安装，请执行以下命令更新软件仓库并安装 redsocks：

```bash
sudo apt-get update
sudo apt-get install redsocks
```



## 配置 redsocks

编辑 `/etc/redsocks.conf` 文件（如果文件不存在，可创建一个），内容示例如下：

```cpp
base {
    log_debug = off;
    log_info = on;
    daemon = on;             # 以守护进程方式运行
    redirector = iptables;   # 使用 iptables 重定向流量
}

redsocks {
    local_ip = 127.0.0.1;      # redsocks 本地监听地址
    local_port = 12345;        # redsocks 监听的端口（可以自定义，如 12345）
    ip = 127.0.0.1;            # Hysteria2 客户端的代理地址（SOCKS5）
    port = 1080;               # Hysteria2 提供的 SOCKS5 代理端口
    type = socks5;             # 使用 socks5 协议
    // login = "your_username";   # 如代理需要认证，则开启并填写
    // password = "your_password";
}
```

保存好文件后，你可以先用调试模式启动测试，再使用守护进程模式运行：

bash



```bash
sudo redsocks -c /etc/redsocks.conf -p /var/run/redsocks.pid
```

------

#### 3. 配置 iptables 规则

下面的 iptables 规则将所有出站的 TCP 流量（除去局域网、回环地址等）重定向到 redsocks 本地监听端口（本例中为 12345）：





```bash
# 新建 redsocks 链
sudo iptables -t nat -N REDSOCKS

# 排除局部地址，防止重定向本地连接（包括 SSH、内网通信等）
sudo iptables -t nat -A REDSOCKS -d 0.0.0.0/8 -j RETURN
sudo iptables -t nat -A REDSOCKS -d 10.0.0.0/8 -j RETURN
sudo iptables -t nat -A REDSOCKS -d 127.0.0.0/8 -j RETURN
sudo iptables -t nat -A REDSOCKS -d 169.254.0.0/16 -j RETURN
sudo iptables -t nat -A REDSOCKS -d 172.16.0.0/12 -j RETURN
sudo iptables -t nat -A REDSOCKS -d 192.168.0.0/16 -j RETURN
sudo iptables -t nat -A REDSOCKS -d 224.0.0.0/4 -j RETURN
sudo iptables -t nat -A REDSOCKS -d 240.0.0.0/4 -j RETURN

# 将所有经过的 TCP 流量重定向到 redsocks 的 12345 端口
sudo iptables -t nat -A REDSOCKS -p tcp -j REDIRECT --to-ports 12345

# 对本机的 OUTPUT 链中所有 TCP 流量应用重定向规则
sudo iptables -t nat -A OUTPUT -p tcp -j REDSOCKS
```



## 结果

失败，对于普通的 tcp 流量正常，但是对于 https 流量则存在问题，TLS 握手会失败