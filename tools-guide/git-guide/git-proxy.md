是的，`git` 命令在处理网络操作时，**也会** 查找并使用代理设置，但它的行为和配置方式比 `curl` 等简单工具要稍微复杂一些，因为它同时支持 HTTP/HTTPS 和 SSH 协议，并且有自己的配置系统 (`git config`)。

以下是 `git` 如何处理代理设置的详细说明：

**1. HTTP 和 HTTPS 协议 (例如 `git clone https://...`, `git push https://...`)**

*   **环境变量优先 (默认行为):**
    *   `git` 底层通常使用 `libcurl` 库来处理 HTTP/HTTPS 请求。
    *   `libcurl` **会** 自动检测并使用 `http_proxy`, `https_proxy`, 和 `all_proxy` (注意是小写) 环境变量。它还会尊重 `no_proxy` 或 `NO_PROXY`。
    *   所以，如果你在 `.zshrc` 中设置了 `http_proxy` 和 `https_proxy`，那么 `git` 通过 HTTPS 协议进行的操作（如 clone, fetch, push 到 `https://` 开头的仓库）**默认就会使用这些代理**。
    *   `all_proxy` (小写) 也可以被 `libcurl` 识别用来指定 SOCKS 代理。如果你设置了 `export all_proxy=socks5://127.0.0.1:1080` (注意小写)，`git` 的 HTTP/HTTPS 操作也可能会尝试通过这个 SOCKS 代理。

*   **Git 配置 (`git config`) 覆盖环境变量:**
    *   `git` 允许你通过 `git config` 命令更精细地配置代理，**这些配置会覆盖环境变量的设置**。
    *   **设置 HTTP 代理:**
        ```bash
        git config --global http.proxy http://127.0.0.1:8080
        ```
    *   **设置 HTTPS 代理:**
        ```bash
        git config --global https.proxy http://127.0.0.1:8080
        ```
    *   **设置 SOCKS 代理 (通常通过指定协议):**
        ```bash
        # 让 HTTP 和 HTTPS 都走 SOCKS5 代理
        git config --global http.proxy 'socks5://127.0.0.1:1080'
        git config --global https.proxy 'socks5://127.0.0.1:1080'
        ```
    *   **查看当前 Git 代理配置:**
        ```bash
        git config --global --get http.proxy
        git config --global --get https.proxy
        ```
    *   **取消 Git 代理配置 (恢复使用环境变量或不使用代理):**
        ```bash
        git config --global --unset http.proxy
        git config --global --unset https.proxy
        ```
    *   `--global` 表示对当前用户的所有仓库生效。去掉 `--global` 则只对当前仓库生效。

**2. SSH 协议 (例如 `git clone git@github.com:...`, `git push git@...`)**

*   **完全不使用** `http_proxy`, `https_proxy`, `ALL_PROXY`, 或 `git config http.proxy` / `https.proxy`。
*   当 `git` 使用 SSH 协议连接远程仓库时（URL 以 `git@...` 或 `ssh://...` 开头），它实际上是**调用系统的 `ssh` 客户端**来建立连接。
*   因此，要让 `git` 通过 SSH 协议走代理，你必须配置 `ssh` 客户端本身，也就是我们之前讨论过的，**修改 `~/.ssh/config` 文件**，使用 `ProxyCommand` 指令。

    ```config
    # ~/.ssh/config
    
    # 对所有主机 (*) 或特定主机 (e.g., Host github.com) 使用 SOCKS 代理
    Host *
        ProxyCommand nc -X 5 -x 127.0.0.1:1080 %h %p
        # 或者使用 connect-proxy
        # ProxyCommand connect-proxy -S 127.0.0.1:1080 %h %p
    ```

**总结:**

*   对于 **HTTP/HTTPS** 仓库 (`https://...`)：
    *   `git` **默认会** 使用 `http_proxy`/`https_proxy`/`all_proxy` 环境变量。
    *   你可以使用 `git config http.proxy`/`https.proxy` 来**覆盖**环境变量，并进行更精细的配置（包括直接设置 SOCKS 代理）。
*   对于 **SSH** 仓库 (`git@...` 或 `ssh://...`)：
    *   `git` **完全忽略** 代理环境变量和 `git config` 中的代理设置。
    *   你**必须**通过修改 `~/.ssh/config` 并使用 `ProxyCommand` 来配置代理。

所以，你的 `http_proxy` 和 `https_proxy` 环境变量对 `git clone https://...` 应该是有效的，但 `ALL_PROXY` 对于 `git` 的作用没有 `http(s)_proxy` 那么直接（虽然底层的 libcurl 可能识别小写的 `all_proxy`）。而对于 `git clone git@...`，这些环境变量和 `git config` 里的代理设置都无效，必须配置 `~/.ssh/config`。