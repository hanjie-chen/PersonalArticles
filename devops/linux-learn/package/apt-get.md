# `apt` 命令详解

apt (advanced package tool) 是 Debian 及其衍生版本（如 Ubuntu）的包管理系统。

> [!note]
>
> `apt-get` VS `apt`
>
> apt-get 的输出稳定，更适合脚本处理，例如 Dockerfile, auto-scripts, CI/CD flow
>
> apt更适合命令行交互，其输出包含进度条等交互元素，格式可能随版本变化

如果我们想要现在一个或者多个 package 比如说 npm, node.js 那么我们一般这样子操作

```shell
sudo apt update
sudo apt install -y nodejs npm
```

- `sudo apt update`: 刷新本机的 package index，所谓的 package index 也就是你能装到哪些版本、从哪个镜像拿
- `sudo apt install -y nodejs npm`: 下载 node.js, npm 并且每次询问的时候都回答 yes（不用手动输入）





# System configuration

### configuration file
```bash
/etc/apt/sources.list          # 主要的软件源配置文件
/etc/apt/sources.list.d/       # 额外的软件源配置目录
```

### cache directories
```bash
/var/cache/apt/archives/      # 下载的软件包缓存
/var/lib/apt/lists/          # 软件包信息列表
```

# Prefessional Usage

适用于 Dockerfile, auto-scripts, CI/CD flow

## Dockerfile best practices

在 Dockers 官方文档中 [Best practices | Docker Docs](https://docs.docker.com/build/building/best-practices/) 均使用 `apt-get` 

### 基本安装模板
```dockerfile
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    package1 \
    package2 \
    package3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
```

### 最小化安装
```dockerfile
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    --no-install-recommends \
    package_name \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
```

### 指定版本安装
```dockerfile
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    package_name=specific_version \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
```

> [!note]
>
> 始终在安装包之前运行 `apt-get update`
>
> 在脚本或 Dockerfile 中使用 `-y` 选项，自动确认
>
> 在完成安装后清理缓存，用于保持容器镜像小巧
