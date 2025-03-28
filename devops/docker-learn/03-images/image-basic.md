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

## Stable Tag VS. Rolling Tags

### Stable Tags

Stable Tags 是固定的、版本化的标签，通常对应于某个特定的软件版本或镜像构建。它们不会随着新的更新而改变内容。

通常以具体的版本号命名，例如 `4.4-nginx-2024081121389` 或 `4.8-openresty-alpine-fat-2024081121389`。

一旦一个稳定标签被创建，它的内容（镜像的代码、依赖等）就不会再改变，除非手动重新发布。

适合生产环境使用，因为它们提供了可预测性和稳定性。你可以确信使用某个稳定标签的镜像不会因为上游更新而意外改变。

### Rolling Tags

Rolling Tags 是动态的标签，会随着新的版本发布而更新，指向最新的镜像内容。

通常是更通用的名称，例如 `nginx` 或 `apache-alpine`。

每次有新的稳定版本发布时，滚动标签会自动更新，指向最新的稳定版本。

所以它们在生产环境中使用时可能会带来风险（例如新版本引入了不兼容的更改），无法保证每次拉取镜像时得到的内容是相同的。

往往用于开发或测试环境中，快速获取最新版本的镜像。

### In a word

Stable Tags 和 Rolling Tags 是一种常见的 Docker 镜像标签管理方式，但并不是所有 Docker 镜像都必须同时支持这两种标签。这取决于镜像维护者的设计和策略。

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
