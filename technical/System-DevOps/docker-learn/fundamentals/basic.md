# Docker Basic

学习路径：

1. 重点学习Docker Engine的使用——docker 命令的使用
3. 理解Docker的核心概念（容器、镜像、网络、存储等）
4. 学习Docker Compose、Dockerfile的编写等

以 [docker/getting-started-todo-app: Sample application to get started with Docker](https://github.com/docker/getting-started-todo-app) 为例

> [!note]
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

