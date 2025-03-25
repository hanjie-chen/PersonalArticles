# `nginx.conf`

Nginx 的全局主配置文件，控制 Nginx 的基本行为，包括 worker 进程数量、日志路径、连接管理等

例如

```nginx
user  nginx;
worker_processes  auto;

error_log  /var/log/nginx/error.log notice;
pid        /var/run/nginx.pid;

events {
    worker_connections  1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    keepalive_timeout  65;

    #gzip  on;

    include /etc/nginx/conf.d/*.conf;
}
```

其中最后一行代码

```nginx
include /etc/nginx/conf.d/*.conf;
```

这行配置告诉 Nginx，它会加载 /etc/nginx/conf.d/ 目录下所有以 .conf 结尾的配置文件。

所以大多数情况下，你不需要直接修改 `nginx.conf`，而是在 `conf.d/` 目录里新增站点配置。



## log format

在 nginx.conf 中，通常能找到 main 日志格式的定义

```nginx
http {
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    # 其他配置...
}
```

#### 这个格式包含以下信息：

1. `$remote_addr` - 客户端 IP 地址
2. `$remote_user` - 客户端用户名称(通常为 "-")
3. `$time_local` - 服务器本地时间
4. `$request` - 完整的 HTTP 请求行
5. `$status` - 响应状态码
6. `$body_bytes_sent` - 发送给客户端的字节数
7. `$http_referer` - 请求的来源页面 URL
8. `$http_user_agent` - 客户端浏览器标识
9. `$http_x_forwarded_for` - 代理服务器转发的客户端 IP

使用 "main" 格式记录的日志看起来可能像这样：

```log
192.168.1.10 - - [24/Mar/2025:10:15:32 +0000] "GET /index.html HTTP/1.1" 200 1234 "https://example.com" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" "-"
```

可以自定义 log 格式，但是在哪里定义呢？难道是在 nginx.conf 文件里面吗？