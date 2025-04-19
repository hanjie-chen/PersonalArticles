# `Docker compose up`

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

我的怀疑是 `docker compose up` 命令并不会主动去 build 这个 image, 除非是没有 image, 如果有 image 就会使用旧的，也不管有 Dockerfile 中 `COPY` 指令中的文件是否变化。但是 `docker compose build` 命令则是会去主动探测变化。

需要进一步查看这个 `docker compose up` 命令的源代码





## rebuild pointed service image

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
