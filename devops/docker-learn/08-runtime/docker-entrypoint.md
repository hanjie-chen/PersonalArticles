本片笔记考虑放在 container-entrypoint.md 文章末尾 title: best practice

# background

在学习 `owasp/modsecurity:nginx-alpine` 的时候发现，在这个 image 的根路径中存在一个 `docker-entrypoint.sh` 文件用于初始化一些东西，从这个 container 启动的 log 中可以看出一些痕迹

```shell
nginx-modsecurity  | /docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
nginx-modsecurity  | /docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
...
```

> [!note]
>
> `owasp/modsecurity:nginx-alpine` 这个 image 是基于 `nginx-alpine` 构建的，所以其实这个 `/docker-entrypoint.sh` 来自于 `nginx-alpine` image

而接下来要探讨的就是这个 `docker-entrypoint.sh` 作为 best practice

# `docker-entrypoint.sh`

不是所有 Docker 镜像都有 `docker-entrypoint.sh`，但很多“设计良好的”、“生产用途”的镜像都会有，特别是：

- 官方基础镜像（如 nginx、mysql、postgres、redis 等）；
- 多阶段构建或需要初始化逻辑的镜像；
- 构建者为了简化部署流程，会加入 entrypoint 脚本做自动化工作。

但“最基础”的镜像，如 `alpine`, `ubuntu`, `debian` 这些**基础操作系统镜像**是**没有**这个脚本的。因为它们不需要初始化程序或特殊逻辑。



每个镜像通常都有自己定制的 `docker-entrypoint.sh`，根据服务的需求来写。

- nginx 的脚本会处理 `nginx` 的参数；
- postgres 的脚本会初始化数据库并设置用户密码；
- redis 的脚本会检查挂载路径等；

所以说，这是一种 **Docker 镜像作者常用的 Best Practice（最佳实践）**，不是标准，但很常见。