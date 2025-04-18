# Docker logs

`docker logs` 默认是可以查看 `docker-compose up` 输出的内容的，只要你知道相关容器的名字或 ID。



### 方法一：查看容器名称

如果你是通过 `docker-compose up -d` 启动的服务，可以通过以下命令找到容器名称：

```bash
docker ps
```

会显示类似下面的内容：

```
CONTAINER ID   IMAGE             COMMAND                  NAMES
a1b2c3d4e5f6   my_web_app        "python app.py"          myproject_web_1
b2c3d4e5f6g7   my_articles_sync  "/start.sh"              myproject_articles-sync_1
```

然后使用容器名称查看日志：

```bash
docker logs myproject_web_1
```



### 方法二：查看所有服务日志（推荐）

如果你想查看所有服务的日志输出（包括 web、articles-sync 等），可以直接用：

```bash
docker compose logs
```

想看具体服务的日志，例如 `web`：

```bash
docker compose logs web
```

默认会显示所有历史日志，你也可以加上 `-f` 实时查看日志（像 `tail -f` 那样）：

```bash
docker compose logs -f
```

------

### 补充说明

- 如果你之前是用 `docker-compose up`（**前台运行**）而不是 `-d`（后台运行），那么输出已经打印在你当时的终端中了，除非你把它记录了下来（比如用 `tee` 命令）。
- Docker 日志默认存储在 `/var/lib/docker/containers/<container-id>/` 中。

但是如果使用了

```bash
docker compose down
```

那么你大概率看不到之前的日志了，因为这个命令会：

1. 停止容器
2. 删除容器
3. 断开并删除网络
4. （可选）删除 volumes（除非加了 `--volumes`）

### 为什么日志会丢？

Docker 的日志是保存在容器内部对应的日志文件中的（例如 `/var/lib/docker/containers/<container-id>/`），而不是一个独立于容器的永久日志系统。

所以，一旦你 `docker compose down` 删除了容器，对应的日志文件也就一并被删除了。