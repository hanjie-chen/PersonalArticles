# `/etc/nginx` directory

在 Nginx 容器（或系统安装的 Nginx）中，`/etc/nginx/` 目录主要用于存放 Nginx 的配置文件。例如

```shell
/etc/nginx # ls
conf.d  fastcgi.conf  fastcgi_params  mime.types  modules  nginx.conf  scgi_params  uwsgi_params
```

接下来，我们将详细解析列出的文件和目录的作用：

## `nginx.conf`

Nginx 的全局主配置文件，控制 Nginx 的基本行为，包括 worker 进程数量、日志路径、连接管理等。

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

所以大多数情况下，你不需要直接修改 `nginx.conf`，而是在 `conf.d/` 目录里新增站点配置。



## `conf.d/` directory

额外的站点配置目录，用于存放各个网站的 `server` 配置文件，通常 `nginx.conf` 会 `include` 这个目录下的所有 `.conf` 文件。

例如

`/etc/nginx/conf.d/default.conf`

`/etc/nginx/conf.d/my-site.conf`

一个经典的 `default.conf` 文件内容如下

```nginx
server {
    listen       80;
    server_name  localhost;

    #access_log  /var/log/nginx/host.access.log  main;

    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
    }

    #error_page  404              /404.html;

    # redirect server error pages to the static page /50x.html
    #
    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }

    # proxy the PHP scripts to Apache listening on 127.0.0.1:80
    #
    #location ~ \.php$ {
    #    proxy_pass   http://127.0.0.1;
    #}

    # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
    #
    #location ~ \.php$ {
    #    root           html;
    #    fastcgi_pass   127.0.0.1:9000;
    #    fastcgi_index  index.php;
    #    fastcgi_param  SCRIPT_FILENAME  /scripts$fastcgi_script_name;
    #    include        fastcgi_params;
    #}

    # deny access to .htaccess files, if Apache's document root
    # concurs with nginx's one
    #
    #location ~ /\.ht {
    #    deny  all;
    #}
}

```



## `mime.types`（MIME 类型映射表）

定义文件扩展名和 MIME 类型的对应关系，告诉 Nginx 如何返回 `Content-Type` 头。





## `fastcgi.conf` & `fastcgi_params`

FastCGI 相关配置，用于 FastCGI 代理（例如连接 PHP-FPM）时的参数定义。



## `scgi_params`

用于 SCGI（Simple Common Gateway Interface）协议的代理设置，类似于 FastCGI，不常用，大多数情况下你不会修改它，除非你要代理 SCGI 应用。



## `uwsgi_params`

用于 Nginx 代理 uWSGI 应用，比如 Python 的 Flask/Django uWSGI 服务器。

如果你用 Flask + uWSGI + Nginx，这个文件会被用到。



## `modules/`

存放 Nginx 的动态模块（`.so` 文件），可用于扩展 Nginx 功能。

