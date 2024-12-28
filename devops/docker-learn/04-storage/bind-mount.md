# Bind Mount

绑定挂载（Bind Mount）可以直接将主机的文件或目录挂载到容器中，可以在任何位置存储，适合开发环境

e.g.

```yaml
services:
  wordpress:
    volumes:
      - ./themes:/var/www/html/wp-content/themes  # 绑定挂载
```

语法格式为 `[host-path]:[container-path]`

`./themes`: 表示主机（你的电脑）上的路径

- `.` 表示当前目录（docker-compose.yml 所在的目录）
- `./themes` 就是当前目录下的 themes 文件夹

`/var/www/html/wp-content/themes`: 容器内的路径



