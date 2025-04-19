# Docker LearnOverview

```perl
docker-learn/
├── 01-fundamentals/          # 替代原来的 basic，包含 Docker 的基础概念
│   ├── images/
│   │   └── docker-architecture.webp
│   ├── introduction.md       # 基础介绍，Docker 是什么，为什么使用 Docker
│   ├── architecture.md       # Docker 架构
│   └── installation.md       # 安装指南
│
├── 02-containers/           # 容器相关操作
│   ├── container-basics.md  # 容器基础概念
│   ├── container-lifecycle.md # 容器生命周期
│   └── container-commands.md # 容器常用命令
│
├── 03-images/              # 替代原来的 docker-images
│   ├── image-basics.md     # 镜像基础概念
│   ├── dockerfile.md       # Dockerfile 详解
│   ├── dockerignore.md     # .dockerignore 文件说明
│   └── best-practices.md   # 最佳实践
│
├── 04-storage/             # 替代原来的 data-management
│   ├── volumes.md          # Docker 卷
│   ├── bind-mounts.md      # 绑定挂载
│   └── tmpfs-mounts.md     # 临时文件系统挂载
│
├── 05-networking/          # 新增网络部分
│   ├── network-basics.md   # 网络基础
│   └── network-types.md    # 网络类型
│
├── 06-compose/            # 独立出来的 Docker Compose
│   ├── compose-basics.md  # Compose 基础
│   └── compose-file.md    # docker-compose.yml 详解
│
├── 07-development/        # 开发环境相关（新增）
│   ├── devcontainer/      # Dev Container 相关
│   │   ├── basics.md      # Dev Container 基础
│   │   ├── configuration.md # devcontainer.json 配置详解
│   │   └── examples/      # 各种语言/框架的配置示例
│   └── best-practices.md  # 开发最佳实践
├── 08-runtime/        # 运行时相关
│   ├── container-entrypoint.md  # 本文内容
│   ├── signal-handling.md
│   ├── init-process.md
│   ├── zombie-process.md
└── README.md             # 项目说明和目录导航
```

