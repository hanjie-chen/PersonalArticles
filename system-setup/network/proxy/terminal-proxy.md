假设已经有一个本地代理在运行：

- SOCKS5 代理：`127.0.0.1:1080`
- HTTP 代理：`127.0.0.1:8080`

要在终端设置代理（针对命令行程序，比如 `curl`、`git` 等），你可以设置环境变量。以下是设置方法：

------

### 一次性设置（仅当前终端会话有效）

#### 如果你想用 HTTP 代理：

```bash
export http_proxy=http://127.0.0.1:8080
export https_proxy=http://127.0.0.1:8080
```

#### 如果你想用 SOCKS5 代理：

```bash
export ALL_PROXY=socks5://127.0.0.1:1080
```

> 注意：SOCKS5 代理用的是 `ALL_PROXY`，有些工具（如 `curl`）才会识别。

------

### 永久设置（对所有终端窗口生效）

可以把上面的命令添加到你的 Shell 配置文件里：

- 如果你用的是 **zsh**（macOS 默认）：

  ```bash
  nano ~/.zshrc
  ```

- 如果你用的是 **bash**：

  ```bash
  nano ~/.bash_profile
  ```

然后把对应的代理设置粘贴进去，比如：

```bash
export http_proxy=http://127.0.0.1:8080
export https_proxy=http://127.0.0.1:8080
export ALL_PROXY=socks5://127.0.0.1:1080
```

保存后，执行：

```bash
source ~/.zshrc   # 或者 ~/.bash_profile
```

------

### 验证代理是否生效（以 curl 为例）

```bash
curl ip.sb
```

如果代理设置成功，它返回的 IP 应该是你的代理出口 IP，而不是你自己的公网 IP。

# 原理

很多其他的命令行程序，比如 `curl`, `wget`, `apt`, `yum`, `pip`, `npm` 等等，确实会读取并使用你设置的 `http_proxy`, `https_proxy`, `ALL_PROXY` 这些环境变量。这背后的原理其实很简单，但关键在于**程序自身的设计**。

核心原理：应用程序的主动检查和使用

这些环境变量并不是由操作系统或 Shell 自动拦截所有网络连接并强制通过代理。相反，是**应用程序本身**（或者它们使用的网络库）被编写成主动去检查这些环境变量是否存在。

具体流程通常是这样的：

1.  **启动程序：** 当你运行一个命令，比如 `curl http://example.com` 时，`curl` 程序开始执行。
2.  **检查环境变量：** 在 `curl` 内部的代码（或者它依赖的底层网络库，如 libcurl）中，有一段逻辑会检查特定的环境变量：
    *   如果要发起 HTTP 请求，它会检查 `http_proxy` 环境变量。
    *   如果要发起 HTTPS 请求，它会检查 `https_proxy` 环境变量。
    *   有些程序还会检查 `ALL_PROXY`（通常用于 SOCKS 代理，或者作为前两者的备选）。
    *   还有 `no_proxy` 或 `NO_PROXY` 环境变量，用于指定哪些主机或域名*不*应该通过代理访问。
3.  **发现代理设置：** 如果程序发现了相应的环境变量（比如 `http_proxy` 被设置为 `http://127.0.0.1:8080`），它就会解析这个值，获取代理服务器的地址 (`127.0.0.1`) 和端口 (`8080`)。
4.  **通过代理连接：**
    *   **对于 HTTP 代理:** 程序不会直接连接 `example.com`，而是连接到代理服务器 `127.0.0.1:8080`。然后，它会向代理服务器发送一个特殊的 HTTP 请求，这个请求包含了原始的目标 URL (`http://example.com`)。代理服务器收到请求后，再代表客户端去访问 `example.com`，并将结果返回给客户端。
    *   **对于 HTTPS 代理:** 通常使用 HTTP `CONNECT` 方法。程序先连接到代理服务器 `127.0.0.1:8080`，然后发送一个 `CONNECT example.com:443` 请求。如果代理允许，它会建立一个到 `example.com:443` 的 TCP 隧道。之后，程序（如 `curl`）就可以通过这个隧道与 `example.com` 进行端到端的 TLS/SSL 加密通信，代理只负责转发加密的数据包，无法看到内容。
    *   **对于 SOCKS 代理 (ALL\_PROXY):** 程序连接到 SOCKS 代理服务器 (`127.0.0.1:1080`)，并遵循 SOCKS 协议（通常是 SOCKS5）的规范，请求代理建立到目标主机和端口的连接。SOCKS 代理比 HTTP 代理更底层，可以代理几乎任何 TCP 连接（甚至 UDP，取决于 SOCKS 版本和实现）。
5.  **未发现代理设置：** 如果程序没有找到相应的环境变量，或者目标地址在 `no_proxy` 列表中，它就会直接连接目标服务器（`example.com`）。

**为什么这种方式可行？**

*   **约定俗成：** `http_proxy`, `https_proxy`, `ftp_proxy`, `ALL_PROXY`, `no_proxy` 已经成为类 Unix 系统（包括 Linux 和 macOS）上配置代理的一种广泛接受的**事实标准**（convention）。开发者在编写需要网络访问的程序时，通常会遵循这个约定，加入检查这些变量的代码。
*   **网络库的支持：** 许多流行的网络编程库（如 `libcurl` C 库, Python 的 `requests` 和 `urllib`, Node.js 的 `http`/`https` 模块, Go 的 `net/http` 包等）都内置了对这些环境变量的自动支持。开发者使用这些库时，通常不需要额外编写代码就能让他们的程序支持代理。

**总结：**

其他终端程序能使用你设置的环境变量代理，不是因为 Shell 或操作系统有什么魔法，而是因为这些**程序本身被设计成了会去查找并使用这些特定的环境变量**。它们主动地改变了自己的网络连接行为，选择通过环境变量指定的代理服务器去访问网络资源。

而 `ssh` 之所以不遵循这个约定，是因为它有自己独立的、更安全的配置体系（`~/.ssh/config`），并且其协议和用途（建立安全的端到端加密隧道）与普通的 HTTP/HTTPS 请求有所不同。