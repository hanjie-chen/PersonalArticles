# auth

## Nginx Basic Auth（基本身份验证）

这是一种最基础、最通用的网页加密方式。它通过浏览器弹出的原生对话框要求你输入用户名和密码。

非常适合用来保护后台管理页面、个人博客的测试版，或者是一些不希望被搜索引擎抓取的内部工具。

### 原理：

1. 请求： 客户端请求一个受保护的页面。
2. 挑战： Nginx 返回 `401 Unauthorized` 响应，并在 Header 中告诉浏览器：“嘿，你需要提供账号密码”。
3. 响应： 浏览器弹出对话框，你输入信息后，浏览器将其拼接成 `用户名:密码` 的格式，进行 Base64 编码，并放在请求头中发回给 Nginx。
4. 授权： Nginx 校验编码后的字符串是否与服务器上的记录一致。

### 配置：

第一步：创建密码文件

你需要一个存储用户名和加密密码的文件。通常使用 `htpasswd` 工具（来自 `apache2-utils` 或 `httpd-tools` 包）。

Bash

```
# 创建一个名为 .htpasswd 的文件，并添加用户 "admin"
# 系统会提示你输入并确认密码
sudo htpasswd -c /etc/nginx/.htpasswd admin
```

第二步：修改 Nginx 配置文件

在你的 `server` 或 `location` 块中添加两行指令：

Nginx

```
server {
    listen 80;
    server_name example.com;

    location /admin {
        # 弹窗上显示的提示信息（部分浏览器可能不显示）
        auth_basic "Restricted Access"; 
        
        # 指定密码文件的路径
        auth_basic_user_file /etc/nginx/.htpasswd; 

        proxy_pass http://localhost:8080;
    }
}
```

修改完成后，记得重载 Nginx：`sudo nginx -s reload`。

> [!note]
>
> - 配合 HTTPS：在 HTTP 下使用 Basic Auth 等于把密码大声喊出来。
> - 隐藏文件：确保 `.htpasswd` 文件不在网站的根目录下，防止被直接下载。
> - 配合 IP 白名单：如果想更安全，可以结合 `allow` 指令，只允许特定 IP 访问。