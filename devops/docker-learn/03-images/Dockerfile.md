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

## **WORKDIR**：设置工作目录

```Dockerfile
WORKDIR /app  # 后续的指令都将在 /app 目录下执行
```
如果目录不存在，Docker 会自动创建

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

`WORKDIR` 是设置工作目录的指令，为后续的 Dockerfile 指令（如 RUN、CMD、ENTRYPOINT、COPY 和 ADD）设置工作目录，如果目录不存在，Docker 会自动创建，相当于 `cd` 命令的效果，容器启动时的默认工作目录

for instance

```dockerfile
# 不使用 WORKDIR
FROM alpine:3.18
COPY script.sh /app/script.sh
RUN cd /app && ./script.sh

# 使用 WORKDIR
FROM alpine:3.18
WORKDIR /app
COPY script.sh .
RUN ./script.sh
```

建议使用 WORKDIR 的情况

1. **项目结构清晰**
```dockerfile
FROM alpine:3.18

# 设置工作目录，使结构更清晰
WORKDIR /app

# 所有相关文件都在 /app 下
COPY scripts/ ./scripts/
COPY data/ ./data/
```

2. **需要频繁操作某个目录**
```dockerfile
WORKDIR /articles-data
# 后续的操作都相对于 /articles-data
COPY ./content .
RUN git init && \
    git add . && \
    git commit -m "Initial commit"
```

3. **多阶段构建**
```dockerfile
# 构建阶段
FROM node:alpine AS builder
WORKDIR /build
COPY package.json .
RUN npm install
COPY . .
RUN npm run build

# 最终阶段
FROM alpine:3.18
WORKDIR /app
COPY --from=builder /build/dist ./dist
```



# `COPY` 指令

e.g.

```dockerfile
COPY logrotate.conf /etc/logrotate.d/personal-website
```

`/etc/logrotate.d/personal-website` 这里的 `personal-website` 是**目标文件名**，不是目录

- 这条命令的意思是：将 `logrotate.conf` 文件复制到 `/etc/logrotate.d/` 目录下，并重命名为 `personal-website`
- 这是 logrotate 的标准配置方式，每个应用程序的轮转配置都是 `/etc/logrotate.d/` 目录下的一个文件

# `EXPOSE` 指令

`EXPOSE` 指令实际上只是一个文档性质的声明，告诉其他人这个容器使用什么端口，实际并不会开放任何端口

要使端口实际可访问，需要配合 `docker run -p` 或者在 `compose.yml` 中指定 `ports`

e.g.

```Dockerfile
# Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

`docker run -p`

```bash
# 不映射端口
docker run my-app
# 结果：容器内的应用运行在5000端口，但从主机无法访问

# 明确映射端口（常用）
docker run -p 8080:5000 my-app
# 结果：可以通过主机的8080端口访问容器的5000端口
```

# `RUN` 指令

## 下载额外的命令

例如如果我想要让images中自带git, 对于python-slim，需要手动下载

``` dockerfile
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

###  `apt-get update`
更新包索引文件

- 这个命令会从软件源服务器下载最新的包信息
- 如果不执行这步，系统可能会使用过时的包索引
- 可能导致软件包找不到或安装旧版本



### `apt-get install -y git`
安装 git 包

`-y` 标志表示自动回答 "yes" 到所有提示，在 Dockerfile 中这很重要，因为构建过程是自动的，不能交互式回答问题

如果想要安装其他的包，比如cron, 可以再 git 之后添加，例如 `apt-get install -y git cron`

### `apt-get clean`
清理 apt 缓存

- 删除 `/var/cache/apt/archives/` 下载的 .deb 文件
- 这些是安装包的缓存文件，安装完成后就不再需要了
- 减小最终镜像的大小

就像安装完软件后删除安装包

### `rm -rf /var/lib/apt/lists/*`
删除 apt 包列表

- 删除 `apt-get update` 下载的包索引文件
- 这些文件在安装完成后不再需要
- 进一步减小镜像大小

- **类比**：就像删除已经用不到的商品目录

### 为什么要组合使用？

1. **Docker 最佳实践**：
   - Docker 镜像是分层的
   - 每个 RUN 命令创建一个新层
   - 把相关命令组合成一个 RUN 可以减少层数
   ``` dockerfile
   # 不好的做法：每个命令一个层
   RUN apt-get update
   RUN apt-get install -y git
   RUN apt-get clean
   RUN rm -rf /var/lib/apt/lists/*
   ```

2. **镜像大小优化**：
   ``` bash
   # 示例：查看这些文件占用的空间
   du -sh /var/cache/apt/archives/
   du -sh /var/lib/apt/lists/
   ```
   - 清理这些文件可以显著减小镜像大小
   - 小的镜像更容易分发和部署

3. **缓存一致性**：
   - 如果 `update` 和 `install` 在不同的 RUN 命令中
   - Docker 缓存机制可能导致使用旧的包索引
   ``` dockerfile
   # 潜在问题的例子
   RUN apt-get update  # 这层可能被缓存
   RUN apt-get install -y git  # 使用旧的包索引
   ```

4. **示例对比**：
   ``` bash
   # 不清理的镜像大小
   docker build -t test-no-clean .
   docker images test-no-clean
   
   # 清理后的镜像大小
   docker build -t test-with-clean .
   docker images test-with-clean
   ```
   清理后的镜像通常会小很多

