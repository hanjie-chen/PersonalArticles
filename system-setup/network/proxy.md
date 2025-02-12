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
  
  只会列出

   

  TCP

   

  监听端口（

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

如果你想使用 **HTTP 代理** 方式，即将所有 TCP 流量通过 HTTP Proxy 转发，可以在 **手动代理设置** 里进行：

1. 在 **“使用代理服务器 (Use a proxy server)”** 处点击**“开 (On)”**
2. **服务器 (Address)** 填写： `127.0.0.1`
3. **端口 (Port)** 填写： `8080`
4. 点击 **“保存 (Save)”** 确认。

> **提示**：这样做之后，系统会将大部分 TCP HTTP/HTTPS 请求自动指向此代理端口。但对于某些不兼容 HTTP 代理协议的程序，可能会无法正确识别。





下面帮你分析为什么 **浏览器** 在开启系统代理后能正常访问 Google，而在 **Windows 终端** 下使用 `curl` 却无法通过代理访问：



## Windows “系统代理” 并不一定对所有程序生效

- 当你在 Windows 设置里指定 “系统代理: 127.0.0.1:8080” 后，大部分 **WinInet** 或 **WinHTTP** API 调用的程序（例如 IE、Edge、Chrome、提示遵循系统代理的应用）会自动走该代理。
- **然而**，像 `curl` 这样的命令行工具，往往**并不**默认读取 Windows GUI 层的系统代理设置；它更常使用环境变量 `HTTP_PROXY` / `HTTPS_PROXY`，或者`--proxy` 命令行参数。
- 结果就是，浏览器能正常走代理访问 Google，但 `curl` 并没有自动套用代理设置，依旧在 **直接访问** Google （所以被 GFW 或网络屏蔽，导致超时无法连接）。

------

## 2. 解决方案

### **方法 A**：在 `curl` 命令行中添加 `--proxy`

让 `curl` 强制走代理，可以加上：

javascript



```javascript
curl --proxy http://127.0.0.1:8080 https://www.google.com
```

> 如果你启用的 **SOCKS5** 代理，则使用：
>
> javascript
>
> 
>
> ```javascript
> curl --socks5 127.0.0.1:1080 https://www.google.com
> ```

### **方法 B**：设置环境变量 `http_proxy`、`https_proxy`

- 在 Windows

   

  ```
  cmd
  ```

   

  中可执行：

  javascript

  

  ```javascript
  set http_proxy=http://127.0.0.1:8080
  set https_proxy=http://127.0.0.1:8080
  ```

  然后

   

  ```
  curl https://www.google.com
  ```

   

  就会自动依赖这些变量去走代理。

- 在 PowerShell 中：

  ```powershell
  $env:http_proxy = "http://127.0.0.1:8080"
  $env:https_proxy = "http://127.0.0.1:8080"
  curl https://www.google.com
  ```
  
  > 注意：环境变量只在当前会话生效，如果你关掉终端还要重复设置。也可以在“系统环境变量”中永久添加。

### **方法 C**：使用 Proxifier 或类似工具

- **Proxifier**, **Proxycap** 等第三方代理管理软件，可以把所有 TCP/UDP 流量（或指定进程的流量）自动转发到代理，而无需每个程序都支持系统代理或环境变量。
- 如果你想让几乎所有命令行工具、GUI 程序都强制走 Hysteria，可以考虑这类工具。



### **结论**

1. **浏览器能访问**，是因为它自动遵循了你在 Windows 系统代理中设置的 `127.0.0.1:8080`。
2. **`curl` 无法访问**，是因为它并**没有**自动使用系统代理，需要手动指定。
3. **解决办法**：在 `curl` 中显式加 `--proxy http://127.0.0.1:8080`，或设置 `http_proxy/https_proxy` 环境变量。

这样，你就在终端里也能通过 Hysteria 代理成功访问外网（包括 Google）。如果还有疑问，欢迎再来交流！



# 某些软件 proxy 设置

steam 可以设置代理，但是需要进入大屏幕状态，才能在设置中看到网络设置