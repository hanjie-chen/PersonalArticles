当我们使用 Dockerfile 来 build 我们自己的 image 的时候。往往会用来 `RUN`, `COPY`, `WORKDIR` 等指令

但是这些指令在 contianer 中默认是由什么 user 来运行呢？

一般来说，OS-based image, 例如 debian, ubuntu, centos 默认是 root user, 因为这些image的初始化目的往往是需要 root 权限的系统设置，例如下载依赖包，配置服务等

但是对于 Application-based image, 例如 python:3.9-slim, nginx:latest 这种，往往默认则是一个 non-root user