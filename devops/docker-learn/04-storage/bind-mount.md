# Bind Mount

绑定挂载（Bind Mount）可以直接将主机的文件或目录挂载到容器中，可以在任何位置存储，适合开发环境

e.g.

```yaml
services:
  wordpress:
    volumes:
      - ./themes:/var/www/html/wp-content/themes  # 绑定挂载
```

语法格式为 `[host-path]:[container-path]`

`./themes`: 表示主机（你的电脑）上的路径

- `.` 表示当前目录（docker-compose.yml 所在的目录）
- `./themes` 就是当前目录下的 themes 文件夹

`/var/www/html/wp-content/themes`: 容器内的路径

# bind mount VS Docerfile `COPY` command

```yaml
services:
  web-app:
    build:
      context: ./web-app
      dockerfile: Dockerfile
    ports:
      - "5000:5000"
    volumes:
      - ./web-app:/app
    ...
  ...
...
```

```dockerfile
...

# set web app directory
WORKDIR /app

# 复制requirements.txt
COPY requirements.txt .

# 安装依赖
RUN pip install -r requirements.txt

...
```

有的时候我们会遇到这样子的情况，我们在 dockerfile 中将目录中的 `requiremetn.txt` 复制到 work directory 下，用于安装相关的依赖，但是实际上我们又会在 `compose.yml` 中使用 bind mount 将目录下的文件 mount 到 work directory 下

这个时候就会有个问题，dockerfile 中的 COPY 指令是否必要呢？

这其实涉及到 bind mount 和 COPY 指令那个先执行的问题

在这种情况下:

- Dockerfile 中的 `COPY` 和 `RUN` 指令会在镜像构建时执行, 将 requirements.txt 复制到镜像中并安装依赖。
- 当容器启动时, compose.yml 中定义的卷挂载(`./web-app:/app`)会将宿主机的 `./web-app` 目录挂载到容器的 `/app` 目录。
- 卷挂载会覆盖镜像中的 `/app` 目录, 但不会影响已经安装的依赖, 因为依赖是安装在 Python 的 site-packages 目录下, 而不是 `/app` 目录。

也就是说 COPY 指令会先执行，所以 `COPY requirements.txt` 和 `RUN pip install` 仍然是必要的, 因为它们保证了依赖的正确安装。即使后续的卷挂载覆盖了 `/app` 目录, 也不会影响容器的运行。
