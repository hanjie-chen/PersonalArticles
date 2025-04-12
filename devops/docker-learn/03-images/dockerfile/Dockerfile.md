# Dockerfile

Dockerfile 是一个文本文件，包含了一系列的指令和参数，Docker 使用它来自动构建镜像

可以将其理解为 "构建镜像的配方" 或 "说明书"，告诉 Docker 如何一步步构建你的应用程序镜像

标准的命名是 `Dockerfile`（首字母大写），这是 Docker 官方推荐的标准命名方式

# Dockerfile: start from an example

通过详细解释下面这个例子，初步的了解 Dockerfile

```Dockerfile
# 使用 '#' 添加注释

# 基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install -r requirements.txt

# 复制项目文件
COPY . .

# 暴露端口
EXPOSE 5000

# 启动命令
CMD ["python", "app.py"]
```

***

```Dockerfile
FROM python:3.9-slim  # 使用官方精简版 Python 镜像
```
指定基础镜像 `python:3.9-slim` 比完整版的 `python:3.9` 体积小，但包含运行 Python 所需的所有组件

```Dockerfile
WORKDIR /app  # 后续的指令都将在 /app 目录下执行
```
设置工作目录，如果目录不存在，Docker 会自动创建该目录，而且是 root 身份创建

```Dockerfile
COPY requirements.txt .  # 复制 requirements.txt 到当前工作目录
COPY . .               # 复制所有项目文件到当前工作目录
```
复制文件

- 第一个路径是主机上的源路径
- 第二个路径是容器中的目标路径

```Dockerfile
RUN pip install -r requirements.txt  # 安装项目依赖
```
在构建镜像时执行的命令

```Dockerfile
EXPOSE 5000  # 声明 contianer 中将使用的端口
```
仅仅作为声明，实际运行时还需要通过其他方式，比如说 docker -p 参数映射端口

```Dockerfile
CMD ["python", "app.py"]  # 容器启动时执行的命令
```
容器启动命令，使用数组形式可以更好地处理参数



# `WORKDIR` 指令

`WORKDIR` 用于为后续的 Dockerfile 指令（如 RUN、CMD、ENTRYPOINT、COPY 和 ADD）设置工作目录，相当于 `cd` 命令的效果，容器启动时的默认目录

如果目标目录不存在，会自动创建该目录，而且使用 `root` 用户创建这个目录，无论 `USER` 指令是否已经切换到 non-root user

## best practice

而依据最小权限规则，我们往往不能让 root user 去运行这个 container，所以最好不要依靠 `WORKDIR` 来创建目录，而是提前创建好目录并且给予权限或者修改目录所有者 e.g.

```dockerfile
...

# define the args for the user/group IDs, can pass these in compose.yml or docker run command
ARG USER_ID=1000
ARG GROUP_ID=1000

# create a group(appgroup) and user(appuser) with args
RUN addgroup -g ${GROUP_ID} -S appgroup && \
    adduser -u ${USER_ID} -S appuser -G appgroup

# Set ownership for the data directory mount point as well
RUN mkdir -p /articles-data && chown appuser:appgroup /articles-data
WORKDIR /articles-data

...
```





# `COPY` 指令

```dockerfile
COPY [--param] <host source file/dir> <container destination file/dir>
```

### example 1

将 host 文件复制到 contianer 中

```dockerfile
COPY logrotate.conf /etc/logrotate.d/personal-website
```

它会将 `logrotate.conf` 文件复制到 `/etc/logrotate.d/` 目录下，并重命名为 `personal-website`

### example 2

```dockerfile
COPY --chown=<user>:<group> <src> <dest>
```

例如，将多个 host 文件复制到一个 container 目录中，并且修改这些文件的拥有者

```dockerfile
COPY --chown=appuser:appgroup update-articles.sh init.sh /usr/local/bin/
```

将2个shell脚本复制到 contianer `/usr/local/bin` 目录下，同时把这 2 个文件所有者设置为 appuser:appgroup

> [!note]
>
> 这仅仅改变这里2个存在于 contianer 目录中的文件的所有者，不会改变 container 目录的所有者（目录所有者还是原来的 root）
>
> 因为 COPY 指令无法被 USER 指令影响，所以如果不指定的话，默认这些文件的拥有者是 root



# `EXPOSE` 指令

`EXPOSE` 指令实际上只是一个文档性质的声明，告诉其他人这个容器使用什么端口，实际并不会开放任何端口

要使端口实际可访问，需要配合 `docker run -p` 或者在 `compose.yml` 中指定 `ports`



# `RUN` 指令

用于在构建镜像时执行命令，并将执行结果保存到镜像的下一层。例如，可以用 `RUN` 安装软件包、复制文件、修改权限等。

## best practice

run 指令最佳实践：用于实现分层构建，充分利用 cache 



# `ENTRYPOINT` 指令

ENTRYPOINT 指令用于设置容器启动时要执行的主要命令，当容器启动时，ENTRYPOINT 指定的命令会自动执行，这个命令将作为容器的主进程（PID 1）

## grammar

ENTRYPOINT 指令有两种格式：

1. Shell 格式：
```dockerfile
ENTRYPOINT command param1 param2
```

2. Exec 格式（推荐）：
```dockerfile
ENTRYPOINT ["executable", "param1", "param2"]
```

## ENTRYPOINT vs CMD

ENTRYPOINT 的优先级高于 CMD
- 如果同时定义了 ENTRYPOINT 和 CMD，CMD 的内容会作为 ENTRYPOINT 的参数
- 如果只定义了 ENTRYPOINT，则容器只执行 ENTRYPOINT 指定的命令

### example

```dockerfile
FROM ubuntu
ENTRYPOINT ["echo", "Hello"]
CMD ["World"]
```
默认输出：`Hello World`

> [!note]
>
> 一个 Dockerfile 中只有最后一个 ENTRYPOINT 生效



# `ARG` 指令

`ARG` 指令在 `Dockerfile` 中用于定义构建时变量，这些变量的值可以在构建镜像的时候通过 `docker run` 指令或者 compose.yml 中使用 `build.args` 传递



# `USER` 指令

### grammer

```dockerfile
USER <username>[:<usergroup>]
# 或
USER <UID>[:<GID>]
```

### 它指定：

- 从这一行之后，Dockerfile 中：
  - 构建阶段的某些指令（如 `RUN`）将以该用户身份执行
  - 所有运行阶段的指令（如 `CMD`、`ENTRYPOINT`）默认以该用户身份执行
- 设置容器运行时的默认用户（镜像启动时默认以谁来运行）

### 不受 `USER` 影响的指令：

- `COPY`
- `ADD`

它们始终由构建系统（通常是 root）来执行

### 类比理解

构建镜像就像是在盖房子，Docker 是施工队

- `RUN` 是你在房子里干活，比如装家具，谁来干？取决于你让谁进来干（`USER`）
- `COPY` / `ADD` 是送材料（文件）进工地，这一定是快递员（系统 root）送的
- `CMD` / `ENTRYPOINT` 是住进去以后谁来使用房子——默认就是 `USER` 指定的那个人



# 构建阶段指令和运行阶段指令

Dockerfile 中不同的指令生效的实践也不同，比如说

构建时执行的指令（`docker build`）：

- `FROM`

- `RUN`

- `COPY`

- `ADD`

- `WORKDIR`

  …

运行时执行的指令（`docker run`）：

- `ENTRYPOINT`
- `CMD`

