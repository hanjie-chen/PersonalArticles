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