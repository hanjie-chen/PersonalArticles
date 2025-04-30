# Alpine Linux

独立的发行版

- Alpine Linux 是一个独立的、安全导向的、轻量级的 Linux 发行版
- 不是基于 Debian、Ubuntu 或其他主流发行版
- 使用 musl libc 而不是 glibc
- 使用 BusyBox 替代 GNU 工具

包管理器
- Alpine 使用 `apk` (Alpine Package Keeper) 作为包管理器
- Debian/Ubuntu 使用 `apt`/`apt-get`
- RHEL/CentOS 使用 `yum`/`dnf`

### 常见的基础镜像对比：

```plaintext
1. Alpine Linux
   - 包管理器: apk
   - 大小: ~5MB
   - 特点: 超轻量级

2. Debian
   - 包管理器: apt/apt-get
   - 大小: ~114MB
   - 特点: 稳定性好

3. Ubuntu
   - 包管理器: apt/apt-get
   - 大小: ~188MB
   - 特点: 更新快，包多

4. CentOS
   - 包管理器: yum/dnf
   - 大小: ~200MB
   - 特点: 企业级稳定性
```

### 为什么选择 Alpine？

1. **体积优势**：
   ```bash
   # 镜像大小对比
   alpine:3.19     ~5MB
   debian:11-slim  ~80MB
   ubuntu:22.04    ~188MB
   ```

2. **安全性**：
   - 默认启用安全特性
   - 定期的安全更新
   - 简化的系统减少攻击面

3. **资源消耗**：
   - 内存占用更少
   - 启动更快
   - 适合容器化应用

### 选择建议：

1. **使用 Alpine 的场景**：
   - 简单的应用
   - 对镜像大小敏感
   - 不需要特定的 glibc 功能

2. **使用 Debian/Ubuntu 的场景**：
   - 需要完整 GNU 工具链
   - 依赖特定的 glibc 功能
   - 需要更广泛的包支持

3. **使用 CentOS 的场景**：
   - 企业级应用
   - 需要长期支持
   - 特定的企业软件要求

### 注意事项：

1. **包名差异**：
   ```dockerfile
   # Alpine
   RUN apk add --no-cache dcron
   
   # Debian/Ubuntu
   RUN apt-get install -y cron
   
   # CentOS
   RUN yum install -y cronie
   ```

2. **系统差异**：
   - Alpine 使用 OpenRC 而不是 systemd
   - 文件位置可能不同
   - 配置方式可能不同

3. **兼容性考虑**：
   - 某些应用可能不兼容 musl libc
   - 某些二进制文件可能需要 glibc

总的来说，Alpine 是容器化应用的优秀选择，但要根据具体需求选择合适的基础镜像。如果你的应用没有特殊要求，使用 Alpine 是个不错的选择，因为它轻量、安全、资源占用少。

# alpine shell

Alpine Linux 为了保持轻量级，默认使用的是 `sh`（具体是 `ash`，来自 BusyBox），而不是 `bash`。

正确的命令应该是：

```bash
docker run -it alpine:3.19 /bin/sh
```

或者简单写成：
```bash
docker run -it alpine:3.19 sh
```

如果您确实需要在 Alpine 容器中使用 bash，您需要先安装它：

1. 首先运行容器：
```bash
docker run -it alpine:3.19 sh
```

2. 然后在容器内安装 bash：
```bash
apk add bash
```

3. 之后就可以使用 bash 了：
```bash
bash
```

补充说明：
- 如果您的应用不特别需要 bash，建议直接使用 sh，这样可以保持镜像的轻量级特性

# alpine in other image

许多官方镜像基于 Alpine Linux 构建，以提供轻量化的运行环境。

例如

`nginx:alpine` image

镜像名称：`nginx:alpine` 是 Docker Hub 上 Nginx 官方镜像的一个变体（tag）。

- `nginx`：表示这是 Nginx Web 服务器的镜像。
- `:alpine`：指定使用 Alpine Linux 作为基础操作系统，



