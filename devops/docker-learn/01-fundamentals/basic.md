# Docker Basic

docker 的 安装 [Install | Docker Docs](https://docs.docker.com/engine/install/)

以 Ubuntu Linux 为例 [Ubuntu | Docker Docs](https://docs.docker.com/engine/install/ubuntu/)

删除存在冲突的 packages

```shell
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
```

设置 docker apt repository

```shell
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```

下载最新版本

```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

验证 docker 是否下载成功

```bash
sudo docker --version
```

> [!note]
>
> 这时，你还是需要 `sudo` 权限来运行 docker, 从而可能会遇到一些问题（例如 vscode plugin: devcontainer）
>
> [Post-installation steps | Docker Docs](https://docs.docker.com/engine/install/linux-postinstall/) 文档讲了如何不加 `sudo` 就可以使用 docker 命令
>
> 简单来说，就是在 Linux 系统中，Docker 守护进程默认绑定到一个 Unix socket，该 socket 归属于 root 用户和 docker 组。因此，要在不使用 sudo 的情况下运行 docker 命令，需要将用户添加到 docker 组。

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

