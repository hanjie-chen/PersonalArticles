# `conf.d/` directory

额外的站点配置目录，用于存放各个网站的 `server` 配置文件，通常 `nginx.conf` 会 `include` 这个目录下的所有 `.conf` 文件。

例如

`/etc/nginx/conf.d/default.conf`

`/etc/nginx/conf.d/my-site.conf`



## `default.conf`

在 nginx:alpine 镜像中，默认会有一个配置文件：/etc/nginx/conf.d/default.conf。这个文件定义了默认的 server 块和 document root。

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

让我们详细分析一下每行代码都是什么意思

最开头的 server {}: 定义一个虚拟服务器实例

```nginx
listen       80;
server_name  localhost;

#access_log  /var/log/nginx/host.access.log  main;
```

**listen 80**: 指定服务器监听的端口，这里是80端口(HTTP默认端口) 

**server_name localhost**: 定义服务器的域名，这里设置为localhost 

**access_log**: 这行被注释掉了，如果取消注释，它会启用访问日志记录，所有的访问请求将记录到指定的文件中。

> [!note]
>
> 这里的 **"main"** 实际上是指向一个日志格式的名称。在Nginx配置中，你可以预先定义多种不同的日志格式，并为每种格式指定一个名称。"main" 是在 Nginx 的主配置文件中（通常是 `/etc/nginx/nginx.conf`）预定义的一个标准日志格式。

### `location /` block

```nginx
location / {
    root   /usr/share/nginx/html;
    index  index.html index.htm;
}
```

- **location /**: 匹配请求的URI路径，"/"表示根路径 
- **root**: 指定网站文件的根目录，这里是容器内的 `/usr/share/nginx/html` 目录 
- **index**: 定义默认首页文件，路径相对于 root 指令定义的目录路径的。 
  - Nginx 会在 `/usr/share/nginx/html` 目录下查找 `index.html` 文件
  - 如果找不到 `index.html`，则会查找 `/usr/share/nginx/html/index.htm` 文件

### error message

```nginx
#error_page  404              /404.html;

# redirect server error pages to the static page /50x.html
#
error_page   500 502 503 504  /50x.html;
location = /50x.html {
    root   /usr/share/nginx/html;
}
```

- error_page 404: 如果取消注释，那么路径则是 `/404.html` 会去匹配 `location /` block 实际路径是 `/usr/share/nginx/html/404.html`
- error_page 5xx: 使用 location  精确匹配去 `/usr/share/nginx/html` 种寻找 50x.html



# document root

Nginx 的 **document root** 是指服务器用来存放静态文件（如 HTML、CSS、JavaScript、图片等）的目录。当客户端请求一个静态资源时，Nginx 会从这个目录中查找并返回相应的文件。

在 nginx:alpine 这个 Docker 镜像中，默认的 document root 是 `/usr/share/nginx/html`

当你将静态资源挂载到这个目录或者它的子目录下时，无需额外修改配置，nginx 就能够直接提供这些内容。

这是因为默认的配置通常定义了 `/usr/share/nginx/html` 作为静态文件的根目录。这意味着，如果你希望 nginx 为你的站点提供静态内容，把文件放在这个目录下或其子目录中，可以无缝配合默认配置而不用做额外调整。

