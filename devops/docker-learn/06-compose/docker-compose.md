# Docker Compose 简介
Docker Compose 是一个用于定义和运行多容器 Docker 应用程序的工具。使用 compose.yml 文件来配置应用程序的服务、网络和 Volume

## compose.yml 的主要作用
多容器管理
- 在一个文件中定义多个容器
- 统一管理多个相关联的服务
- 简化容器的启动和停止过程

服务编排
- 定义容器之间的依赖关系
- 设置容器的启动顺序
- 配置容器间的网络连接

## compose.yml 基本结构
```yaml
version: '3'  # Compose文件版本
services:     # 定义服务
  web:        # 服务名称
    image: nginx:latest  # 使用的镜像
    ports:    # 端口映射
      - "80:80"
    volumes:  # 数据卷挂载
      - ./html:/usr/share/nginx/html
    
  db:         # 另一个服务
    image: mysql:5.7
    environment:  # 环境变量
      MYSQL_ROOT_PASSWORD: example
```

需要了解更具体的内容或者有什么疑问，欢迎继续询问！

> [!note]
>
> `compose.yml` VS `docker-compose.yml`
>
> 本质上是同一个东西，都是 Docker Compose 的配置文件，区别仅在于：
>
> - `docker-compose.yml` 是较老的命名方式（Docker Compose V1）
> - `compose.yml` 是较新的命名方式（Docker Compose V2）
>
> 新项目推荐使用 `compose.yml`，更简洁现代

# `compose.yml` 使用场景

如果你的应用符合以下任一条件，建议使用 compose.yml：
- 配置项超过 3 个以上
- 需要设置环境变量
- 需要配置数据卷
- 需要特定的网络设置
- 将来可能需要添加其他服务
- 需要与他人分享或版本控制配置

以下情况可以直接使用 docker run：
- 只是简单测试某个镜像
- 配置极其简单（如只需要端口映射）
- 一次性运行的容器
