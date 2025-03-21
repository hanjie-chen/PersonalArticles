# document root

Nginx 的 **document root** 是指服务器用来存放静态文件（如 HTML、CSS、JavaScript、图片等）的目录。当客户端请求一个静态资源时，Nginx 会从这个目录中查找并返回相应的文件。



在 nginx:alpine 这个 Docker 镜像中，默认的 document root 是 `/usr/share/nginx/html`

当你将静态资源挂载到这个目录或者它的子目录下时，无需额外修改配置，nginx 就能够直接提供这些内容。

这是因为默认的配置通常定义了 `/usr/share/nginx/html` 作为静态文件的根目录。这意味着，如果你希望 nginx 为你的站点提供静态内容，把文件放在这个目录下或其子目录中，可以无缝配合默认配置而不用做额外调整。



# `/etc/nginx/nginx.conf`

`nginx.conf` 是 nginx 的主配置文件，nginx:alpine container 的 `nginx.conf` 文件内容如下所示

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

