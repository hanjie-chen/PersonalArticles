# Docker Basic

所以，如果您想真正掌握Docker技术：

1. 重点学习Docker Engine的使用
2. 掌握命令行操作
3. 理解Docker的核心概念（容器、镜像、网络、存储等）
4. 学习Docker Compose、Dockerfile的编写等

## Docker desktop VS Docker Engine

Docker Desktop只是一个辅助工具，而不是必需品。特别是在生产环境中，几乎都是直接使用Docker Engine的命令行操作。这也是为什么在Linux服务器上，通常只安装Docker Engine。

### Docker Engine

这是真正需要学习和掌握的Docker技术核心，包含了所有基本的Docker功能：dockerd（Docker守护进程）、Docker CLI（命令行接口）、Docker API、容器运行时

### Docker Desktop

本质上是一个包装了Docker Engine的图形化应用程序，提供了容器和镜像的可视化管理，简单的设置界面和一些额外的开发工具集成 

## Install Docker Engine

[Install | Docker Docs](https://docs.docker.com/engine/install/) 选择一个合适的 OS 例如 Ubuntu : [Ubuntu | Docker Docs](https://docs.docker.com/engine/install/ubuntu/)