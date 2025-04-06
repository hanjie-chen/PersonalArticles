link: https://chatgpt.com/c/67ef8c93-fba8-800a-b11c-d8870ea700d1

是的，DoH (DNS over HTTPS) 指的是 **DNS 解析通过 HTTPS 进行加密传输**，以提高安全性和隐私保护。它使得 DNS 查询不再是明文可见，而是通过加密的 HTTPS 连接进行解析，从而防止 DNS 劫持和中间人攻击。

------

### 🔹 **DoH (DNS over HTTPS) 详解**

1. **传统 DNS 存在的问题**

   - 传统的 DNS 查询是明文的，攻击者可以拦截和篡改 DNS 解析结果（如 DNS 劫持）。
   - 运营商或其他第三方可以监视用户的 DNS 查询，影响隐私。

2. **DoH 如何工作？**

   - **加密**：使用 HTTPS (通常是 TLS 1.2 / 1.3) 传输 DNS 查询和响应，防止被拦截或篡改。
   - **标准化协议**：IETF（互联网工程任务组）发布了 **RFC 8484** 规范，定义了 DoH 的实现方式。
   - **查询格式**：客户端将 DNS 查询封装成 HTTP/2 或 HTTP/3 请求，发送给支持 DoH 的 DNS 服务器（如 Cloudflare 1.1.1.1、Google 8.8.8.8）。
   - **返回结果**：DoH 服务器解析查询，并通过 HTTPS 返回 IP 地址。

3. **DoH 与 DoT (DNS over TLS) 的对比**

   | 特性       | DoH (DNS over HTTPS)          | DoT (DNS over TLS)          |
   | ---------- | ----------------------------- | --------------------------- |
   | 端口       | 443 (HTTPS)                   | 853 (TLS)                   |
   | 传输层协议 | HTTP/2, HTTP/3                | 纯 TLS 连接                 |
   | 安全性     | ✅ TLS 加密 + HTTP             | ✅ TLS 加密                  |
   | 兼容性     | 🔥 更容易在现有 Web 服务中集成 | ⚠ 需要专门的 DNS 客户端支持 |
   | 隐私保护   | ⭐⭐⭐⭐（更隐蔽，难以被封锁）    | ⭐⭐⭐（独立端口可能被封锁）   |

4. **主流支持 DoH 的公共 DNS**

   | DNS 提供商 | DoH 服务器地址                    |
   | ---------- | --------------------------------- |
   | Cloudflare | `https://1.1.1.1/dns-query`       |
   | Google     | `https://dns.google/dns-query`    |
   | Quad9      | `https://dns.quad9.net/dns-query` |

5. **优点** ✅ 防止 DNS 劫持和中间人攻击
    ✅ 保护隐私，防止 ISP 监视 DNS 查询
    ✅ 在普通 HTTPS 流量中伪装，难以被干扰或封锁

6. **缺点** ⚠️ 可能影响本地网络的 DNS 解析策略（如企业网络可能无法使用内部 DNS）
    ⚠️ 配置复杂度略高（相比传统 DNS）

7. **如何在 Linux/Windows 上启用 DoH？**

   - **浏览器（如 Chrome/Firefox）**：可以在“网络设置”中启用 DoH
   - **系统级（如 Windows 11 / Linux）**：可以配置 `systemd-resolved` 或使用 **Cloudflare / Google 的 DoH 客户端**
   - **Nginx 代理**：可以配置 Nginx 作为 DoH 服务器，提供本地 DNS 加密解析

------

### 🚀 **结论**

DoH 是目前提升 DNS 安全和隐私的重要技术，适用于个人和企业使用，特别是在网络审查或隐私保护需求高的环境下。你打算在你的 **Flask + Nginx** 服务器上使用 DoH，还是只是对这项技术感兴趣？ 😃



Windows 10 **系统级别**可以配置 DoH，但不像 Windows 11 那样内置 GUI 选项，需要手动修改 **注册表** 来启用 DoH 解析。

------

### ✅ **Windows 10 系统级别启用 DoH 方法**

Windows 10 **2004 (20H1) 及以上版本**支持 DoH，但默认未启用。可以通过 **注册表修改** 来开启。

#### **📌 1. 修改注册表启用 DoH**

1. **打开注册表编辑器**

   - 按 `Win + R` 输入 `regedit`，回车。

2. **定位到以下路径**：

   ```plaintext
   HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Dnscache\Parameters
   ```

3. **新建 DWORD 值**

   - 右键 **空白区域** → **新建** → **DWORD（32 位）值**，命名为：

     ```plaintext
     EnableAutoDoh
     ```

   - 设置值为：

     ```plaintext
     2  （表示强制使用 DoH）
     ```

   - 可能的值：

     - `0` = 关闭 DoH
     - `1` = 自动检测 DoH
     - `2` = 强制使用 DoH

4. **重启 DNS 服务**

   - 在命令提示符 (cmd) 或 PowerShell 运行：

     ```powershell
     net stop dnscache && net start dnscache
     ```

------

#### **📌 2. 设置支持 DoH 的 DNS 服务器**

修改 **Windows 网络设置**，指定支持 DoH 的 DNS：

1. **打开“网络和 Internet 设置”**
2. 选择 **更改适配器选项**
3. 右键 **你的网络适配器** → **属性**
4. 选择 **Internet 协议版本 4 (TCP/IPv4)** → **属性**
5. 选择 **使用下面的 DNS 服务器地址**，填入支持 DoH 的 DNS：
   - **Cloudflare**：`1.1.1.1` 和 `1.0.0.1`
   - **Google**：`8.8.8.8` 和 `8.8.4.4`
   - **Quad9**：`9.9.9.9`

**⚠ 注意**：Windows 10 仅对 **系统自带的 DNS 解析器**启用 DoH，部分 VPN、代理或企业网络可能会绕过此设置。

------

### **📌 3. 测试 DoH 是否生效**

你可以使用 Cloudflare 的 DoH 测试页面： 🔗 https://1.1.1.1/help
 如果 **Using DNS over HTTPS (DoH) = Yes**，说明生效了。

------

### **🚀 结论**

Windows 10 **可以**配置系统级别的 DoH，但需要**手动修改注册表**。如果不想折腾，可以直接在 **Chrome / Firefox / Edge** 里启用 DoH，这样更简单。🚀 你是想在 Windows 10 上测试 DoH，还是考虑用于企业环境？ 😃