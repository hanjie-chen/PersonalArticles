如果我们需要一个 nginx 的 container 作为我们 web app 的反向代理，我们应该如何操作呢？

在你的项目根目录下新建一个文件夹，例如 `nginx/conf.d`，并在其中创建一个配置文件（如 `default.conf`）。配置文件内容示例如下：

```nginx
# nginx/conf.d/default.conf

upstream webapp {
    # web-app 容器名称和内部端口
    server web-app:5000;
}

server {
    listen       80;
    server_name  localhost;

    location / {
        proxy_pass http://webapp;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

这个配置文件做了以下工作：

- 定义了一个 `upstream`，将请求转发到服务名为 `web-app` 的容器上（在 Docker 内部网络中，容器名可直接被解析）。
- 监听 80 端口，对于所有请求通过 `proxy_pass` 指令转发到 upstream 中。

在你的 `compose.yml` 文件中新增 nginx 服务。修改后的 `compose.yml` 示例：

```yaml
  nginx:
    image: nginx:alpine
    container_name: nginx
    ports:
      - "80:80"
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d
      # 可选：挂载日志目录
      - ./nginx/logs:/var/log/nginx
    depends_on:
      - web-app
```

nginx 目录

```shell
├── nginx
│   ├── conf.d
│   │   └── default.conf
│   └── logs
```



## 为什么是 `nginx/conf.d`

Nginx 官方镜像默认的主配置文件（通常是 `/etc/nginx/nginx.conf`）中已经写好了一条指令：

```nginx
include /etc/nginx/conf.d/*.conf;
```

这意味着 Nginx 会自动加载 `/etc/nginx/conf.d/` 目录下所有以 `.conf` 结尾的配置文件。

因此，我们通常会在本地项目中建立一个文件夹（例如 `nginx/conf.d`）并在里面放入我们定制的配置文件（比如 `default.conf`），然后在 docker-compose.yml 中将这个文件夹挂载到容器内的 `/etc/nginx/conf.d`。



## `default.conf` file

`default.conf` 是一个 Nginx 的配置文件，用于定义 Nginx 的行为，也就是告诉 Nginx 当它启动后如何处理传入的 HTTP 请求。详细来说，这个文件中通常会包含以下几部分内容：

### Server Block

这是 Nginx 的核心部分之一。在一个 server 块中，你可以指定 Nginx 应该监听哪个端口（例如：80 或 443），以及当请求匹配某个 server_name（域名）时，如何处理请求。例如，你可以设置：

- **监听端口**：`listen 80;` 表示 Nginx 监听 80 端口。
- **服务器名称**：`server_name localhost;` 指定了域名或主机名。

### Location Block

在 server 块内，你可以定义一个或多个 location 块来匹配特定的 URL 路径。例如：当请求路径为 `/` 或其他路径时应如何处理。
在反向代理的场景下，location 块内通常会包含 `proxy_pass` 指令，用来将请求转发到后端的 Web 服务器或应用容器。例如：

```nginx
location / {
    proxy_pass http://webapp;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

### Upstream 模块

有时你需要定义一个后端服务组，这就是 upstream 模块的用途。通过 upstream，可以定义一个或多个后台服务器，Nginx 会将请求分发到这些服务器中。这在做负载均衡时非常有用。例如：

```nginx
upstream webapp {
    server web-app:5000;
}
```

在这个例子里，我们定义了一个名为 `webapp` 的服务组，其内的服务器对应 web-app 容器的 5000 端口。