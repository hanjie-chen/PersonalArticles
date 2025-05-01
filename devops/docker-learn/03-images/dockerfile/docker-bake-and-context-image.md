# background

在研究 owasp/modsecurity-crs:nginx-alpine 的时候发现在其 `nginx/` 目录下存在 2 个 dockerfile: `Dockerfile`, `Dockerfile-alpine`

但是看这里 2 个 dockerfile 并没有发现其 source image 而是仅仅如下的一句指令

```dockerfile
FROM image AS build
```

这让我百思不得其解，和 gpt-4o 讨论之后发现原来是使用了 docker buildx

# Docker buildx

关键在于这句：

```Dockerfile
FROM image AS build
```

和常见的：

```Dockerfile
FROM alpine
# 或者 FROM nginx:alpine
```

不同，因为这个 Dockerfile 是一个“模板型”的 Dockerfile，它依赖的是一个外部构建系统（比如 `docker-bake.hcl` 或 CI 系统）来动态地指定 `image` 是什么镜像。

这里的 `image` 实际上是一个 变量/占位符，并不是一个固定的基础镜像名。它实际的值（比如 `nginx:alpine`, `debian:bullseye`, `ubuntu`, 等）是由外部构建系统提供的。

这个项目使用了 `docker-bake.hcl` 构建文件，它是 Docker 官方 [`docker buildx bake`](https://docs.docker.com/build/bake/) 功能的一部分，用来定义各种构建组合、变量、镜像版本等。

## docker-bake.hcl

打开 project root 中的 `docker-bake.hcl` 文件可以看到关于 nginx 的关键部分的代码

```hcl
target "nginx" {
    matrix = {
        base = [
            {
                name = "debian"
                dockerfile = "nginx/Dockerfile"
                image = "docker-image://nginxinc/nginx-unprivileged:${nginx-version}"
                ...
            },
            {
                name = "alpine"
                dockerfile = "nginx/Dockerfile-alpine"
                image = "docker-image://nginxinc/nginx-unprivileged:${nginx-version}-alpine"
                ...
            }
        ],
        ...
    }
    ...
    contexts = {
        image = base.image
    }
    dockerfile = base.dockerfile
    ...
}
```



`target "nginx"` 定义了两个“变体”：

| 名称       | Dockerfile 路径           | 基础镜像（即你问的 OS）                               |
| ---------- | ------------------------- | ----------------------------------------------------- |
| **debian** | `nginx/Dockerfile`        | `nginxinc/nginx-unprivileged:${nginx-version}`        |
| **alpine** | `nginx/Dockerfile-alpine` | `nginxinc/nginx-unprivileged:${nginx-version}-alpine` |

也就是说：

- `nginx/Dockerfile` 使用的是基于 **Debian** 的 `nginxinc/nginx-unprivileged` 镜像。
- `nginx/Dockerfile-alpine` 使用的是基于 **Alpine** 的 `nginxinc/nginx-unprivileged:...-alpine` 镜像。

`image = "docker-image://..."` 是 BuildKit 的语法，用于指定构建时传入的基础镜像值。



### `FROM image` 如何绑定镜像？

在 Dockerfile 中你看到的：

```Dockerfile
FROM image AS build
```

是在这里绑定的：

```hcl
contexts = {
    image = base.image
}
```

这意味着 `FROM image` 实际上就是：

```Dockerfile
FROM nginxinc/nginx-unprivileged:1.28.0-alpine （或 1.28.0）
```

# continue

[Nginx Dockerfile 对比](https://chatgpt.com/c/68122799-8c60-800a-8b14-1a28398cc6fe)

desired index

```markdown
# 多 Dockerfile 与 Buildx Bake 构建机制

## 背景
- 项目使用多个 Dockerfile（例如 alpine 与 debian）
- Dockerfile 中使用了 `FROM image` 占位符
- 构建行为由 `docker-bake.hcl` 控制

## docker-bake.hcl 关键概念
- matrix 构建（多平台、多变体）
- context.image 如何传入 Dockerfile
- 多阶段构建与镜像组合策略

## Buildx & Bake 简介
- 什么是 docker buildx？
- 什么是 docker buildx bake？
- 命令示例：查看 / 构建

## 实践例子：modsecurity-crs-docker 项目
- 如何构建 nginx-alpine 版本
- 如何手动构建不使用 bake

## 总结
- `FROM image` 背后是 context 注入机制
- bake 的多维构建非常适合复杂项目

```

