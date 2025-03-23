# `/etc/nginx` directory

在 Nginx 容器（或系统安装的 Nginx）中，`/etc/nginx/` 目录主要用于存放 Nginx 的配置文件。例如

```shell
/etc/nginx # ls
conf.d  fastcgi.conf  fastcgi_params  mime.types  modules  nginx.conf  scgi_params  uwsgi_params
```

接下来，我们将详细解析列出的文件和目录的作用：





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

