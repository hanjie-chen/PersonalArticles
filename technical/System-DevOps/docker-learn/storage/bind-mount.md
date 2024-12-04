# 绑定挂载（Bind Mount）详解

```yaml
services:
  wordpress:
    volumes:
      - ./themes:/var/www/html/wp-content/themes  # 绑定挂载
```

这行代码是一个绑定挂载（Bind Mount），它的格式是：`[主机路径]:[容器路径]`

- **`./themes`**: 表示主机（你的电脑）上的路径
  - `.` 表示当前目录（docker-compose.yml 所在的目录）
  - `./themes` 就是当前目录下的 themes 文件夹

- **`/var/www/html/wp-content/themes`**: 容器内的路径

## 绑定挂载的常见用例

### 1. 开发环境
```yaml
services:
  node-app:
    volumes:
      - ./src:/app/src  # 源代码目录
      - ./package.json:/app/package.json  # 项目配置文件
```

### 2. 配置文件
```yaml
services:
  nginx:
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf  # 配置文件
      - ./html:/usr/share/nginx/html        # 静态文件
```
