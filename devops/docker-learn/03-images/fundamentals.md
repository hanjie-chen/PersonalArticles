# Docker image

在 02-container 中，我们已经直接操作了 container，但 container 不是凭空产生的，它总是基于 image 启动

这一章不再讲 container 操作，而是聚焦 image 本身的标识、拉取和本地管理

# 如何标识一个 image

## image name

Docker 镜像的命名通常遵循以下格式：

```dockerfile
[registry-host]/[namespace]/[repository]:[tag]
```

- registry-host: 如果不写，默认去 docker.io 找
- namespace: 命名空间，用于区分镜像的来源
- repositoryu: 镜像名
- tag: 标签，具体说明镜像，用于选择特定版本或配置

例如

```dockerfile
owasp/modsecurity:nginx-alpine
```

- `owasp/`: OWASP 社区提供的官方镜像，由 OWASP 组织维护。
- `modsecurity`: reposiroty该镜像的主要功能是提供 ModSecurity WAF
- `nginx-alpine`: tag,表示这个镜像包含 Nginx Web 服务器，基础操作系统是 Alpine Linux。

## Stable / Rolling Tags

### Stable Tags

Stable Tags 是固定的、版本化的标签，通常对应于某个特定的软件版本或镜像构建。它们不会随着新的更新而改变内容。

通常以具体的版本号命名，例如 `4.4-nginx-2024081121389` 或 `4.8-openresty-alpine-fat-2024081121389`。

适合生产环境使用，因为它们提供了可预测性和稳定性。

### Rolling Tags

Rolling Tags 是动态的标签，会随着新的版本发布而更新，指向最新的镜像内容。

通常是更通用的名称，例如 `nginx` 或 `apache-alpine`。

往往用于开发或测试环境中，快速获取最新版本的镜像。

## registry-host

### Docker hub

Docker Hub 是 Docker 公司提供的官方云端容器镜像仓库服务。

它可以理解为 docker image 的 GitHub，专门用来存储、分发和管理 Docker 镜像的。

用户可以将自己构建的镜像推送到 Docker Hub，也可以从中拉取官方或其他开发者共享的镜像

limitation: 免费用户只能拥有 1 个 private repository 和无限多的 public repository

### GHCR

github container registry(GHCR) 类似于 docker hub 是用于存储 image 的地方，与 docker hub 不同的是它并没有一个独立的网站，而是在 github 主页的 package 页面，

例如 https://github.com/hanjie-chen?tab=packages



# pull images

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

## docker.io

当使用 `docker pull/run` ，并且只提供了 `repository/image:tag`（如 `owasp/modsecurity:nginx-alpine`）或者只提供了 `image:tag`（对于官方镜像，如 `nginx:alpine`），Docker 客户端会默认去 `docker.io` (Docker Hub) 查找这个镜像。

所以，`docker pull owasp/modsecurity:nginx-alpine` 和 `docker pull docker.io/owasp/modsecurity:nginx-alpine` 是等效的。

命令执行完成后，Docker 会显示镜像的完整规范名称，其中就包括了默认的仓库主机名 `docker.io`

如果想从其他仓库拉取镜像，需要在镜像名称前加上仓库的主机名，例如

```shell
docker pull myregistry.example.com/myimage:latest
```

## Digest hash

Digest  是整个镜像清单的内容哈希值，通常使用 SHA256 算法计算（所以前缀是 `sha256:`）。

镜像的 `REPOSITORY:TAG` (如 `owasp/modsecurity:nginx-alpine`) 是可以改变的。同一个 `tag` (比如 `latest` 或 `nginx-alpine`) 可能在不同时间指向不同的镜像版本。但是，`Digest` 是根据镜像内容（具体来说是镜像清单，它引用了所有层和配置）计算出来的，只要镜像内容不变，`Digest` 就不会变。它提供了一种绝对精确、不可变的方式来引用一个特定的镜像版本。

你可以使用 `docker pull owasp/modsecurity@sha256:c9c6...` 来拉取这个精确版本的镜像，即使 `nginx-alpine` 标签后来被更新指向了别的镜像。



# 4. 如何理解 docker pull 的输出

这里放：

- 多行哈希值其实是 layer
- layer 为什么能复用
- digest 为什么更精确
- 为什么有时显示 Already exists

这一节是把你现在 image-basic.md 里比较零碎但很有价值的解释，变成“命令输出阅读课”。

## 多行哈希值？

在 `docker pull` 命令中我们可以看到多行的类似于哈希值一样的东西，它们其实是镜像层 (Image Layers) 的 ID

Docker 镜像不是一个单一的大文件，而是由多个只读层（Layers）叠加组成的。每一层都代表了 Dockerfile 中的一条指令（如 `RUN`, `COPY`, `ADD` 等）或者基础镜像的一层。

那些类似 `213ec9aee27d` 的字符串是每一层的（短）内容哈希 ID (Layer ID or Digest)。Docker 通过这些 ID 来唯一识别每一层。

每一行 `xxxx: Pull complete` 表示 Docker 客户端已经成功地从镜像仓库（Registry）下载了对应 ID 的那一层文件。

这样子有什么好处？

*   **缓存和复用：** 如果你本地已经有了某个镜像层（可能来自另一个镜像），Docker 就不会重新下载它，你会看到 `Already exists` 而不是 `Pull complete`。这大大加快了镜像拉取和构建的速度，也节省了磁盘空间。
*   **增量更新：** 当镜像更新时，通常只需要下载发生变化的层。

# List Local Images

我们可以使用 `docker image ls` 命令来查看本地存在的 images

