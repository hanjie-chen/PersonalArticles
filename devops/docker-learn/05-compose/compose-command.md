当我们更新了某些构建 image 的文件的时候，比如说 requirements.txt，使用 `docker compose up` 结果发现这个修改并没有生效到image 中，反而是使用了旧的 image 去运行 container

这个时候，大概率是 `docker compose up` 使用了已经构建的缓存文件，而不是重新构建

为了解决这个问题，我们需要使用下面的命令强制重新构建一下 image

```shell
$ docker compose build --no-cache
```

或者

```shell
docker compose up --build
```

这样会在 `up` 的同时强制重新构建镜像，然后再启动容器



但是这里有一个矛盾的地方，在这篇文档中 [Compose Build Specification | Docker Docs](https://docs.docker.com/reference/compose-file/build/#using-build-and-image) 提到了这样子一句话

> If `pull_policy` is missing from the service definition, Compose attempts to pull the image first and then builds from source if the image isn't found in the registry or platform cache.

似乎说明了如果没有 `pull_policy` 的话就会使用存在的 image

但是在这篇关于 cache 的文档中 [Cache | Docker Docs](https://docs.docker.com/build/cache/) 提到

> ```dockerfile
> # syntax=docker/dockerfile:1
> FROM ubuntu:latest
> 
> RUN apt-get update && apt-get install -y build-essentials
> COPY main.c Makefile /src/
> WORKDIR /src/
> RUN make build
> ```
>
> . . .
>
> Whenever a layer changes, that layer will need to be re-built. For example, suppose you make a change to your program in the `main.c` file. After this change, the `COPY` command will have to run again in order for those changes to appear in the image. In other words, Docker will invalidate the cache for this layer.

有提到了，如果 `COPY` 指令中的文件变化了就会重新构建

我的怀疑是 `docker compose up` 命令并不会主动去 build 这个 image, 除非是没有 image, 如果有 image 就会使用旧的，也不管有 Dockerfile 中 `COPY` 指令中的文件是否变化。但是 `docker compose build` 命令则是会管理这些

不知道我的理解是否正确