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
EXPOSE 5000  # 声明容器将使用的端口
```
- 这只是声明，实际运行时还需要通过 -p 参数映射端口

## **CMD**：容器启动命令

```Dockerfile
CMD ["python", "app.py"]  # 容器启动时执行的命令
```
使用数组形式可以更好地处理参数

# `EXPOSE` 指令

**EXPOSE 的作用**

- `EXPOSE` 指令实际上只是一个文档性质的声明，告诉使用者这个容器内的应用程序会使用哪些端口
- 它 **不会** 实际开放任何端口
- 可以理解为它是一种 "元数据"，一种使用说明

**重要说明**

- `EXPOSE` 并不会使端口在主机上可访问
- 要使端口实际可访问，在运行容器时还需要使用 `-p` 或 `-P` 参数

**实际例子**

```Dockerfile
# Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

运行容器的不同方式：

```bash
# 方式1：不映射端口
docker run my-app
# 结果：容器内的应用运行在5000端口，但从主机无法访问

# 方式2：明确映射端口（常用）
docker run -p 8080:5000 my-app
# 结果：可以通过主机的8080端口访问容器的5000端口

# 方式3：使用-P自动映射
docker run -P my-app
# 结果：Docker会自动将EXPOSE的端口映射到主机的随机高位端口
```

4. **多端口示例**
```Dockerfile
# 可以EXPOSE多个端口
EXPOSE 5000 80 443
```

5. **实际应用场景**

假设你有一个 Flask 应用：
```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

对应的 Dockerfile：
```Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

运行方式：
```bash
# 将容器的5000端口映射到主机的8080端口
docker run -p 8080:5000 my-flask-app

# 现在可以通过以下地址访问：
# http://localhost:8080
```

6. **端口映射的不同方式**
```bash
# 映射到特定端口
docker run -p 8080:5000 my-app  # 主机8080映射到容器5000

# 映射到特定接口的特定端口
docker run -p 127.0.0.1:8080:5000 my-app  # 只允许本地访问

# 映射到随机端口
docker run -P my-app  # 自动映射 EXPOSE 的端口到随机端口
```

7. **查看端口映射**
``` bash
# 查看容器的端口映射情况
docker ps
# 或
docker port <container_id>
```

总结：
- `EXPOSE` 是声明性的，告诉用户这个容器需要使用哪些端口
- 实际的端口映射需要在 `docker run` 时通过 `-p` 或 `-P` 参数完成
- 容器内的应用可以使用任何端口，不一定要是 `EXPOSE` 声明的端口
- `EXPOSE` 主要用于：
  - 文档目的（告诉其他人这个容器使用什么端口）
  - 配合 `-P` 参数实现自动端口映射
  - 在 Docker Compose 或其他容器编排工具中提供信息

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
