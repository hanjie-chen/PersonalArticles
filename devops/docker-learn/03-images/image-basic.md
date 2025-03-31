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

# `docker images` command

当我们使用 `docker images` 命令的时候，就会发现可能会出现奇怪的的 dangling images:

```shell
$ docker images
REPOSITORY              TAG       IMAGE ID       CREATED       SIZE
website-web-app         latest    2db53ba692a3   4 days ago    177MB
<none>                  <none>    984f65eb163d   2 weeks ago   177MB
website-articles-sync   latest    448d2ca47dfe   2 weeks ago   18.8MB
<none>                  <none>    2c113072ff30   2 weeks ago   167MB
<none>                  <none>    8816ede22564   2 weeks ago   18.8MB
nginx                   alpine    1ff4bb4faebc   7 weeks ago   47.9MB
```

出现 `<none>:<none>` 的镜像的原因

1. 镜像构建过程中的中间产物或旧版本被覆盖：
   
   当使用 `docker build` 构建一个镜像时，如果之前已经有同名镜像（比如 `website-web-app:latest`），新构建的镜像会取代旧的镜像。旧的镜像失去了它的标签（`tag`），变成了 `<none>:<none>`。
   
2. 手动删除标签：
   
   如果手动移除了某个镜像的标签（例如通过 `docker rmi <tag>` 或 `docker tag` 修改），但镜像本身没有被彻底删除，它就会变成 `<none>:<none>`
   
3. 多阶段构建（Multi-stage Build）的副产物：
   
   如果你在 Dockerfile 中使用了多阶段构建，中间阶段的镜像可能会在构建完成后失去引用，变成悬空镜像。


## clear dangling images
这些悬空镜像占用了磁盘空间，如果你确定不需要它们，可以使用下面的方式清理掉：

1. **清理所有悬空镜像**：
   
   ```bash
   docker image prune
   ```
   这会删除所有没有被任何容器引用且没有标签的镜像（即 `<none>:<none>` 的镜像）。
   
2. **清理未使用的镜像、容器、网络等**：
   如果你想更彻底地清理，可以运行：
   ```bash
   docker system prune
   ```
   注意：这会删除所有未被使用的资源（包括停止的容器、悬空镜像等），请确认没有重要数据后再执行。

3. **手动删除特定镜像**：
   如果只想删除某个特定的 `<none>:<none>` 镜像，可以用：
   ```bash
   docker rmi 984f65eb163d
   ```



## 如何避免产生过多悬空镜像？

- **使用具体的标签**：在构建镜像时，避免总是用 `latest`，可以用版本号或其他有意义的标签，例如 `website-web-app:v1.0`。
- **定期清理**：养成定期运行 `docker image prune` 的习惯。
- **检查构建过程**：如果使用多阶段构建，确保只保留最终需要的镜像。
