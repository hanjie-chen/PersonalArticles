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

## 单容器使用 compose.yml 的优缺点

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