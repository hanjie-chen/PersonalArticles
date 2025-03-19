# Docker 存储空间管理

遇到这样子一个问题，有一天 ssh 登录我的 linux vm 发现，似乎没有多少存储空间了

```shell
  System load:  0.05               Processes:             140
  Usage of /:   74.0% of 28.89GB   Users logged in:       0
  Memory usage: 23%                IPv4 address for eth0: 10.0.2.4
  Swap usage:   0%
```

毕竟我用的是 Azure 默认的 Linux 30GB 的空间然后使用命令查了一下，结果发现是 docker 占用了很多的存储

```shell
Plain@Linux-VM:~/Personal_Project$ sudo du -sh /* 2>/dev/null | sort -hr
16G     /var
2.8G    /usr
1.7G    /opt
...

Plain@Linux-VM:~/Personal_Project$ sudo du -sh /var/* 2>/dev/null | sort -hr
12G     /var/lib
3.1G    /var/log
...

Plain@Linux-VM:~/Personal_Project$ sudo du -sh /var/lib/* 2>/dev/null | sort -hr
11G     /var/lib/docker
504M    /var/lib/snapd
...
```

然后我们查看 docker 全局存储使用

```bash
Plain@Linux-VM:~/Personal_Project$ docker system df
TYPE            TOTAL     ACTIVE    SIZE      RECLAIMABLE
Images          34        3         9.285GB   9.285GB (99%)
Containers      3         0         294.5kB   294.5kB (100%)
Local Volumes   4         1         650.5MB   443.8MB (68%)
Build Cache     140       0         509.9MB   509.9MB
```

输出字段说明：
- `TYPE`: 资源类型（Images/Containers/Local Volumes/Build Cache）
- `TOTAL`: 总数量
- `ACTIVE`: 正在使用的数量
- `SIZE`: 占用空间
- `RECLAIMABLE`: 可回收空间

结果发现是无用的 images 占据了大部分空间 所以我们需要及时清理掉

我们首先查看一下所有的 docker image

```shell
Plain@Linux-VM:~/Personal_Project$ docker images
REPOSITORY                         TAG        IMAGE ID       CREATED         SIZE
test-website-articles-sync         latest     be3d01bd99af   11 days ago     18.7MB
<none>                             <none>     c373d328d472   13 days ago     18.7MB
<none>                             <none>     7f9553060948   13 days ago     18.7MB
<none>                             <none>     7d98f24fd278   13 days ago     18.7MB
<none>                             <none>     40f182207227   2 weeks ago     18.7MB
<none>                             <none>     7b943abf5018   2 weeks ago     18.7MB
<none>                             <none>     ff4bc61d33ab   2 weeks ago     18.7MB
<none>                             <none>     197fa782730b   3 weeks ago     181MB
<none>                             <none>     85e30e533acf   3 weeks ago     181MB
<none>                             <none>     df206467c6a2   3 weeks ago     181MB
<none>                             <none>     cfd122ac2c9f   4 weeks ago     181MB
test-website-web-app               latest     a6b8f2921e54   4 weeks ago     166MB
<none>                             <none>     88312d28c368   4 weeks ago     961MB
<none>                             <none>     3a17a474ca70   4 weeks ago     18.7MB
test-website-articles-data         latest     8e2ab0c07488   4 weeks ago     18.7MB
my-website                         latest     4683b71bcaf9   6 weeks ago     1.17GB
<none>                             <none>     3de94fb68dd9   7 weeks ago     960MB
<none>                             <none>     d13e3db30839   7 weeks ago     975MB
<none>                             <none>     47b85b6b64fe   8 weeks ago     975MB
<none>                             <none>     337b7d9e28aa   8 weeks ago     975MB
<none>                             <none>     233b14a3e3d7   8 weeks ago     975MB
python                             3.9-slim   473b3636d11e   8 weeks ago     125MB
python                             latest     3ca4060004b1   8 weeks ago     1.02GB
<none>                             <none>     f4d246af4e89   2 months ago    182MB
getting-started-todo-app-client    latest     7a126d24d539   2 months ago    1.19GB
<none>                             <none>     a17cd65912e7   2 months ago    1.19GB
getting-started-todo-app-backend   latest     58ff7bba8548   2 months ago    1.17GB
traefik                            v2.11      8ea66c686b7b   3 months ago    173MB
mysql                              8.0        9f4b39935f20   3 months ago    590MB
ubuntu                             latest     59ab366372d5   3 months ago    78.1MB
alpine                             3.19       07c39c7bc641   4 months ago    7.39MB
docker/welcome-to-docker           latest     c1f619b6477e   14 months ago   18.5MB
phpmyadmin                         latest     e5b700ec0014   19 months ago   559MB
hello-world                        latest     d2c94e258dcb   21 months ago   13.3kB
```

可以发现存在大量的 `<none>` 镜像和很多的我们用不上的大体积镜像，例如 `getting-started-todo-app-client` 这种镜像，像这样子的镜像被称为悬空镜像（Dangling Images）

> [!note]
>
> 为什么会出现 `<none>` 镜像？
>
> 1. 构建镜像时的覆盖行为
>
> 当你多次用 相同标签 构建镜像时（例如 `docker build -t my-image:latest`），新构建的镜像会覆盖旧镜像的标签，旧镜像的 `REPOSITORY` 和 `TAG` 会变成 `<none>`。
>
> ```
> # 第一次构建（生成镜像 ID: abcd1234，标签为 my-image:latest）
> docker build -t my-image:latest .
> 
> # 第二次构建（新镜像 ID: 5678efgh，旧镜像 abcd1234 变成 <none>）
> docker build -t my-image:latest .
> ```
>
> #### 2. 未指定标签的构建
>
> 如果构建镜像时未指定标签（例如直接运行 `docker build .`），生成的镜像默认没有 `REPOSITORY` 和 `TAG`。
>
> #### 3. 依赖镜像层
>
> Docker 镜像采用分层存储，某些中间层可能未被正确清理，导致残留 `<none>` 镜像。

我们可以使用下面的命令清理资源

| 目标           | 命令                     | 说明                     |
| -------------- | ------------------------ | ------------------------ |
| 删除悬空镜像   | `docker image prune`     | 清理 `<none>` 标签的镜像 |
| 删除未使用卷   | `docker volume prune`    | 需确保卷无容器依赖       |
| 清理构建缓存   | `docker builder prune`   | 删除无效的构建缓存       |
| 清理停止的容器 | `docker container prune` | 删除所有已停止的容器     |



