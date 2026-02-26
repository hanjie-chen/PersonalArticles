# docker compose command



# `docker compose up`

```shell
docker compose -f <yaml-filename> up -d
```

`docker compose`

- 下载镜像（如果本地没有）。
- 创建容器。
- 启动服务。
- 更新配置：如果你修改了配置文件，它会检测到差异并重新创建受影响的容器。

`-f <yaml-filename>` 

- 告诉 Docker Compose：请使用 `<yaml-filename>` 这个文件作为配置文件。
- 不写 `-f compose.yml` 那么Docker Compose 会自动寻找名为 compose.yml 或 docker-compose.yml 的文件。
- 当你的 yaml file 不叫标准名字时。比如：docker compose -f production.yml up（使用生产环境配置启动）。

`-d`

- Detached mode，即“分离模式”或“后台运行”。
- 不加 -d 启动后，终端会被占用，屏幕上会疯狂滚动服务的日志。如果你按 Ctrl + C，容器通常会停止。加上 -d： 启动后，Docker 会在后台默默运行容器。终端控制权会立即还给你，你可以继续输入其他命令。
- 只要你想让服务在服务器上一直跑，通常都会加 -d。

### multi-file

```
docker compose -f compose.yml -f compose.dev.yml up
```

这里出现了两次 -f，这是 Docker Compose 非常强大的配置合并（Merge/Override）功能。

逻辑：像“图层”一样叠加

1. 先读取 compose.yml（基础配置）。
2. 再读取 compose.dev.yml（开发环境配置）。
3. 将两者合并，且后者的设置会覆盖前者。

## rebuild image

当我们更新了某些构建 image 的文件的时候，比如说 requirements.txt, source code part，使用 `docker compose up` 结果发现这个修改并没有生效，反而是使用了旧的 image 去运行 container

这个时候，大概率是 `docker compose up` 使用了已经构建的 image 文件，为了解决这个问题，我们需要使用下面的命令强制重新构建一下 image

```shell
docker compose build --no-cache
```

或者

```shell
docker compose up --build
```

这样会在 `up` 的同时强制重新构建镜像，然后再启动容器

`docker compose up` 命令并不会主动去 build image, 除非是没有 image, 如果有 image 就会使用旧的，也不管有 Dockerfile 中 `COPY` 指令中的文件是否变化。

但是 `docker compose build` 命令则是会去主动探测变化，如果有变化（哈希值对比），那么就会重新构建

### rebuild pointed service image

如果我们遇到这样子一个问题：

仅仅改动了某个 service 的 dockerfile，而且仅仅需要重建这个 service 的 image, 我们应该怎么办呢？

也就是如何只重建这个镜像，而不是 `docker compose build --no-cache` 重建所有？

我们可以使用

```bash
docker compose build --no-cache <服务名>
```

比如你的 `docker-compose.yml` 文件里有如下服务：

```yaml
services:
  articles-sync:
    build:
      context: .
      dockerfile: Dockerfile
  web-app:
    image: my-web-app
    ...
```

那么你只需要重建 `articles-sync`：

```bash
docker compose build --no-cache articles-sync
```

这个命令只会对指定服务重建镜像，并不会影响其他服务。

## clean redundant container

在 docker 实践过程中，当我们更新了某些部分（yaml, code etc）的时候，为了没有 downtime 的部署，常用下面这个命令

```
docker compose up -d --remove-orphans
```

它的作用是：根据配置文件启动所有容器，并在后台运行，同时清理掉那些不再需要的“孤儿”容器。

`--remove-orphans`

- 清理“孤儿”容器：所谓的“孤儿”容器，是指那些已经在配置文件中被删除、但仍然在 Docker 中运行的容器。
- 场景举例：假设你以前在 `yml` 里写了 `mysql` 和 `web` 两个服务。后来你把 `mysql` 删掉了，只剩下 `web`。如果你只运行 `docker compose up`，那个旧的 `mysql` 容器可能还会残留在后台占用资源。加上这个参数，Docker 会自动发现它不再属于当前项目并将其删除。