# `apt` 命令详解

apt (advanced package tool) 是 Debian 及其衍生版本（如 Ubuntu）的包管理系统。

## `apt-get` VS `apt`

apt-get 的输出稳定，更适合脚本处理，例如 Dockerfile, auto-scripts, CI/CD flow

apt更适合命令行交互，其输出包含进度条等交互元素，格式可能随版本变化



# Essential Commands (Daily Usage)

### update pakcage-index
```bash
# apt-get 方式
apt-get update

# apt 方式
apt update
```

### update package

```bash
# 更新所有包
apt-get upgrade

# 更新所有包，必要时可以删除旧包
apt-get dist-upgrade

# apt 方式
apt upgrade
apt full-upgrade  # 相当于 dist-upgrade
```

### install

```bash
# apt-get 方式
apt-get install package_name

# apt 方式
apt install package_name

# 常用选项：
-y          # 自动确认
--no-install-recommends  # 不安装推荐的包
--no-install-suggests   # 不安装建议的包
```

### delete
```bash
# 仅删除软件
apt-get remove package_name

# 删除软件和配置文件
apt-get purge package_name
# 或
apt-get remove --purge package_name

# 删除自动安装且不再使用的依赖包
apt-get autoremove
```

### search
```bash
# 搜索包
apt-cache search keyword

# 显示包信息
apt-cache show package_name

# apt 方式
apt search keyword
apt show package_name
```

# Advanced Usage

### check package dependency

```bash
# 查看依赖
apt-cache depends package_name

# 查看被依赖
apt-cache rdepends package_name
```

### clean

```bash
# 清理已下载的安装包
apt-get clean

# 清理旧版本的安装包
apt-get autoclean

# 清理不再使用的依赖包
apt-get autoremove
```

### 

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
