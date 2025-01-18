# Bind Mount

**Bind Mount** 是 Docker 中的一种卷类型，它将主机文件系统中的一个目录或文件挂载到容器内的一个目录或文件。这意味着容器内指定路径下的内容与主机上的内容是 **同步的和共享的**。

双向同步：绑定挂载是 双向的，即主机和容器对该路径的更改都会相互反映。

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

# bind mount 生效时机

首先我们看这个 compose.yml

```yaml
services:
  ...
    volumes:
      - ./web-app:/app
    ...
  ...
```

然后看这个 Dockerfile

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

我们在 dockerfile 中将目录中的 `requiremetn.txt` 复制到 work directory 下，用于安装相关的依赖，但是实际上我们又会在 `compose.yml` 中使用 bind mount 将目录下的文件 mount 到 work directory 下

这个时候就会有个问题，dockerfile 中的 COPY 指令是否必要存在呢？

这个问题的本质其实是关于 bind mount 和 COPY 指令那个先执行的问题

- Dockerfile 中的 `COPY` 和 `RUN` 指令会在镜像构建时执行, 将 requirements.txt 复制到镜像中并安装依赖。
- 当容器启动时, compose.yml 中定义的卷挂载(`./web-app:/app`)会将宿主机的 `./web-app` 目录挂载到容器的 `/app` 目录。
- 卷挂载会覆盖镜像中的 `/app` 目录,

也就是说 COPY 指令会先执行，所以 `COPY requirements.txt` 和 `RUN pip install` 仍然是必要的, 因为它们保证了依赖的正确安装。即使后续的卷挂载覆盖了 `/app` 目录, 也不会影响容器的运行。

# bind mount 本质

当使用bind mount将主机上的一个路径挂载到容器中的一个路径时,容器中该路径原有的文件会被隐藏 ,但并不会被删除或覆盖。具体而言:

假设容器中的路径 `/container/path` 下原本有如下文件:

```javascript
/container/path/
  |- file1
  |- file2
```

如果把主机路径 `/host/path` 挂载到容器的 `/container/path`,而 `/host/path` 下有如下文件:

```javascript
/host/path/
  |- file3 
  |- file4
```

那么容器中 `/container/path` 下可见的文件将变为:

```javascript
/container/path/  
  |- file3
  |- file4  
```

此时容器中原有的 `file1` 和 `file2` 已经被隐藏,无法访问,但它们并没有被删除,数据还在容器内部。

如果卸载掉这个bind mount, 容器内 `/container/path` 下的内容会恢复原样,又可以看到原来的 `file1` 和 `file2` 了。所以使用bind mount不会造成容器内数据丢失,只是暂时隐藏了原有文件,使其不可访问而已。

在挂载状态下,如果容器中的程序在 `/container/path` 下创建了一个新文件 `file5`,那么可以确定的是:

1. 在主机的 `/host/path` 下可以看到 `file5`,因为此时容器的 `/container/path` 实际上就是映射到主机的 `/host/path`。
2. 在容器内的 `/container/path` 下也可以看到 `file5`,因为容器进程是在这个路径下创建的文件。

但是,一旦卸载掉这个bind mount,情况会发生变化:

1. 主机上的 `/host/path` 中会保留 `file3`, `file4`, `file5`,因为这个目录一直都在主机上,并不受容器生命周期影响。
2. 但容器内的 `/container/path` 将恢复到挂载前的状态,只包含原有的 `file1` 和 `file2`。在挂载状态下新创建的 `file5` 并不会出现在容器的这个路径中,因为它实际上是直接写在主机上的。

所以,bind mount 的本质是将容器内的路径临时"替换"为主机上的另一个路径。在挂载状态下,容器内外是共享这个路径的。但一旦卸载,容器内原有的数据就会恢复可见,而在挂载状态下新写入的数据则仅保留在主机上,不会出现在容器内部。

所以在使用 bind mount 时要注意数据持久化的问题,特别是在多个容器共享同一个主机路径的情况下,需要小心处理可能出现的数据不一致问题。