### 完整的最佳实践
``` dockerfile
RUN apt-get update && \
    DEBIAN_FRONTEND = noninteractive apt-get install -y \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
```
- 使用 `&&` 确保所有命令成功执行
- `DEBIAN_FRONTEND=noninteractive` 防止某些包的安装脚本请求用户输入
- 如果要安装多个包，可以在 git 后面继续添加



# `ENTRYPOINT` 指令

ENTRYPOINT 指令用于设置容器启动时要执行的主要命令，它有两个主要作用：

1. **设置容器的默认执行命令**
   - 当容器启动时，ENTRYPOINT 指定的命令会自动执行
   - 这个命令将作为容器的主进程（PID 1）

2. **使容器像可执行程序一样使用**
   - 让容器表现得像一个可执行程序，更符合容器"一个进程"的理念
   - 可以接收命令行参数

### 语法格式

ENTRYPOINT 有两种格式：

1. Shell 格式：
```dockerfile
ENTRYPOINT command param1 param2
```

2. Exec 格式（推荐）：
```dockerfile
ENTRYPOINT ["executable", "param1", "param2"]
```

### ENTRYPOINT vs CMD

1. **ENTRYPOINT 的优先级高于 CMD**
   - 如果同时定义了 ENTRYPOINT 和 CMD，CMD 的内容会作为 ENTRYPOINT 的参数
   - 如果只定义了 ENTRYPOINT，则容器只执行 ENTRYPOINT 指定的命令

2. **命令行参数的处理**
   - docker run 命令行中的参数会覆盖 CMD 指定的内容
   - 但不会覆盖 ENTRYPOINT 指定的命令

### 实际示例

1. 基础示例：
```dockerfile
FROM ubuntu
ENTRYPOINT ["echo", "Hello"]
CMD ["World"]
```
- 默认输出：`Hello World`
- 运行 `docker run image_name John`：输出 `Hello John`

2. 创建可执行工具：
```dockerfile
FROM ubuntu
ENTRYPOINT ["nginx", "-g", "daemon off;"]
```
- 容器将始终以 nginx 服务器启动
- 更符合"容器即服务"的理念

### 最佳实践

1. **优先使用 Exec 格式**
   - 避免 shell 格式可能带来的问题
   - 更直接地执行命令，不通过 shell 解释器

2. **合理搭配 CMD**
   - ENTRYPOINT 定义固定的执行命令
   - CMD 提供可变的默认参数

3. **考虑可覆盖性**
   - 如果需要灵活性，可以使用 CMD
   - 如果要强制执行特定命令，使用 ENTRYPOINT

### 注意事项

1. 一个 Dockerfile 中只有最后一个 ENTRYPOINT 生效
2. 可以在运行容器时使用 `--entrypoint` 覆盖 ENTRYPOINT 设置
3. 使用 ENTRYPOINT 时要考虑信号处理和进程管理

通过合理使用 ENTRYPOINT，可以使容器更加规范和专注于特定用途，提高容器的可用性和可维护性。

# build 指令和运行时指令

### Dockerfile 指令执行时机

1. **构建时执行的指令**（`docker build`）：
   - `FROM`
   - `RUN`
   - `COPY`
   - `ADD`
   - `WORKDIR`
   等...

2. **运行时执行的指令**（`docker run`）：
   - `ENTRYPOINT`
   - `CMD`

### 为什么这个设计很重要

这个设计允许我们：

1. **正确处理 volume 挂载**：
   ```dockerfile
   ENTRYPOINT [ "/usr/local/bin/init.sh" ]  # 容器启动时执行
   ```
   - volume 挂载发生在容器启动时
   - ENTRYPOINT 指定的命令在 volume 挂载之后执行
   - 因此可以正确访问和操作挂载的 volume

2. **实现运行时初始化**：
   ```bash
   # init.sh
   if [ -z "$(ls -A $ARTICLES_DIR)" ]; then
       git clone ...  # 只在目录为空时克隆
   fi
   ```
   - 可以根据运行时状态做出决策
   - 避免重复初始化
   - 实现优雅的启动逻辑

3. **支持容器重用**：
   - 第一次运行时初始化数据
   - 后续重启时保持数据不变

### 对比错误做法

如果我们在 `RUN` 指令中执行初始化：
```dockerfile
# ❌ 错误做法
RUN git clone https://github.com/xxx/xxx.git /articles-data
```
- 克隆的内容会被写入镜像层
- 容器启动时，volume 挂载会覆盖这些内容
- 每次构建镜像都会执行克隆，浪费资源

### 最佳实践总结

1. **构建时（Dockerfile）**：
   ```dockerfile
   # 只做环境准备
   RUN apk add --no-cache git dcron
   
   # 准备必要的脚本和目录
   COPY init.sh /usr/local/bin/
   RUN chmod +x /usr/local/bin/init.sh
   ```

2. **运行时（ENTRYPOINT）**：
   ```dockerfile
   # 延迟到容器启动时执行初始化
   ENTRYPOINT [ "/usr/local/bin/init.sh" ]
   ```

3. **初始化脚本（init.sh）**：
   ```bash
   # 在 volume 挂载后执行实际的初始化操作
   if [ -z "$(ls -A $ARTICLES_DIR)" ]; then
       git clone ...
   fi
   ```

这种模式确保了：
- 正确的执行顺序
- 数据持久化
- 优雅的初始化流程
- 资源的有效利用

所以是的，利用 `ENTRYPOINT` 的运行时执行特性是这个解决方案的关键。这让我们可以在正确的时机（volume 挂载后）执行必要的初始化操作。
