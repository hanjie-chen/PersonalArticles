# Docker Compose 简介
Docker Compose 是一个用于定义和运行多容器 Docker 应用程序的工具。使用 compose.yml 文件来配置应用程序的服务、网络和 Volume

## compose.yml 的主要作用
1. **多容器管理**
   - 在一个文件中定义多个容器
   - 统一管理多个相关联的服务
   - 简化容器的启动和停止过程

2. **服务编排**
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

## 常用命令
1. 启动所有服务：
```bash
docker compose up
```

2. 后台运行服务：
```bash
docker compose up -d
```

3. 停止并删除所有服务：
```bash
docker compose down
```

## compose.yml 的优势
1. **可重复性**
   - 配置文件可以版本控制
   - 确保开发、测试、生产环境一致

2. **简化复杂度**
   - 不需要编写复杂的 docker run 命令
   - 所有配置集中在一个文件中

3. **服务间依赖管理**
   - 自动处理服务启动顺序
   - 确保依赖服务先启动

## 实际应用示例
这是一个包含 Web 应用和数据库的典型配置：

```yaml
version: '3'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    depends_on:
      - db
    environment:
      DATABASE_URL: postgresql://postgres:example@db:5432/mydb

  db:
    image: postgres
    environment:
      POSTGRES_PASSWORD: example
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## 使用建议
1. 开始时可以从简单的配置开始
2. 逐步添加更多服务和配置
3. 注意查看官方文档中的最佳实践
4. 使用版本控制管理配置文件

compose.yml 是 Docker 生态系统中非常重要的工具，特别适合开发环境和小型部署。随着您对 Docker 的深入学习，您会发现它是一个非常有用的工具。

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

单容器使用 compose.yml 的优缺点

### 优点

1. **配置更清晰**
   - 所有配置都在一个文件中，结构化管理
   - 比长串的 docker run 命令更易读和维护

2. **便于版本控制**
   - 配置可以纳入代码仓库
   - 方便追踪配置变更

3. **未来扩展方便**
   - 如果之后需要添加其他服务（如数据库），直接在同一文件中添加
   - 不需要重新学习新的配置方式

### 缺点

1. **可能显得有点重**
   - 对于非常简单的应用，显得配置过度
   - 增加了一个额外的配置文件

2. **学习成本**
   - 需要了解 Compose 文件的语法
   - 对于完全的初学者可能有些复杂

## 使用场景建议

### 适合使用 compose.yml 的情况：

1. **配置较复杂**
```yaml
services:
  app:
    image: nginx
    ports:
      - "80:80"
    volumes:
      - ./html:/usr/share/nginx/html
    environment:
      - NODE_ENV=production
    restart: always
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

2. **需要频繁修改配置**
   - 经常调整端口映射
   - 需要修改环境变量
   - 需要调整数据卷挂载

3. **项目可能扩展**
   - 未来可能添加数据库
   - 可能需要添加缓存服务
   - 可能需要添加其他中间件

### 适合直接使用 docker run 的情况：

1. **极简单的场景**
```bash
docker run -d -p 80:80 nginx
```

2. **一次性运行**
   - 临时测试某个镜像
   - 做简单的验证实验

## 实际例子对比

### 使用 docker run 命令：
```bash
docker run -d \
  --name my-nginx \
  -p 80:80 \
  -v $(pwd)/html:/usr/share/nginx/html \
  --restart always \
  nginx:latest
```

### 使用 compose.yml：
```yaml
services:
  web:
    image: nginx:latest
    container_name: my-nginx
    ports:
      - "80:80"
    volumes:
      - ./html:/usr/share/nginx/html
    restart: always
```

## 建议

1. **如果你的应用符合以下任一条件，建议使用 compose.yml**：
   - 配置项超过 3 个以上
   - 需要设置环境变量
   - 需要配置数据卷
   - 需要特定的网络设置
   - 将来可能需要添加其他服务
   - 需要与他人分享或版本控制配置

2. **以下情况可以直接使用 docker run**：
   - 只是简单测试某个镜像
   - 配置极其简单（如只需要端口映射）
   - 一次性运行的容器

## 最佳实践

即使是单容器，我个人还是更倾向于使用 compose.yml，原因是：

1. **可维护性**
   - 配置清晰明了
   - 易于修改和维护

2. **一致性**
   - 保持项目结构的一致性
   - 便于团队协作

3. **可扩展性**
   - 未来添加服务更容易
   - 不需要重新学习新的工具

总结：虽然对于单容器来说使用 compose.yml 可能看起来有点"大材小用"，但从长远来看，使用 compose.yml 管理容器配置是一个更好的选择。它提供了更好的可维护性和扩展性，特别是当你的项目逐渐变得复杂时。

# `compose.yml` 语法详解

## `version`
根据最新的 docker compose 规范 [Version and name top-level elements | Docker Docs](https://docs.docker.com/reference/compose-file/version-and-name/)

Compose 不再使用此字段来选择验证模式， 而是默认使用最新的模式来解析文件，如果使用此字段会收到警告消息
