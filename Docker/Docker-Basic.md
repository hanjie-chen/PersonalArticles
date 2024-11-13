# Docker Basic

所以，如果您想真正掌握Docker技术：

1. 重点学习Docker Engine的使用
2. 掌握命令行操作
3. 理解Docker的核心概念（容器、镜像、网络、存储等）
4. 学习Docker Compose、Dockerfile的编写等

## Docker desktop VS Docker Engine

### Docker Engine

这是真正需要学习和掌握的Docker技术核心，包含了所有基本的Docker功能：dockerd（Docker守护进程）、Docker CLI（命令行接口）、Docker API、容器运行时

install docker engine: [Install | Docker Docs](https://docs.docker.com/engine/install/)

### Docker Desktop

本质上是一个包装了Docker Engine的图形化应用程序，提供了容器和镜像的可视化管理，简单的设置界面和一些额外的开发工具集成

在生产环境中，几乎都是直接使用Docker Engine的命令行操作。这也是为什么在Linux服务器上，通常只安装Docker Engine。

## Docker Architecture

![architecture](./images/docker-architecture.webp)

Docker的架构是基于客户端-服务器模型的。主要包括以下几个部分：

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

# Docker Containers Command

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

# Docker hub & Docker Image

[Docker Hub](https://hub.docker.com) 是 Docker 官方维护的公共镜像仓库，类似于 GitHub 之于代码，包含了大量官方和社区维护的镜像

如果我查看 [Get Ubuntu Server | Download | Ubuntu](https://ubuntu.com/download/server) 镜像，那么就会发现其大小在2.6 GB 左右，难道 `docker run ubuntu` 命令要去拿这个大小的 iso 文件吗？

其实不是，关于 Ubuntu 镜像，这里有一个重要的区别：

Docker Hub 上的 Ubuntu 镜像和 Ubuntu Server ISO 是完全不同的

Docker 的 Ubuntu 镜像是经过特别精简的版本，Ubuntu Docker 镜像的大小远远小于 Ubuntu Server ISO，最新的 Ubuntu Docker 镜像大约只有 30 MB，这个大小是压缩后的大小，解压后可能会稍大一些，但仍然远小于完整的 Ubuntu Server

镜像大小的原因：
- Docker 镜像是经过特别精简的版本，只包含最基本的系统组件
- 它们移除了许多不必要的包和服务，只保留运行容器所需的最小集合
- 这种精简版的 Ubuntu 被称为 "Minimal Ubuntu"

下载和存储：
- 当你运行 `docker run ubuntu` 时，Docker 会从 Docker Hub 下载这个约 29 MB 的镜像
- Docker 会自动管理镜像的存储，你不需要手动创建文件夹
- 镜像默认存储在 Docker 的数据目录中，通常在 Linux 系统的 `/var/lib/docker` 目录下 [6]

本地镜像：
- 如果你已经下载过镜像，Docker 会直接使用本地的镜像，不会再次从 Docker Hub 下载
- 你可以使用 `docker images` 命令查看本地已有的镜像

轻量级特性：
- 正是因为这种精简的特性，Docker 容器才能实现快速启动和低资源消耗
- 与完整的虚拟机相比，Docker 容器确实非常轻量级 

