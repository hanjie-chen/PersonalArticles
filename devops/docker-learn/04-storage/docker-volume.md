# Docker Volume 

Docker volume 实际上是一个独立于容器的存储空间，它的生命周期独立于容器。可以把它理解为一个"共享文件夹"。

在 compose.yml 我们可以这样子定义和使用 volume

```yaml
services:
  web:
    volumes:
      - articles_data:/articles-data  # [volume名称]:[容器内挂载路径]
    
  articles-data:
    volumes:
      - articles_data:/articles-data

volumes:
  articles_data:  # 声明volume
```

这个配置的含义是：
1. `volumes: articles_data:` 声明了一个名为 `articles_data` 的volume
2. 这个volume被挂载到：
   - articles-data容器的 `/articles-data` 目录
   - web容器的 `/articles-data` 目录

### 3. 工作原理图解

```plaintext
┌─────────────────────────────────────┐
│    Docker Host 			          │
│                                     │
│  ┌────────────────┐                 │
│  │  Docker Volume │                 │
│  │ (articles_data)│                 │
│  └───────┬────────┘                 │
│          │                          │
│    ┌─────▼─────┐      ┌──────────┐  │
│    │/articles- │      │/articles-│  │
│    │   data    │      │   data   │  │
│    │           │      │          │  │
│    │articles-  │      │  web-app │  │
│    │data   	 │      │      	   │  │
│    └───────────┘      └──────────┘  │
└─────────────────────────────────────┘
```



这个volume实际存储在：

```bash
# Docker volumes默认存储在
/var/lib/docker/volumes/[volume-name]/_data
```

### 6. 验证方式

你可以通过以下命令验证volume的工作：

```bash
# 查看volume详情
docker volume ls
docker volume inspect articles_data

# 进入容器查看挂载点
docker exec -it web ls /articles-data
docker exec -it articles-data ls /articles-data
```



### 8. 重要注意事项

1. **数据持久性**：
   - Volume数据在容器重启后仍然存在
   - 删除容器不会删除volume

2. **权限问题**：
   ```dockerfile
   # 在articles-data的Dockerfile中
   RUN chown -R nobody:nobody /articles-data && \
       chmod -R 755 /articles-data
   ```

3. **同步问题**：
   - Volume是共享的，需要注意并发访问
   - 建议web容器以只读方式挂载：
   ```yaml
   web:
     volumes:
       - articles_data:/articles-data:ro  # 只读模式
   ```

现在你应该理解了：
1. Volume不属于任何容器，而是独立的存储空间
2. 多个容器可以同时挂载同一个volume
3. 这种机制使得容器间的数据共享变得简单和高效

这就是为什么虽然文件最初是在articles-data容器中创建的，但web容器也能访问这些文件的原因。

# docker build –> volumd mount

### 执行顺序

当你运行 `docker compose up` 时，顺序是这样的：

1. **首先创建 volume**：
   - Docker 创建名为 `articles_data` 的 volume
   - 此时 volume 是空的

2. **构建和启动 articles-data 容器**：
   - 执行 Dockerfile 中的命令
   - `WORKDIR /articles-data` 在容器内创建目录
   - `git clone` 命令将仓库克隆到该目录
   - 当容器启动时，volume 会挂载到 `/articles-data`
   - **重要**：volume 挂载会覆盖容器中对应路径的内容

3. **构建和启动 web-app 容器**：
   - volume 被以只读方式挂载到 `/articles-data`



1. **Volume 挂载时机**：
   - Volume 挂载发生在容器启动时
   - Dockerfile 中的操作（如 git clone）发生在镜像构建时
   - 这意味着在构建时克隆的文件会被 volume 挂载覆盖

2. **使用 entrypoint 脚本的好处**：
   - 可以检查 volume 是否已经包含数据
   - 只在需要时执行初始化
   - 避免重复克隆仓库

### 6. 数据持久性

使用这种设置：
- Volume 中的数据会在容器重启后保留
- 即使删除并重建容器，数据也不会丢失
- 只有显式删除 volume 才会删除数据：
  ```bash
  docker compose down -v  # 这会删除 volume
  ```

# an example

让我详细解释一下执行顺序，这样你就能更好理解为什么 init.sh 中的 git clone 不会被覆盖：

### 执行顺序

1. **构建阶段**（docker build）：
   ```dockerfile
   FROM alpine:3.19
   RUN apk add --no-cache git dcron
   COPY update-articles.sh init.sh /usr/local/bin/
   ...
   ENTRYPOINT [ "/usr/local/bin/init.sh" ]
   ```
   - 这时只是配置环境和复制脚本
   - 还没有执行 git clone

2. **启动阶段**（docker-compose up）：
   ```yaml
   services:
     app:
       volumes:
         - articles_data:/articles-data
   ```
   执行顺序是：
   1. 首先挂载 volume 到 `/articles-data`
   2. 然后执行 ENTRYPOINT 指定的 init.sh
   3. init.sh 检查 `/articles-data` 是否为空
   4. 如果为空，执行 git clone

所以：
- 之前说的"构建时克隆的文件会被 volume 挂载覆盖"是指如果你在 Dockerfile 中使用 RUN git clone 的情况
- 而我们现在的方案是在容器启动后（volume 已挂载）才执行 git clone
- 因此克隆的内容会直接写入到已挂载的 volume 中，不会被覆盖

### 对比两种方案

**❌ 错误方案**（会被覆盖）：
```dockerfile
FROM alpine:3.19
WORKDIR /articles-data
RUN git clone https://github.com/xxx/xxx.git .  # 在构建时克隆
```

**✅ 正确方案**（我们现在用的）：
```dockerfile
FROM alpine:3.19
WORKDIR /articles-data
COPY init.sh /usr/local/bin/
ENTRYPOINT ["/usr/local/bin/init.sh"]  # 在运行时克隆
```

```bash
# init.sh
if [ -z "$(ls -A $ARTICLES_DIR)" ]; then
    git clone ...  # volume 挂载后才执行
fi
```

### 验证

你可以通过以下步骤验证：

```bash
# 首次启动
docker-compose up -d

# 检查 volume 中的内容
docker-compose exec app ls -la /articles-data

# 停止并删除容器（但保留 volume）
docker-compose down

# 重新启动
docker-compose up -d

# 再次检查内容，应该还在
docker-compose exec app ls -la /articles-data
```

所以不用担心，init.sh 中的 git clone 操作不会被覆盖，因为它是在 volume 挂载完成后才执行的。这正是我们使用 init.sh 而不是直接在 Dockerfile 中克隆的原因之一。
