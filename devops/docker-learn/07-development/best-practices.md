如果遇到这样一个问题

有一个 flask web app 运行在一个 container 上，这个 flask web app 需要从一个 /articles-data 目录拿取数据，而这个目录则是一个 github repository, 需要使用 cron 服务定期的 git pull 以保持最新的状态

而目前 falsk web app 使用的是 python: 3.9-slim 的镜像，导致没有 git, cron 等服务，需要重新下载，而 cron 服务由于 docker 的特殊性

- Docker 容器默认不运行完整的 init 系统（如 systemd）
- 容器启动时只运行 CMD 或 ENTRYPOINT 指定的主进程

又因为

- 安装 cron 包只是将程序文件复制到系统中
- 在传统 Linux 系统中，服务是由 init 系统（如 systemd）自动启动的

所以需要手动启动 cron 服务

这个时候应该怎么办？

可以尝试把这些服务都安装到同一个 container 中，但是这样要考虑同时启动了 flask web app 之后，又要启动 cron 服务，又会遇到一个进程管理的问题，虽然可以写一个启动脚本例如

```bash
#!/bin/bash
service cron start
flask run --host=0.0.0.0 --debug
```

或者使用 `supervisord` 这样子的进程管理工具，配置 supervisord.conf

```json
[supervisord]
nodaemon=true

[program:cron]
command=/usr/sbin/cron -f
autostart=true
autorestart=true

[program:flask]
command=flask run --host=0.0.0.0 --debug
autostart=true
autorestart=true
```

并且还需要在 Dockerfile 额外下载 `supervisord`

```dockerfile
RUN apt-get update && apt-get install -y supervisor cron
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
CMD ["/usr/bin/supervisord"]
```

但是 Docker 是单进程模型，也就是一个容器一个服务，我们更倾向于在另一个容器中启动 cron 和 git 并且将 github repository 放到另一个 conianer 中去，然后使用 docker compose 管理多个容器

在 [Best practices | Docker Docs](https://docs.docker.com/build/building/best-practices/#decouple-applications) 提到

> Each container should have only one concern. Decoupling applications into multiple containers makes it easier to scale horizontally and reuse containers. For instance, a web application stack might consist of three separate containers, each with its own unique image, to manage the web application, database, and an in-memory cache in a decoupled manner.

简单来说就是：一个容器应该只运行一个应用或进程

# Reference

[Best practices | Docker Docs](https://docs.docker.com/build/building/best-practices/)