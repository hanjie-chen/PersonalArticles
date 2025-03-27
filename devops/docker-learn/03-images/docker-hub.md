# Docker hub

Docker Hub 是 Docker 公司提供的官方云端容器镜像仓库服务。

它类似于 GitHub，但专门用来存储、分发和管理 Docker 镜像的。开发者可以将自己构建的镜像推送到 Docker Hub，也可以从中拉取官方或其他开发者共享的镜像

Repositories 用户可以创建公共或私有仓库来存储自己的 Docker 镜像



## hub repository

准确地说，一个 Docker Hub Repository 通常用来存放一个特定镜像的不同版本（Tags）

例如 `web-app` image 可能会有开发版 (`dev`)，一个稳定版 (`latest` 或 `v1.0`) 这些不同的版本都属于 `web-app` 这个逻辑上的镜像。

在 Docker Hub 上，创建一个名为 `yourusername/my-website-webapp` 的 Repository 之后，你可以推送不同的标签 (Tags) 到这个仓库里，例如：
*   `yourusername/my-website-webapp:latest`
*   `yourusername/my-website-webapp:dev`

所以，一个 Repository (仓库) 对应一个基础镜像项目或应用，但可以通过 **Tags** 来管理它的多个不同变体或版本。

不能（也不应该）把完全不相关的镜像（比如 `web-app` 的镜像和 `articles-sync` 的镜像）硬塞到同一个 Repository 里。它们是两个不同的应用，应该有各自独立的 Repository



## hub limitation

Docker Hub 的免费用户计划只允许你拥有 1 个 private repository 和无限多的 public repository
