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

# download image - `docker pull`

下载 Docker 镜像的基本命令是：

```bash
docker pull <image-name>
```

e.g.

```shell
$ docker images
REPOSITORY              TAG       IMAGE ID       CREATED       SIZE
website-web-app         latest    2db53ba692a3   9 days ago    177MB
website-articles-sync   latest    448d2ca47dfe   3 weeks ago   18.8MB
nginx                   alpine    1ff4bb4faebc   7 weeks ago   47.9MB

$ docker pull owasp/modsecurity:nginx-alpine
nginx-alpine: Pulling from owasp/modsecurity
213ec9aee27d: Pull complete
864534705ce1: Pull complete
fe2c9e7418f8: Pull complete
f08ef11b2dfc: Pull complete
36f0053ae033: Pull complete
e47e25891bf2: Pull complete
4c031bee5bcb: Pull complete
fef8f2051ac1: Pull complete
8584876a8ff9: Pull complete
8a170b411969: Pull complete
98a3c898933f: Pull complete
fcd0b9f1a321: Pull complete
6faa179269b4: Pull complete
15f7e4ed297d: Pull complete
33e3004d1266: Pull complete
b1d509b219c0: Pull complete
e4ccc158aa70: Pull complete
43d5536979ce: Pull complete
864dd6527889: Pull complete
6927f3372eae: Pull complete
c8a5877ffbaf: Pull complete
4f4fb700ef54: Pull complete
Digest: sha256:c9c6652f254743f85c0249d59fd31b6e31c46676ae3baeef312cf056eba600b3
Status: Downloaded newer image for owasp/modsecurity:nginx-alpine
docker.io/owasp/modsecurity:nginx-alpine

$ docker images
REPOSITORY              TAG            IMAGE ID       CREATED       SIZE
website-web-app         latest         2db53ba692a3   9 days ago    177MB
website-articles-sync   latest         448d2ca47dfe   3 weeks ago   18.8MB
nginx                   alpine         1ff4bb4faebc   7 weeks ago   47.9MB
owasp/modsecurity       nginx-alpine   89bf1ae1b8fa   2 years ago   73.8MB
```

## 多行哈希值？

在 `docker pull` 命令中我们可以看到多行的类似于哈希值一样的东西，它们其实是镜像层 (Image Layers) 的 ID

Docker 镜像不是一个单一的大文件，而是由多个只读层（Layers）叠加组成的。每一层都代表了 Dockerfile 中的一条指令（如 `RUN`, `COPY`, `ADD` 等）或者基础镜像的一层。

那些类似 `213ec9aee27d` 的字符串是每一层的（短）内容哈希 ID (Layer ID or Digest)。Docker 通过这些 ID 来唯一识别每一层。

每一行 `xxxx: Pull complete` 表示 Docker 客户端已经成功地从镜像仓库（Registry）下载了对应 ID 的那一层文件。

这样子有什么好处？
*   **缓存和复用：** 如果你本地已经有了某个镜像层（可能来自另一个镜像），Docker 就不会重新下载它，你会看到 `Already exists` 而不是 `Pull complete`。这大大加快了镜像拉取和构建的速度，也节省了磁盘空间。
*   **增量更新：** 当镜像更新时，通常只需要下载发生变化的层。



## Digest hash

Digest  是整个镜像清单的内容哈希值，通常使用 SHA256 算法计算（所以前缀是 `sha256:`）。

镜像的 `REPOSITORY:TAG` (如 `owasp/modsecurity:nginx-alpine`) 是可以改变的。同一个 `tag` (比如 `latest` 或 `nginx-alpine`) 可能在不同时间指向不同的镜像版本。但是，`Digest` 是根据镜像内容（具体来说是镜像清单，它引用了所有层和配置）计算出来的，只要镜像内容不变，`Digest` 就不会变。它提供了一种绝对精确、不可变的方式来引用一个特定的镜像版本。

你可以使用 `docker pull owasp/modsecurity@sha256:c9c6...` 来拉取这个精确版本的镜像，即使 `nginx-alpine` 标签后来被更新指向了别的镜像。



## docker.io

当你使用 `docker pull` 或 `docker run` 等命令，并且只提供了 `repository/image:tag`（如 `owasp/modsecurity:nginx-alpine`）或者只提供了 `image:tag`（对于官方镜像，如 `nginx:alpine`），Docker 客户端会默认去 `docker.io` (Docker Hub) 查找这个镜像。

所以，`docker pull owasp/modsecurity:nginx-alpine` 和 `docker pull docker.io/owasp/modsecurity:nginx-alpine` 是等效的。

命令执行完成后，Docker 会显示镜像的完整规范名称，其中就包括了默认的仓库主机名 `docker.io`

如果你想从其他私有或公共仓库拉取镜像，你就需要在镜像名称前加上仓库的主机名 e.g.

```shell
docker pull myregistry.example.com/myimage:latest
```







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

1. 清理所有悬空镜像：
   
   ```bash
   docker image prune
   ```
   这会删除所有没有被任何容器引用且没有标签的镜像（即 `<none>:<none>` 的镜像）。
   
2. 清理未使用的镜像、容器、网络等：
   如果你想更彻底地清理，可以运行：
   
   ```bash
   docker system prune
   ```
   注意：这会删除所有未被使用的资源（包括停止的容器、悬空镜像等），请确认没有重要数据后再执行。
   
3. 手动删除特定镜像：
   如果只想删除某个特定的 `<none>:<none>` 镜像，可以用：
   
   ```bash
   docker rmi 984f65eb163d
   ```



## 如何避免产生过多悬空镜像？

- 使用具体的标签：在构建镜像时，避免总是用 `latest`，可以用版本号或其他有意义的标签，例如 `website-web-app:v1.0`。
- 定期清理：养成定期运行 `docker image prune` 的习惯。
- 检查构建过程：如果使用多阶段构建，确保只保留最终需要的镜像。



# 删除

要删除某个 Docker 镜像，可以使用以下命令：

```bash
docker rmi <image_name_or_id>
```

### 示例：

```bash
docker rmi my-image:latest
```

或者使用镜像的 ID：

```bash
docker rmi 123abc456def
```

------

### 注意事项：

1. **镜像正在被容器使用时无法删除**
    如果该镜像正被某个容器使用（即使容器已停止），你会看到类似以下错误：

   ```
   Error response from daemon: conflict: unable to remove repository reference ...
   ```

   你需要先删除对应的容器，或使用 `-f` 强制删除镜像：

   ```bash
   docker rmi -f <image_name_or_id>
   ```

2. **列出所有镜像**
    查看你本地的镜像列表，可以使用：

   ```bash
   docker images
   ```
