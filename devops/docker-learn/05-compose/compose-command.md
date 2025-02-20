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