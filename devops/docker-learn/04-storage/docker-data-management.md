# Docker 数据管理的三种方式

**Volumes（数据卷）**

- Docker 管理的持久化数据
- 存储在 Docker 管理的区域（通常在 `/var/lib/docker/volumes/`）
- 最佳的数据持久化方式

**Bind Mounts（绑定挂载）**

**tmpfs mounts**

- 临时文件系统，数据存在内存中
- 容器停止后数据消失

# Volumes

让我们通过具体例子来说明如何使用 Volume 和环境变量：

#### 2.1 创建 Docker Volume

```bash
# 创建一个 volume
docker volume create articles-data

# 查看 volume 信息
docker volume ls
```

#### 2.2 修改 config.py

```python
import os

# 使用环境变量配置路径
Articles_Directory = os.getenv('ARTICLES_DIRECTORY', '/app/articles-data')
Rendered_Articles = "rendered_articles"
```

#### 2.3 创建 docker-compose.yml

```yaml
services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      # 使用命名卷
      - articles-data:/app/articles-data
      # 如果需要持久化 rendered_articles
      - rendered-articles:/app/rendered_articles
    environment:
      - ARTICLES_DIRECTORY=/app/articles-data
      - FLASK_APP=app.py
      - FLASK_DEBUG=1
    command: flask run --debug --host=0.0.0.0
  
  # 添加初始化服务
  init-data:
    image: my-website
    volumes:
      - articles-data:/app/articles-data
      - /home/Plain/Personal_Project/articles-data-test:/host-data:ro
	command: >
      sh -c "cp -r /host-data/* /app/articles-data/"

volumes:
  articles-data:  # 声明命名卷
  rendered-articles:
```

### 3. 使用方式

```bash
# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down

# 停止服务并删除卷
docker-compose down -v
```



### 5. 完整的开发环境配置

创建 `docker-compose.dev.yml`:

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      # 开发环境使用 bind mount
      - /home/Plain/Personal_Project/articles-data-test:/app/articles-data
      - ./rendered_articles:/app/rendered_articles
      # 如果需要实时修改代码，可以添加以下行
      - .:/app
    environment:
      - ARTICLES_DIRECTORY=/app/articles-data
      - FLASK_APP=app.py
      - FLASK_DEBUG=1
    command: flask run --debug --host=0.0.0.0
```

使用开发配置：
```bash
docker-compose -f docker-compose.dev.yml up -d
```

