# Bind Mount

**Bind Mount** 是 Docker 中的一种卷类型，它将主机文件系统中的一个目录或文件挂载到容器内的一个目录或文件。这意味着容器内指定路径下的内容与主机上的内容是 **同步的和共享的**。

**双向同步**：绑定挂载是 **双向的**，即主机和容器对该路径的更改都会相互反映。

- **主机到容器**：当您在主机上修改了挂载的目录或文件，这些更改会立即反映在容器内对应的路径上。
- **容器到主机**：同样地，当您的容器内的应用程序对挂载的目录或文件进行了更改，这些更改也会立即反映在主机上的对应路径上。

绑定挂载实际上是让主机和容器共享同一个文件系统位置。无论是主机还是容器，对该位置的操作都是对同一文件系统的操作。

e.g.

```yaml
services:
  web-app:
    ...
    volumes:
      - articles_data:/articles-data:ro
      # bind mount used to develop env, need to delete when product env
      - ./web-app:/app
    ...

  articles-sync:
    ...
    volumes:
      - articles_data:/articles-data:rw
      # bind mount conainer logs folder, used to devlop env
      - ./articles-sync/logs:/var/log/personal-website
    ...

volumes:
  articles_data:
```

在 `compose.yml` 中，绑定挂载的语法是 `host_path:container_path[:permission_options]`

`permission_option`

- `:ro` 容器内挂载的路径将被设置为只读。容器内的应用程序无法对其进行写操作。
- `:rw` 容器内挂载的路径可以读写。容器内的应用程序可以对其进行读写操作。`rw` 是默认选项，可以省略。

# bind mount VS. Docerfile `COPY` command

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
