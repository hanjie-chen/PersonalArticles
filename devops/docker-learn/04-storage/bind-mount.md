# Bind Mount

Bind Mount 是 Docker 中的一种卷类型，它将 host machine 中的一个目录或文件挂载到 container 内的一个目录或文件。这意味着container 内指定路径下的内容与 host 的内容是同步的和共享的。

绑定挂载实际上是让主机和容器共享同一个文件系统位置。无论是主机还是容器，对该位置的操作都是对同一文件系统的操作。

这些文件因为写入了 host filesystem, 所以就算 contianer 消失，这些文件也不会消失

e.g.

```yaml
services:
  web-app:
    ...
    volumes:
      # bind mount used to develop env, need to delete when product env
      - ./web-app:/app
    ...
  ...
```

在 `compose.yml` 中，绑定挂载的语法是 `host_path:container_path[:permission_options]`

`permission_option`

- `:ro` 容器内挂载的路径将被设置为只读。容器内的应用程序无法对其进行写操作。
- `:rw` 容器内挂载的路径可以读写。容器内的应用程序可以对其进行读写操作。`rw` 是默认选项，可以省略。



# files permission in bind mount

我们有时候会遇到这样子的问题，那就是当我们使用 bind mount 将 host machine 的一个空目录挂载到 container 中，然后由这个 container 来创建和修改这个目录下的文件。

当我们想要在 host machine 上删除这个文件的时候，却发现会报错：

```shell
$ rm 'articles-sync.log 2>&1'
rm: remove write-protected regular file 'articles-sync.log 2>&1'? y
rm: cannot remove 'articles-sync.log 2>&1': Permission denied
```

这是因为对于此情况下 container 内的进程（无论是 root 还是普通用户）在这个目录下创建文件时，文件的拥有者和权限由创建文件的进程决定。

而当这个进程是以 root user 运行的时候，容器内文件的所有权就是 root, host machine 上面则会同样显示为所有权是 root

所以 host machine 上面的 non-root user 无法删除这个文件

> [!note]
>
> Docker 默认情况下会将容器内用户的 UID (User ID) 和 GID (Group ID) 直接映射到宿主机上相同的 UID 和 GID。

我们当然可以简单的使用 `sudo rm` 命令来删除这个文件，但是作为 best practice 我们最好使用 non-root user 去运行 container process: [Dockerfile best practice](./03-images/dockerfile/best-practice.md)

并且这个用户的 UID/GID 最好能匹配你宿主机上的用户的 UID/GID。

## another situation: 

如果 host machine 上面的目录不为空，里面存在文件，并且 container 中的进程需要修改这些文件。

如果这些文件是由 host machine 上的 root 用户创建的，而容器内的 non-root user（UID:1000）尝试写入这些文件，会因为权限不足而失败。

如果是 host machine non-root user 创建（比如说 UID:1000），那么对于权限 644（rw-r--r--），container 中的 UID:1000 的 non-root user 有读写权限，因此可以修改。

## another situation: no such a dir

当我们再 `compose.yml` 中配置完 bind mount 将一个 host machine 的路径映射到 container 中，如果 host machine 没有这个路径，那么会发生什么呢？

答：Docker 会自动在宿主机上创建该路径（包括必要的父目录），而且是由运行 Docker 守护进程（Docker Daemon）的用户创建的，通常是 root 用户

> [!note]
>
> Docker 守护进程（dockerd）通常以 root 用户身份运行（除非你特意配置了非 root 模式，如 rootless Docker）



# bind mount 生效时机

首先我们看这个 compose.yml

```yaml
services:
  web-app:
    ...
    volumes:
      # bind mount used to develop env, need to delete when product env
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
- 卷挂载会覆盖镜像中的 `/app` 目录

也就是说 COPY 指令会先执行，将 `requirement.txt` 复制到 images 中去，然后当这个 image 运行起来，变成 container 的时候，bind mount 才会生效，将 host machine 中的 `./web-app` 目录覆盖 container 中的 `/app` 目录

# bind mount 本质

Bind mount 会将宿主机上的“一切”（包括目录、文件、权限等）覆盖或带入到容器中

这意味着将宿主机指定的路径（包括其文件、子目录及其权限）完全“映射”到容器内的目标路径，覆盖容器内该路径的原有内容。容器内的进程访问该路径时，实际上操作的是宿主机的文件系统，权限检查也基于宿主机的文件权限。

> [!tip]
>
> 这意味着如果 container 中原有的 dir1(owned by root user)，然后 bind mount 了 host machine 上面的一个 dir2(owned by non-root user, UID:1000) 那么如果 container 中同样也是使用 non-root user(UID:1000) 去运行的，就可以成功访问到这个 dir
>
> 但是实际上如果解除了这个 bind mount, 反而就会出现权限问题 

## what about the source file in container?

那么原来在 container 中的这个路径怎么办呢？

它们（容器中该路径原有的文件）会被隐藏 ,但并不会被删除或修改。

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
