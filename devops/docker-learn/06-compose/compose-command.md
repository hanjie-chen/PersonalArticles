# docker compose command



# `docker compose up`



## point yml file

命令

```shell
docker compose -f compose.yml up -d
```

#### -f compose.yml (File / 指定文件)

- 含义： 告诉 Docker Compose：“请使用 compose.yml 这个文件作为配置文件”。
- 为什么有时候看着多余？ 默认情况下，Docker Compose 会自动寻找名为 compose.yml 或 docker-compose.yml 的文件。所以如果你没改文件名，不写 -f compose.yml 效果也是一样的。
- 什么时候必用？ 当你的配置文件名字不叫标准名字时。比如：docker compose -f production.yml up（使用生产环境配置启动）。

#### -d (Detached / 后台模式)

- 含义： Detached mode，即“分离模式”或“后台运行”。
- 对比：不加 -d (你平时用的)： 启动后，终端会被占用，屏幕上会疯狂滚动服务的日志。如果你按 Ctrl + C，容器通常会停止。加上 -d： 启动后，Docker 会在后台默默运行容器。终端控制权会立即还给你，你可以继续输入其他命令。
- 场景： 只要你想让服务在服务器上一直跑，通常都会加 -d。

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