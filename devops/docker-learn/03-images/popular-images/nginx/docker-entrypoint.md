如果我们进入一个 nginx 就会在 `/` 目录下看到一个 docker-entrypoint.sh 

```shell
#!/bin/sh
# vim:sw=4:ts=4:et

set -e

entrypoint_log() {
    if [ -z "${NGINX_ENTRYPOINT_QUIET_LOGS:-}" ]; then
        echo "$@"
    fi
}

if [ "$1" = "nginx" ] || [ "$1" = "nginx-debug" ]; then
    if /usr/bin/find "/docker-entrypoint.d/" -mindepth 1 -maxdepth 1 -type f -print -quit 2>/dev/null | read v; then
        entrypoint_log "$0: /docker-entrypoint.d/ is not empty, will attempt to perform configuration"

        entrypoint_log "$0: Looking for shell scripts in /docker-entrypoint.d/"
        find "/docker-entrypoint.d/" -follow -type f -print | sort -V | while read -r f; do
            case "$f" in
                *.envsh)
                    if [ -x "$f" ]; then
                        entrypoint_log "$0: Sourcing $f";
                        . "$f"
                    else
                        # warn on shell scripts without exec bit
                        entrypoint_log "$0: Ignoring $f, not executable";
                    fi
                    ;;
                *.sh)
                    if [ -x "$f" ]; then
                        entrypoint_log "$0: Launching $f";
                        "$f"
                    else
                        # warn on shell scripts without exec bit
                        entrypoint_log "$0: Ignoring $f, not executable";
                    fi
                    ;;
                *) entrypoint_log "$0: Ignoring $f";;
            esac
        done

        entrypoint_log "$0: Configuration complete; ready for start up"
    else
        entrypoint_log "$0: No files found in /docker-entrypoint.d/, skipping configuration"
    fi
fi

exec "$@"
```

> [!tip]
>
> 其实 owasp/modsecurity-crs:nginx-alpine 也复用使用了这个 docker-entrypoint.sh



## 解释

```sh
#!/bin/sh
# vim:sw=4:ts=4:et

set -e
```

- `#!/bin/sh`：声明使用 `sh` 解释器执行。
- `set -e`：如果脚本中的任意命令执行失败（返回非 0），脚本就会立即退出。



```sh
entrypoint_log() {
    if [ -z "${NGINX_ENTRYPOINT_QUIET_LOGS:-}" ]; then
        echo "$@"
    fi
}
```

定义一个简单的函数，用于打印日志。它会检查 `NGINX_ENTRYPOINT_QUIET_LOGS` 环境变量，如果这个变量没有设置，就打印传入的日志信息。这允许用户通过设置这个环境变量来减少启动时的日志输出。



```sh
if [ "$1" = "nginx" ] || [ "$1" = "nginx-debug" ]; then
```

检查传递给脚本的第一个参数 (`$1`) 是否是 `nginx` 或 `nginx-debug`（这是启动 Nginx 服务器的命令）。

*   如果不是（例如，你运行 `docker run ... sh` 来获取一个 shell），那么整个 `if` 块内的配置逻辑就会被跳过。
*   如果是，则继续执行配置逻辑。



### 查找并执行 /docker-entrypoint.d/ 下的脚本文件

```sh
if /usr/bin/find "/docker-entrypoint.d/" -mindepth 1 -maxdepth 1 -type f -print -quit 2>/dev/null | read v; then
```

判断 `/docker-entrypoint.d/` 目录下是否存在文件。如果存在，则执行配置脚本。

然后遍历这些文件：

```sh
find "/docker-entrypoint.d/" -follow -type f -print | sort -V | while read -r f; do
```

遍历所有文件（按文件名自然排序 `sort -V`），对不同扩展名作不同处理。

处理逻辑如下：

*   `*.envsh`: 如果是 `.envsh` 文件并且可执行 (`-x "$f"`)，就 source 这个脚本 (`. "$f"`)。Source 会在当前 shell 环境中执行脚本的命令，通常用于设置环境变量。如果不可执行，则忽略。
*   `*.sh`: 如果是 `.sh` 文件并且**可执行** (`-x "$f"`)，就执行这个脚本 (`"$f"`)。执行会在一个子 shell 中运行脚本。如果不可执行，则忽略。
*   `*)`: 忽略其他任何类型的文件。

```sh
entrypoint_log "$0: Configuration complete; ready for start up"
```

所有脚本执行完后输出“配置完成”日志。





### 最后执行传入的命令

```sh
exec "$@"
```

`"$@"`: 代表传递给 `docker-entrypoint.sh` 脚本的所有参数（例如 `nginx -g 'daemon off;'`）。

`exec`: 这个 shell 命令会用后面的命令替换掉当前的 shell 进程。它不会创建新的进程。

当执行到这一行时，`docker-entrypoint.sh` 这个 shell 进程就结束了，取而代之的是 `$@` 所指定的命令进程（也就是 `nginx` 主进程）。这确保了 Nginx 进程成为容器的主进程 (PID 1)，能够正确接收 Docker 发送的信号（如 `docker stop` 发送的 SIGTERM）。



# docker-entrypoint.d

在这个目录下目前存在 4 个文件

```shell
/docker-entrypoint.d # tree
.
├── 10-listen-on-ipv6-by-default.sh
├── 15-local-resolvers.envsh
├── 20-envsubst-on-templates.sh
└── 30-tune-worker-processes.sh

0 directories, 4 files
```

