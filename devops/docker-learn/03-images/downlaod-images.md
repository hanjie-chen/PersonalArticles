下载 Docker 镜像的基本命令是：

```bash
docker pull [镜像名称]:[标签]
```

一些使用示例：

1. 下载最新版本的镜像（默认 tag 为 latest）：
```bash
docker pull ubuntu
```

2. 下载指定版本的镜像：
```bash
docker pull ubuntu:20.04
```

3. 从特定仓库下载镜像：
```bash
docker pull registry.example.com/ubuntu:20.04
```

一些常用的参数：
- `-a` 或 `--all-tags`：下载仓库中的所有标签
- `--disable-content-trust`：跳过镜像验证
- `--platform`：指定平台，如 linux/amd64, linux/arm64 等

下载完成后，你可以使用 `docker images` 命令查看已下载的镜像列表。