> [!note]
>
> 等价于旧版 `docker images` 命令
>
> 在 Docker 早期，命令设计比较“随性”，所有的操作都直接挂在 `docker` 后面（如 `docker images`, `docker rmi`, `docker ps`）。随着功能增加，命令变得非常混乱。
>
> 为了统一规范，Docker 引入了管理命令（Management Commands）的概念，将命令按操作对象分类：
>
> - `docker image`：负责镜像相关（ls, rm, build...）
> - `docker container`：负责容器相关（ls, stop, rm...）
> - `docker network`：负责网络相关
>
> 因此，`docker image ls` 是官方现在更推荐的写法，因为它符合 `docker <object> <action>` 的逻辑结构。

```shell
$ docker image ls
REPOSITORY              TAG       IMAGE ID       CREATED       SIZE
website-web-app         latest    2db53ba692a3   4 days ago    177MB
<none>                  <none>    984f65eb163d   2 weeks ago   177MB
website-articles-sync   latest    448d2ca47dfe   2 weeks ago   18.8MB
<none>                  <none>    2c113072ff30   2 weeks ago   167MB
<none>                  <none>    8816ede22564   2 weeks ago   18.8MB
nginx                   alpine    1ff4bb4faebc   7 weeks ago   47.9MB
```

其中每行的表示非常清晰，从仓库来源，到镜像大小



# dangling images

在我们使用 `docker image ls` 的时候，会发现一些奇怪的的 none images, 其实它们叫 dangling images

出现 dangling images 的原因

1. 镜像构建过程中的中间产物或旧版本被覆盖：

   当使用 `docker build` 构建一个镜像时，如果之前已经有同名镜像（比如 `website-web-app:latest`），新构建的镜像会取代旧的镜像。旧的镜像失去了它的标签（`tag`），变成了 `<none>:<none>`。

2. 手动删除标签：

   如果手动移除了某个镜像的标签（例如通过 `docker rmi <tag>` 或 `docker tag` 修改），但镜像本身没有被彻底删除，它就会变成 `<none>:<none>`

3. 多阶段构建（Multi-stage Build）的副产物：

   如果在 Dockerfile 中使用了多阶段构建，中间阶段的镜像可能会在构建完成后失去引用，变成悬空镜像。

如何避免产生过多悬空镜像？

- 使用具体的标签：在构建镜像时，避免总是用 `latest`，可以用版本号或其他有意义的标签，例如 `website-web-app:v1.0`。
- 定期清理：养成定期运行 `docker image prune` 的习惯。
- 检查构建过程：如果使用多阶段构建，确保只保留最终需要的镜像。

那么我们要如何删除与清理 image 呢？

# remove images

## docker rmi

要删除某个 Docker 镜像，可以使用以下命令：

```bash
docker rmi <image_name_or_id>
```

e.g.

```bash
# use image name
docker rmi my-image:latest
# or use image ID
docker rmi 123abc456def
```

镜像正在被容器使用时无法删除

如果该镜像正被某个容器使用（即使容器已停止），你会看到类似以下错误：

```
Error response from daemon: conflict: unable to remove repository reference ...
```

你需要先删除对应的容器，或使用 `-f` 强制删除镜像：

```bash
docker rmi -f <image_name_or_id>
```

## docker prune

使用命令 `docker image prune` 这会删除所有没有被任何容器引用且没有标签的镜像

或者使用命令`docker system prune` 一键全清理（镜像、容器、网络），这个命令会删除所有未被使用的资源（包括停止的容器、悬空镜像等），请确认没有重要数据后再执行。

## 0B

当我们使用 docker image purne 的时候发现

```shell
$ docker image prune
WARNING! This will remove all dangling images.
Are you sure you want to continue? [y/N] y
Deleted Images:
deleted: sha256:392c3571e7321948a10dccb39f7665236dfb7e3db1ba3a700f335880d5b9fa02
...
deleted: sha256:a7c5d2902a07beba2357e546d6d7fd9abe0cc64618fb4ef990e23ef6295ac6f1

Total reclaimed space: 0B
```

明明删除了那么多镜像，为什么最终释放的空间确实 0B 呢？这里涉及到了 Docker 镜像的“分层机制”。

要理解这个现象，我们需要区分两个概念：镜像（Images） 和 层（Layers）。

当执行 `docker image prune` 时，删除的是那些没有标签（TAG 为 `<none>`）且没有被任何容器使用的镜像。这通常发生在重新构建镜像（Build）后，旧的镜像层被新的覆盖，旧的就变成了“孤儿”。

Docker 镜像是像积木一样叠起来的。虽然删除了一些 dangling images 的引用，但这些镜像所包含的底层数据（Layers）可能还在被其他正在使用的镜像所引用。

只有当一个层（Layer）不再被任何镜像引用时，Docker 才会真正从磁盘上物理删除它。

- 刚才删除的那些 `sha256` 记录，很多时候只是元数据指针或者是已经包含在其他镜像中的中间层。
- 如果这些层仍然是某个活跃镜像（比如你的网站镜像）的一部分，Docker 就不会真的删除文件，自然也就没有空间被释放。

刚才的操作就像是清理了书架上的旧索引卡片，但书架上的书本身还在（因为其他索引还在用这些书）。虽然清理了“名义上”的冗余镜像，但实际占空间的二进制文件依然被保留着。

如果确定不需要保留任何没在运行的东西，可以使用更彻底的命令：

清理所有未使用的镜像（不只是虚悬的）：

```shell
docker image prune -a
```

注意：这会删除所有目前没有被容器使用的镜像，下次启动时可能需要重新拉取。