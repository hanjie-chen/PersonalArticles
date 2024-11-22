# Docker Basic

学习路径：

1. 重点学习Docker Engine的使用——docker 命令的使用
3. 理解Docker的核心概念（容器、镜像、网络、存储等）
4. 学习Docker Compose、Dockerfile的编写等

以 [docker/getting-started-todo-app: Sample application to get started with Docker](https://github.com/docker/getting-started-todo-app) 为例

> ![note]
>
> Docker Engine是核心技术组件，包含CLI、API和运行时；Docker Desktop则是其图形界面封装，提供可视化管理工具，主要用于开发环境。生产环境通常直接使用Engine。

# Docker Architecture

![architecture](./images/docker-architecture.webp)

Docker的架构是基于 Client-Server 模型的。主要包括以下几个部分：

1. Docker Client
   - 这是用户与Docker交互的主要方式。
   - 当你在命令行输入Docker命令时，你就是在使用Docker客户端。
   - 例如，当你输入 `docker run` 命令时，客户端会将这个命令发送给Docker守护进程。

2. Docker Daemon (dockerd)
   - 这是Docker的核心，运行在后台。
   - 它负责管理Docker对象，如镜像、容器、网络和数据卷。
   - 守护进程接收来自Docker客户端的命令并执行它们。

3. Docker Images
   - 这些是用来创建Docker容器的只读模板。
   - 镜像包含了运行应用所需的所有内容：代码、运行时环境、库、环境变量和配置文件。

4. Docker Containers
   - 容器是镜像的可运行实例。
   - 你可以创建、启动、停止、移动或删除容器。
   - 每个容器都是相互隔离的安全平台。

5. Docker Registry
   - 这是用来存储Docker镜像的地方。
   - Docker Hub是一个公共注册表，任何人都可以使用。
   - 你也可以运行自己的私有注册表。

工作流程：
1. 用户通过Docker客户端发出命令。
2. Docker守护进程接收这些命令并管理Docker对象。
3. 如果需要，守护进程会从注册表拉取或推送镜像。
4. 守护进程使用这些镜像创建和管理容器。

这种架构允许Docker在不同的环境中一致地运行，无论是本地开发机器、公司服务器还是云平台。它使得应用程序的开发、测试和部署变得更加简单和标准化。

Docker hub & Docker Image

[Docker Hub](https://hub.docker.com) 是 Docker 官方维护的公共镜像仓库，类似于 GitHub，包含了大量官方和社区维护的镜像

以Ubuntu镜像为例，与Server ISO（2.6GB）不同，Docker镜像经过精简（约30MB），仅保留基础组件。镜像可自动下载存储，支持本地缓存复用，通过docker images查看。

# `docker run` command

`docker run -i -t ubuntu /bin/bash` 命令详解

这个命令是用来启动一个 Ubuntu 容器的，让我们逐个部分来分析：

`docker run`：

- 这是基础命令，用于创建并启动一个新的容器
- 如果本地没有所需的镜像，Docker 会自动从 Docker Hub 下载

`-i`（interactive）：

- 保持标准输入（STDIN）开启
- 允许你与容器进行交互
- 如果不加这个参数，你将无法向容器输入命令

`-t`（terminal）：

- 分配一个伪终端（pseudo-TTY）
- 提供一个交互式的终端界面
- 让你可以像使用普通的命令行终端一样使用容器

`ubuntu`：

- 这是要使用的 Docker 镜像的名称
- 在这里指的是官方的 Ubuntu 操作系统镜像
- 如果本地没有这个镜像，Docker 会从 Docker Hub 自动下载最新版本

`/bin/bash`：

- 这是容器启动后要执行的命令
- bash 是一个命令行解释器（shell）
- 这将在容器内启动一个 bash shell，让你可以在容器内执行命令

实际效果：
- 运行这个命令后，你会进入到一个 Ubuntu 容器的命令行界面
- 你可以像使用普通的 Ubuntu 系统一样，在容器内执行各种 Linux 命令
- 要退出容器，你可以：
  - 输入 `exit` 命令
  - 或使用 `Ctrl + D` 快捷键

一个类比：想象你在电脑上运行了一个虚拟机，但这个"虚拟机"（容器）非常轻量级，启动速度很快，而且只包含运行应用所需的最基本组件。

需要注意的是，这个容器在你退出 bash shell 后就会停止运行，除非你特别指定了其他参数（比如 `--rm` 参数会在容器停止后自动删除容器）。

***

```bash
docker run -d -p 8080:80 docker/welcome-to-docker
```

这个命令可以拆分成几个部分：

1. `docker run`
   - 这是基础命令，表示"运行一个容器"
   - 相当于告诉Docker："我要启动一个新的容器"

2. `-d`
   - 代表 "detached" 模式
   - 意思是在后台运行容器
   - 如果不加这个参数，容器会在前台运行，占据你的终端窗口

3. `-p 8080:80`
   - `-p` 表示端口映射（port mapping）
   - `8080:80` 的格式是 `主机端口:容器端口`
   - 意思是：把容器内的80端口映射到主机的8080端口
   - 这样你就可以通过访问 `localhost:8080` 来访问容器中运行的web服务

4. `docker/welcome-to-docker`
   - 这是容器镜像的名称
   - `docker/` 是镜像所属的组织/用户
   - `welcome-to-docker` 是具体的镜像名称
   - 这是一个官方提供的示例镜像，运行后会显示一个欢迎页面

用生活中的例子来解释的话：
- 如果把容器比作一个外卖餐盒
- `docker run` 就是打开这个餐盒
- `-d` 就是把餐盒放在一边，你可以继续做其他事
- `-p 8080:80` 就像是在餐盒上开了个小窗口（80），然后用一根吸管（8080）连接到外面，这样你就可以喝到里面的饮料了
- `docker/welcome-to-docker` 就是这个餐盒的品牌和型号

运行这个命令后：
1. Docker会先下载这个镜像（如果本地没有的话）
2. 然后创建一个新的容器
3. 在后台运行这个容器
4. 设置端口映射，让你可以通过 `http://localhost:8080` 访问容器中的web服务

这就是为什么文章中说运行这个命令后，可以通过浏览器访问 `http://localhost:8080` 来看到欢迎页面。

默认情况下，使用 `-p` 参数时就会监听所有接口：

```bash
docker run -d -p 8080:80 docker/welcome-to-docker
```
这个命令实际上等同于：
```bash
docker run -d -p 0.0.0.0:8080:80 docker/welcome-to-docker
```

2. 如果你想明确指定监听地址，可以使用完整格式：
```bash
docker run -d -p [host-ip]:[host-port]:[container-port] image-name
```

# `docker ps` command

要查看正在运行的 Docker 容器，可以使用以下命令：

```bash
docker ps
```

这个命令会显示所有正在运行的容器，包括以下信息：
- CONTAINER ID：容器的唯一标识符
- IMAGE：容器使用的镜像
- COMMAND：容器启动时运行的命令
- CREATED：容器的创建时间
- STATUS：容器的当前状态
- PORTS：容器映射的端口
- NAMES：容器的名称

如果你想查看所有容器（包括已停止的容器），可以使用：

```bash
docker ps -a
```

# `docker compose` command

`docker compose` 命令基于当前目录下的 compose.yaml 或者 docker-compose.yaml 文件来操作

**项目隔离**

- 每个使用 Docker Compose 的项目都是独立的
- 容器名称会自动加上项目名作为前缀
- 网络也是独立的，默认创建的网络名称为 `项目名_default`

例如：

**docker compose up -d**

- 只会启动当前 compose 文件中定义的服务
- `-d` 表示 detached 模式（后台运行）
- 会自动使用当前目录名作为项目名称前缀
- 如果服务之前没有构建过镜像，会自动构建

```bash
# 只会启动 getting-started-todo-app 项目中定义的服务
sudo docker compose up -d
```

**docker compose down**

- 只会停止和删除当前 compose 文件中定义的服务的容器
- 同时也会删除默认网络
- 不会影响其他项目的容器

```bash
# 只会关闭 getting-started-todo-app 项目的容器
sudo docker compose down
```







## `docker compose watch`

`docker compose watch` 是 Docker Compose 的一个重要功能，主要用于开发环境中实现实时更新。它的主要作用和特点如下：

**实时文件监控**

- 监视项目中的源代码文件变化
- 当检测到文件变更时，自动重新构建和更新相关的容器
- 无需手动重启容器或重新运行 compose 命令

**工作原理**

- 持续监控指定的目录和文件
- 当发现文件变化时，根据配置执行以下操作之一：
  - 同步文件变更到容器中
  - 重新构建容器
  - 重启受影响的服务

这个命令特别适合在开发环境中使用，它极大地提高了使用 Docker 进行开发时的效率。在文章中的 todo 应用例子里，正是这个命令让我们能够实时看到对前端样式、后端逻辑的修改效果，而不需要手动重启任何服务。

## `docker compose ps`

`docker ps` 和 `docker compose ps` 有以下几个主要区别：

**显示范围不同**：

- `docker ps`：显示所有正在运行的容器，无论它们是如何启动的（手动启动、Docker Compose 启动等）
- `docker compose ps`：只显示由当前目录下的 docker-compose.yml（或 compose.yml）文件创建的容器

**上下文不同**：

- `docker ps`：在全局 Docker 环境中工作
- `docker compose ps`：在特定的 Compose 项目上下文中工作，与当前目录的 compose 文件相关联

**输出格式不同**：

`docker ps` 默认显示：

- CONTAINER ID
- IMAGE
- COMMAND
- CREATED
- STATUS
- PORTS
- NAMES

`docker compose ps` 通常更关注于 Compose 服务，显示：

- NAME（使用 compose 项目名称作为前缀）
- COMMAND
- SERVICE
- STATUS
- PORTS

**使用场景**：

- `docker ps`：适合查看系统中所有运行的容器
- `docker compose ps`：适合在使用 Docker Compose 开发时查看特定项目的容器状态

例如，在你的项目中：
```bash
# docker compose ps 只会显示 getting-started-todo-app 相关的容器
sudo docker compose ps

# docker ps 会显示系统中所有运行的容器
sudo docker ps
```

建议：
- 当你在特定项目目录下工作时，使用 `docker compose ps` 更清晰
- 当你需要查看系统整体容器状态时，使用 `docker ps`
- 如果你想看到所有容器（包括停止的），可以使用 `docker ps -a` 或 `docker compose ps -a`
