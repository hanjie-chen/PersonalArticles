# Docker Volume 详解

## 什么是 Docker Volume？
Docker Volume 是 Docker 提供的数据持久化方案，它是一个可以让容器存储数据的独立空间。想象成是一个"虚拟硬盘"，可以被一个或多个容器挂载和使用。



## Volume 的使用方式

创建并查看 volume

```bash
# 创建 volume
docker volume create articles-data

# 查看所有 volume
docker volume ls

# 查看 volume 详细信息
docker volume inspect articles-data
```

在 compose.yml 中使用 volume

```yaml
# 使用 compose.yml
services:
  web:
    image: my-website
    volumes:
      - test-data:/app/data

volumes:
  test-data:
    external: True
    name: articles-data
```



# docker volume command

## `docker volume create volume-name` 

for example

```bash
docker volume create articles-data
```

- 创建了一个名为 `articles-data` 的 volume
- 在 Docker 的存储区域（通常在 `/var/lib/docker/volumes/`）创建了一个目录
- 这个 volume 可以被任何容器挂载使用

## 其他常用命令

```bash
# 列出所有 volume
docker volume ls

# 查看 volume 详情
docker volume inspect articles-data

# 删除 volume
docker volume rm articles-data

# 删除所有未使用的 volume
docker volume prune
```



# volume –> `compose.yml` 

for example

```yaml
services:
  wordpress:
    image: wordpress
    volumes:
      - wp-content:/var/www/html/wp-content  # 使用 volume
      - ./themes:/var/www/html/wp-content/themes  # 绑定挂载
  
  mysql:
    image: mysql
    volumes:
      - db-data:/var/lib/mysql  # 使用相同方式声明的 volume

volumes:  # 顶级声明
  wp-content:    # 声明 WordPress 内容 volume
    name: my-wp-content  # 可选：指定 volume 名称
  db-data:       # 声明数据库 volume
    driver: local # 可选：指定 volume 驱动
```



## services level `volumes`

```yaml
volumes:
  - my-volume:/app/data
```

这个语法的格式是：`[volume name]:[容器内的挂载路径]`

- `my-volume` 是 Docker volume 的名称
- `/app/data` 是容器内部的挂载点路径

> [!note]
>
> 这会在容器中创建一个挂载点，指向 volume 的实际存储位置，而不是将数据拷贝到容器中，类似于 Linux 中的挂载点概念
>
> 如果 `/app/data` 路径在容器中不存在，Docker 会自动创建，这个路径可以是任意有效的路径，不必预先存在



## top level `volumes`

> [!note]
>
> 如果仅在 services 层级配置 volumes，而未在 top-level 配置 volumes，Docker 会使用容器引擎的默认配置来创建命名卷，默认配置包括：使用默认存储驱动、无特殊标签、卷名格式为 `项目名称_卷名`
>
> 执行 `docker compose up` 时，如果卷不存在则自动创建，当容器停止（`docker compose down`）时，卷会持久保留。只有执行 `docker compose down -v` or `docker volume rm` 才会删除卷

reference: [Volumes top-level element | Docker Docs](https://docs.docker.com/reference/compose-file/volumes/)

### `external` & `name`

external 属性用于分辨这个 volume 是否之前已经创建过，如果设置为 true 那么会使用已经创建的 volume，如果这个 volume 不存在则会报错

for example:

```yaml
volumes:
  db-data:
    external: true
    name: "actual-name-of-volume"  # 指定外部已存在的卷的实际名称
```

> [!note]
>
> 当一个卷被标记为 `external: true` 时，这个特定卷的配置中只能再添加 `name` 属性，而不能再添加其他的属性。如果 Compose 检测到任何其他属性，它会将 Compose 文件视为无效并拒绝执行。
>
> 这个限制的原因是：当声明一个卷为 `external` 时，意味着这个卷是在 Compose 项目之外管理的，因此 Compose 不应该尝试配置或修改它的任何属性，它只需要知道卷的名称即可。

### `driver` & `driver_opts`

driver 是存储驱动程序，决定了 Docker 如何在主机上存储和管理卷数据，不同的 driver 提供不同的存储功能和特性

for example

```yaml
volumes:
  db-data:
    driver: local    # 默认的驱动程序，数据存储在本地主机
```

其他常用 drivers：
- `nfs`: 网络文件系统
- `azure-file`: Azure 文件存储
- `aws-efs`: AWS 弹性文件系统

***

`driver_opts` 是用来为卷驱动程序（volume driver）提供特定选项的配置项。这些选项的具体参数取决于你使用的驱动程序类型。

例如 NFS 卷配置

```yaml
volumes:
  nfs-data:
    driver: local
    driver_opts:
      type: "nfs"
      o: "addr=10.40.0.199,nolock,soft,rw"  # NFS 选项
      device: ":/docker/example"             # NFS 共享路径
```

### `name`

除了与 external: true 一起使用，name 还可以独立使用

```yaml
volumes:
  db-data:
    name: "custom-volume-name"  # 为新创建的卷指定自定义名称
```
这种情况下，`name` 用来为新创建的卷指定一个自定义名称，而不是使用默认的命名规则。

如果不指定 `name`，Docker Compose 会使用以下格式自动生成卷名：
```
{项目名称}_{卷名}
```

例如

```yaml
# 项目名为 myapp
volumes:
  db-data: {}  # 最终卷名将是 myapp_db-data
```
