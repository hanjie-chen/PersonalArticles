# Docker image



## image name convention

reference: [docker image tag | Docker Docs](https://docs.docker.com/reference/cli/docker/image/tag/#extended-description)

Docker 镜像的命名通常遵循以下格式：

```dockerfile
[repository]/[image-name]:[tag]
```

`repository` 这是 Docker 镜像的命名空间，用于区分镜像的来源

`image-name` 镜像名称，往往用于表明镜像的主要功能或者核心组件

`tag` 镜像标签，具体说明镜像的变体，帮助用户选择特定版本或配置

例如

```dockerfile
owasp/modsecurity:nginx-alpine
```

`owasp/`

这是 OWASP 社区提供的官方镜像，由 OWASP 组织维护。

`modsecurity`

表明该镜像的主要功能是提供 ModSecurity WAF

`:nginx-alpine`

表示这个镜像包含 Nginx Web 服务器，基础操作系统是 Alpine Linux。

## down image

下载 Docker 镜像的基本命令是：

```bash
docker pull [镜像名称]:[标签]
```

一些使用示例：

1. 下载最新版本的镜像（默认 tag 为 latest）：
```bash
docker pull ubuntu
```

2. 下载指定版本的镜像：
```bash
docker pull ubuntu:20.04
```

3. 从特定仓库下载镜像：
```bash
docker pull registry.example.com/ubuntu:20.04
```

一些常用的参数：
- `-a` 或 `--all-tags`：下载仓库中的所有标签
- `--disable-content-trust`：跳过镜像验证
- `--platform`：指定平台，如 linux/amd64, linux/arm64 等

下载完成后，你可以使用 `docker images` 命令查看已下载的镜像列表。
