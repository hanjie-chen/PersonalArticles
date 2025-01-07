# `compose.yml` 语法详解

## `services`

[Services top-level elements | Docker Docs](https://docs.docker.com/reference/compose-file/services/)

```
# 指定 contianer name
container_name: web-app
```

如果你没有指定 `container_name` Docker Compose 会自动生成一个默认的容器名称, 格式为 `<project>_<service>_<number>`

e.g. `test-website-articles-data-1 `

## `version`

根据最新的 docker compose 规范 [Version and name top-level elements | Docker Docs](https://docs.docker.com/reference/compose-file/version-and-name/)

Compose 不再使用此字段来选择验证模式， 而是默认使用最新的模式来解析文件，如果使用此字段会收到警告消息

## `develop`

compose.yml 中 `develop` 部分，是 Docker Compose 的开发模式特性 [Use Compose Watch | Docker Docs](https://docs.docker.com/compose/how-tos/file-watch/)

### watch 配置详解

```yaml
develop:
  watch:
    - path: ./web-app     # 本地源代码路径
      target: /app        # 容器内的目标路径
      action: sync+restart # 发生变化时的动作
```

#### action 类型：

1. `sync`: 同步文件变化，用于静态文件、数据文件
2. `sync+restart`: 同步文件并重启容器，用于需要重启才能生效的应用
3. `rebuild`: 重新构建容器，用于需要重新构建的情况

### 启动开发模式：

```bash
# 使用开发模式启动
docker compose watch
```

### igonre file

```yaml
develop:
  watch:
    - path: ./src
      target: /app/src
      ignore:
        - node_modules/
        - *.test.js
```

使用 ignore 排除不需要监控的文件

### 实战

在开发环境中，我们往往使用 bing mount 来将本地文件实时同步到 contianer 中去，所以我们在 develop 字段往往只需要 path 和 restart action 即可

e.g.

```yaml
services:
  web-app:
    build:
      context: ./web-app
      dockerfile: Dockerfile
    ports:
      - "5000:5000"
    volumes:
      - articles_data:/articles-data:ro
      - ./web-app:/app
    environment:
      - ARTICLES_DIRECTORY=/articles-data
      - FLASK_APP=app.py
    develop:
      watch:
        - path: ./web-app
          action: restart

  # ...
```

在这个配置中:

- `path` 指定了要监视的宿主机目录(`./web-app`)。
- `action` 指定了当该目录下的文件发生变化时要执行的操作(`restart`)。

这样, 就可以在宿主机上编辑 `./web-app` 中的代码, 这些改动会立即同步到容器内(通过卷挂载), 然后触发容器重启(通过 `develop.watch` 配置), 从而实现了开发环境下的热重载