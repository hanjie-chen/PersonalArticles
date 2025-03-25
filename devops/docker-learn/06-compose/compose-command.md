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



