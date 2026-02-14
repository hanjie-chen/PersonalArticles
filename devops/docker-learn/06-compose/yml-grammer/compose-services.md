---
Title: docker compose.ymal services block 语法速查
Author: 陈翰杰
Instructor: o1-preview, grok3
CoverImage: ./images/cover-image.png
RolloutDate: 2025-01-16
---

```
BriefIntroduction: 
docker compose.ymal top level services block 语法速查
```

<!-- split -->

![docker compose](./images/cover-image.png)

# `compose.yml` –> services 语法详解

[Services top-level elements | Docker Docs](https://docs.docker.com/reference/compose-file/services/)



# `container name`

```
# 指定 contianer name
container_name: web-app
```

如果你没有指定 `container_name` Docker Compose 会自动生成一个默认的容器名称, 格式为 `<project>_<service>_<number>`

e.g. `test-website-articles-data-1 `



# `develop-watch`

[Use Compose Watch | Docker Docs](https://docs.docker.com/compose/how-tos/file-watch/)

在开发的过程中，当某些代码变动时候，我们往往需要 restart, rebuild container 使得代码生效，并且查看其效果，但是手动 docker compose down, 然后 docker compose up 实在是过于繁琐

这个时候我们可以使用 `develop: watch` 字段

## grammer

```yaml
develp:
  watch:
    - path: project-source-path/
      target: container-destination-path
      action: 
      ignore:
        - ignore-path/
```

### `watch`

- 除了 ignore 之外的所有的路径都是基于项目路径
- `.dockerignore` rules 会自动生效，除此之外 `.git` 文件夹会自动忽略

### `action`

- `sync` 将 project path 路径中变化复制到 container target 路径中
- `rebuild` 重建一个新的 images 并且替换掉原来的 container
- `sync+restart` 复制+重启

action 只能为这 3 个值，而不能随意拆分组合，例如不能使用单独的 `restart` 

### `path` and  `target`

- `path` 主机项目路径
- `target` container 路径

如果没有指定 target, 那么 `sync` 动作将默认把主机上的 `path` 路径同步到容器内的相同路径

### `ignore`

必须是一个 数组（列表），即使只有一个元素

```yaml
ignore:
  - logs/
```

wrong config

```yaml
ignore: logs/
```

`ignore` 参数的路径是相对于 `path` 参数的，例如我的项目中

```shell
website
├── Readme.md
├── articles-sync
│   ├── Dockerfile
│   ├── ...
│   ├── logs
├── compose.yml
└── web-app
    ├── Dockerfile
    ├── ...
    ├── ...
    └── templates
```

想要忽略 website/articles-sync/logs 目录下的所有文件，那么在 yaml 中就是

```yaml
services:
  ...

  articles-sync:
    ...
    develop:
      watch:
        - path: ./articles-sync
          ignore:
            - logs/**
          action: rebuild

volumes:
  articles_data:
```

其实关于 ignore realtive path 这个部分 docker compose watch 文档几乎没有解释，所以我创建了一个 PR 来说的更清楚的一些

PR: [Update file-watch.md: add ignore attribute path by hanjie-chen · Pull Request #21820 · docker/docs](https://github.com/docker/docs/pull/21820)

## `compose watch` VS. `bind mounts`

我们可以使用 bind mount 来将一个 主机目录共享到 container 目录中去

同样的，我们可以使用 `compose watch` 字段，检测源代码变化并且同步到 container 中去，而且可以使用 ignore 字段和 `.dockerignore` 控制监控的文件

但是这 2 者往往可以共存，比如说我需要实时查看 container 中一个目录所有的文件变化情况，还是需要 bind mount, 而不仅仅是 sync 源代码

## start watch

我们可以使用下面的命令启用 watch 模式

```shell
docker compose up --watch
```

或者使用

```shell
docker compose watch
```

不过这条命令只输出文件监视相关的信息，不包含容器运行时的详细日志

注意这些第一个命令的输出的本质其实还是 docker log, 所以当你意外的断开ssh 连接之后，可以使用下面的实时查看 docker log 的命令达到类似的效果

```shell
docker compose logs -f
```

# `ports`

docker documents: [Services top-level elements | Docker Docs](https://docs.docker.com/reference/compose-file/services/#ports)

我们可能想要将 contianer 中进程暴露给 host machine 但是，这个时候我们就需要使用到 `ports` 字段

grammer

```yaml
ports:
  - "8080:5000"  # "<host-machine port>":"<container port>"
```

# `image` & `build`

build: [Compose Build Specification | Docker Docs](https://docs.docker.com/reference/compose-file/build/)

## build

用于指定如何构建 image

```yaml
build:
  context: ./articles-sync
  dockerfile: Dockerfile
```

- `context`: 上下文的位置

- `dockerfile`: Dockerfile 的位置，如果默认的名称 `Dockerfile` 这个字段也可以忽略，可以将整体内容省略为

  ```yaml
  build: ./articles-sync
  ```

默认情况下，Docker Compose 会为构建的镜像自动命名，格式为 `<porject-name>_<service-name>`（项目名通常是当前目录名）

如果需要自定义镜像名称，可以结合 image 字段

```yaml
build: ./articles-sync
image: articles-sync1.0
```

> [!tip]
>
> 虽然字段顺序不影响功能，但为了代码的可读性和一致性，我们通常将 build 写在 image 之前：因为逻辑上，先构建（build）然后命名（image）更符合直觉。

## image

用于指定一个已经存在的镜像（可以是本地构建的，也可以是从远程镜像仓库拉取的）。Docker Compose 会直接使用这个镜像来启动容器，而不会去构建新的镜像。

```yaml
image: nginx
```

# `depends_on`

`depends_on` 用于定义服务之间的依赖关系，可以控制服务的启动顺序

如果服务 A 的 depends_on 中指定了服务 B，那么 Docker Compose 会确保服务 B 先启动，然后再启动服务 A。

```yaml
nginx:
  depends_on:
    - web
```

# `healthcheck`

用于定义容器健康检查的字段，它可以让 Docker 定期检查容器内部的运行状况，并根据检查结果决定该容器的健康状态。

- 自动检测应用是否正常运行
   例如，一个 Flask 应用可能已经崩溃，但进程仍在运行，默认情况下 Docker 不会发现这个问题，而 `healthcheck` 可以主动检查。
- **确保依赖的服务可用**
   比如，`web-app` 依赖 `articles-sync`，可以在 `web-app` 的 `depends_on` 配置中使用 `condition: service_healthy` 让其等待 `articles-sync` 进入健康状态后再启动。
- **在 Swarm 或 Compose 中实现更智能的容器管理**
   当服务不健康时，Swarm 可能会重新调度容器。

## config

`healthcheck` 主要由以下几个参数组成：

- **`test`**：指定执行的健康检查命令，通常是 shell 命令或 `CMD` 形式。
- **`interval`**：检查时间间隔（默认 `30s`）。
- **`timeout`**：健康检查命令的超时时间（默认 `30s`）。
- **`retries`**：失败多少次后认为不健康（默认 `3`）。
- **`start_period`**：容器启动后在这个时间段内不会触发健康检查，适用于启动较慢的应用。

## example

检查 Flask 应用是否正常运行

```yaml
services:
  web-app:
    image: my-flask-app
    ports:
      - "5000:5000"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
```

- `test`: 使用 `curl` 访问 `http://localhost:5000/health`，如果 HTTP 请求失败则视为不健康。
- `interval: 30s`: 每 30 秒检查一次。
- `timeout: 10s`: 超过 10 秒没有响应就算失败。
- `retries: 3`: 连续 3 次失败后，容器被标记为 `unhealthy`。
- `start_period: 10s`: 容器启动后，前 10 秒内不会进行健康检查，给 Flask 预留启动时间。

# `command`

compose.yml 文件的中 command 字段会覆盖 dockerfile 中的 CMD 启动命令，例如如果我们有 compose.yml如下

```yaml
services:
  web-app:
    ...
    command: ["flask", "run", "--host=0.0.0.0", "--debug"]
```

而在 web-app 的 Dockerfile 中这样子写道

```dockerfile
...

# 启动命令 (production)
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]
```

那么最红，实际上会使用 flask run 作为启动命令，这个特点可以用于开发环境的设定，比如说你可以做一个 compose.dev.yml 用于覆盖 dockerfile 中的命令

# 自定义字段

`x-` 开头的字段会被 Docker 视为“用户自定义扩展”。Compose 会完全忽略它们的内容，这使得它们成为存放 YAML 锚点的绝佳位置。

例如，我们可以利用 `x-` 和 `&` 锚点来将某个配置复用，例如复用 docker log 配置

```yaml
x-logging: &default-logging
  driver: json-file
  options:
    max-size: "1m"
    max-file: "5"

services:
  articles-sync:
    ...
    logging: *default-logging
  ...
...
```

