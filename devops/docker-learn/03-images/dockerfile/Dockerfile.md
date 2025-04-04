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

## **FROM**：指定基础镜像

```Dockerfile
FROM python:3.9-slim  # 使用官方精简版 Python 镜像
```
- `python:3.9-slim` 比完整版的 `python:3.9` 体积小，但包含运行 Python 所需的所有组件
- 也可以使用 `python:3.9-alpine` 更小，但可能会有一些兼容性问题

## WORKDIR：设置工作目录

```Dockerfile
WORKDIR /app  # 后续的指令都将在 /app 目录下执行
```
如果目录不存在，Docker 会自动创建该目录，而且是 root

## **COPY**：复制文件

```Dockerfile
COPY requirements.txt .  # 复制 requirements.txt 到当前工作目录
COPY . .               # 复制所有项目文件到当前工作目录
```
- 第一个路径是主机上的源路径
- 第二个路径是容器中的目标路径

## **RUN**：执行命令

```Dockerfile
RUN pip install -r requirements.txt  # 安装项目依赖
```
- 在构建镜像时执行的命令

## **EXPOSE**：声明端口

```Dockerfile
EXPOSE 5000  # 声明 contianer 中将使用的端口
```
仅仅作为声明，实际运行时还需要通过 -p 参数映射端口

## **CMD**：容器启动命令

```Dockerfile
CMD ["python", "app.py"]  # 容器启动时执行的命令
```
使用数组形式可以更好地处理参数

让我详细解释一下 `WORKDIR` 的作用和使用场景：

# `WORKDIR` 指令

`WORKDIR` 用于为后续的 Dockerfile 指令（如 RUN、CMD、ENTRYPOINT、COPY 和 ADD）设置工作目录，相当于 `cd` 命令的效果，容器启动时的默认目录

如果目标目录不存在，会自动创建该目录，而且使用 `root` 用户创建这个目录，无论 `USER` 指令是否已经切换到 non-root user

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

将 host 文件复制到 contianer 中 e.g.

```dockerfile
COPY logrotate.conf /etc/logrotate.d/personal-website
```

它会将 `logrotate.conf` 文件复制到 `/etc/logrotate.d/` 目录下，并重命名为 `personal-website`



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



# build 指令和运行时指令

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

