# Background

本来我使用 nginx:alpine image 作为我的反向代理，但是处于安全考虑，我打算加一个 waf，最终选择 owasp/modsecurity-crs:nginx-alpine 因为它同时兼具 nginx + waf 的功能

但是我的开发环境之前使用 bind mount 来将本地的 conf.d 目录中的 default.conf 文件之际映射到 nginx container 中的 `/etc/nginx/conf.d/` 路径中去，但是当我转换为使用 owasp/modsecurity-crs:nginx-alpine 的时候，发现会有如下的报错

```shell
nginx-modsecurity  | /docker-entrypoint.d/20-envsubst-on-templates.sh: line 53: can't create /etc/nginx/conf.d/logging.conf: Permission denied
nginx-modsecurity exited with code 1
```

就算我只 bind mount 一个 default.conf 文件，也报错

```shell
nginx-modsecurity  | /docker-entrypoint.d/20-envsubst-on-templates.sh: line 53: can't create /etc/nginx/conf.d/default.conf: Permission denied
nginx-modsecurity exited with code 1
```

这我没办法了，只能去 [github](https://github.com/coreruleset/modsecurity-crs-docker) 把 Readme 和源代码都看一遍了



# Readme part

在 Readme 中的 `Nginx based images breaking change` 这个部分提到

> Nginx based images are now based on upstream nginx. This changed the way the config file for nginx is generated.

但是对于 owasp/modsecurity:nginx 来说，则是使用一种通过模板和环境变量自动生成配置的机制

而如果这种方式（通过模板和环境变量自动生成配置）满足不了你的需要，你需要自定义 default.conf 的内容，然后不要将其直接挂载到 /etc/nginx/conf.d/default.conf，而应该：

1. 准备你的自定义配置文件：在你的宿主机上创建一个文件，包含你想要的 Nginx 配置（例如，在 ./nginx-modsecurity/conf.d/my-custom-default.conf）。
2. 将其挂载到 `template` 路径：在你的 compose.yaml 中，将这个自定义文件挂载到容器内对应的模板文件路径。对于 default.conf，对应的模板路径是 /etc/nginx/templates/conf.d/default.conf.template。



# source code part

我们查看项目源代码，可以发现

```shell
modsecurity-crs-docker$ tree -L 2
.
├── LICENSE
├── README-containers.md
├── README.md
├── REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf
├── RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf
├── apache
│   ├── Dockerfile
│   ├── Dockerfile-alpine
│   ├── conf
│   └── docker-entrypoint.sh
├── docker-bake.hcl
├── docker-compose.yaml
├── nginx
│   ├── Dockerfile
│   ├── Dockerfile-alpine
│   ├── docker-entrypoint.d
│   └── templates
├── renovate.json
└── src
    ├── bin
    ├── etc
    └── opt

10 directories, 13 files
```

让我们先 focus on `nginx/` 这个目录（因为我目前用的就是 nginx-alpine）

首先发现存在 2 个 dockerfile: `Dockerfile`, `Dockerfile-alpine` 分别用于构建基于 nginx 和 nginx-alpine 的 image

```shell
/modsecurity-crs-docker/nginx$ tree -L 1
.
├── Dockerfile
├── Dockerfile-alpine
├── docker-entrypoint.d
└── templates

3 directories, 2 files
```

需要注意的是和普通的 nginx 不一样

一般来说对于普通的 nginx contianer, 比如说 nginx-alpine, 我们一般直接把本地的 conf 文件复制或者挂载到  `/etc/nginx/conf.d/default.conf` 路径中





# nginx in  modsecurity

首先我们来看到 modsecurity-crs-docker 的 nginx 目录下

```shell
/modsecurity-crs-docker/nginx$ tree -L 2
.
├── Dockerfile
├── Dockerfile-alpine
├── docker-entrypoint.d
│   ├── 0-move-writables.sh
│   ├── 01-check-low-port.sh
│   ├── 10-generate-certificate.sh
│   ├── 90-copy-modsecurity-config.sh
│   ├── 91-update-resolver.sh
│   ├── 92-update-real_ip.sh
│   └── 93-update-proxy-ssl-config.sh
└── templates
    ├── conf.d
    ├── includes
    ├── modsecurity.d
    └── nginx.conf.template

6 directories, 10 files
```

好的，我们来结合 README 和这个目录结构，逐一解释 `nginx` 目录下第一层的文件和目录：

## `Dockerfile`

用于构建标准版（非 Alpine Nginx） `owasp/modsecurity-crs:nginx` 镜像的 Dockerfile。

## `Dockerfile-alpine`

用于构建 Alpine Linux 版 `owasp/modsecurity-crs:nginx-alpine` 镜像的 Dockerfile

## `docker-entrypoint.d` 

这个目录包含一系列 Shell 脚本，这些脚本会在容器启动时，在 Nginx 主进程运行之前，由主入口点脚本 (`docker-entrypoint.sh`，虽然它不直接在这个目录下，但会调用这里的脚本) 按**数字顺序**依次执行。

依据 (README 和之前的错误日志): 之前的错误日志明确显示了这些脚本（如 `01-check-low-port.sh`, `10-generate-certificate.sh`）的执行过程。README 提到了基于环境变量的配置生成，这个目录下的脚本（特别是像 `91-update-resolver.sh`, `92-update-real_ip.sh` 等，以及那个未列出但实际存在的 `20-envsubst-on-templates.sh`）负责实现这一功能。`0-move-writables.sh` 可能与 README 中提到的 "Read-only Root Filesystem" 变体有关，用于在只读文件系统中处理需要写入的目录。

*   **简述**: 容器启动时的**初始化脚本**目录。负责检查环境、生成临时配置（如自签名证书）、根据环境变量修改配置模板、设置权限等预备工作。





## `templates`

*   **作用**: 这个目录存放着 Nginx（以及可能相关的 ModSecurity）配置文件的**模板**。
*   **依据 (README 和之前的讨论)**: README 中明确提到：
    
    > *"What happens if I want to make changes in a different file, like `/etc/nginx/conf.d/default.conf`? You mount your local file, e.g. `nginx/default.conf` as the new template: `/etc/nginx/templates/conf.d/default.conf.template`."*
    > 这直接说明了这个目录的用途。入口点脚本（特别是 `20-envsubst-on-templates.sh`）会读取这个目录下的文件（通常是 `.template` 文件，但也可能是普通 `.conf` 文件被当作模板处理），使用环境变量替换其中的占位符（例如 `${PORT}`, `${BACKEND}` 等），然后将处理后的**最终配置文件**输出到容器内实际生效的配置路径（如 `/etc/nginx/nginx.conf`, `/etc/nginx/conf.d/`, `/etc/nginx/modsecurity.d/`）。
*   **包含**:
    *   `nginx.conf.template`: 主 Nginx 配置文件 (`nginx.conf`) 的模板。
    *   `conf.d` (子目录): 存放将被放置在 `/etc/nginx/conf.d/` 目录下的配置文件的模板（例如 `default.conf.template`）。这里通常定义 `server` 块。
    *   `modsecurity.d` (子目录): 存放 ModSecurity 相关配置的模板。
    *   `includes` (子目录): 可能包含一些被其他配置文件 `include` 的通用配置片段模板（如 SSL 配置、安全头部等）。
*   **简述**: Nginx 配置文件的**蓝本/模板**存放地。容器启动时会基于这些模板和环境变量生成最终的配置文件。

总的来说，`nginx` 目录包含了构建和运行 Nginx + ModSecurity 容器所需的核心文件：两个不同基础系统（标准版和 Alpine 版）的 `Dockerfile`，用于启动时初始化的 `docker-entrypoint.d` 脚本，以及用于动态生成配置的 `templates` 目录。



# successful running log

最后，当运行成功的时候，就可以看到这样子的log

```shell
nginx-modsecurity  | /docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
nginx-modsecurity  | /docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
nginx-modsecurity  | /docker-entrypoint.sh: Launching /docker-entrypoint.d/01-check-low-port.sh
nginx-modsecurity  | /docker-entrypoint.sh: Launching /docker-entrypoint.d/10-generate-certificate.sh
nginx-modsecurity  | /usr/local/bin/generate-certificate: generating new certificate
nginx-modsecurity  | Warning: Not placing -key in cert or request since request is used
nginx-modsecurity  | Warning: No -copy_extensions given; ignoring any extensions in the request
nginx-modsecurity  | /usr/local/bin/generate-certificate: generated /etc/nginx/conf/server.key and /etc/nginx/conf/server.crt
nginx-modsecurity  | /docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
nginx-modsecurity  | 10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
nginx-modsecurity  | 10-listen-on-ipv6-by-default.sh: info: /etc/nginx/conf.d/default.conf differs from the packaged version
nginx-modsecurity  | /docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
nginx-modsecurity  | /docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
nginx-modsecurity  | 20-envsubst-on-templates.sh: Running envsubst on /etc/nginx/templates/modsecurity.d/modsecurity.conf.template to /etc/nginx/modsecurity.d/modsecurity.conf
nginx-modsecurity  | 20-envsubst-on-templates.sh: Running envsubst on /etc/nginx/templates/modsecurity.d/modsecurity-override.conf.template to /etc/nginx/modsecurity.d/modsecurity-override.conf
nginx-modsecurity  | 20-envsubst-on-templates.sh: Running envsubst on /etc/nginx/templates/modsecurity.d/setup.conf.template to /etc/nginx/modsecurity.d/setup.conf
nginx-modsecurity  | 20-envsubst-on-templates.sh: Running envsubst on /etc/nginx/templates/conf.d/logging.conf.template to /etc/nginx/conf.d/logging.conf
nginx-modsecurity  | 20-envsubst-on-templates.sh: Running envsubst on /etc/nginx/templates/conf.d/modsecurity.conf.template to /etc/nginx/conf.d/modsecurity.conf
nginx-modsecurity  | 20-envsubst-on-templates.sh: Running envsubst on /etc/nginx/templates/conf.d/default.conf.template to /etc/nginx/conf.d/default.conf
nginx-modsecurity  | 20-envsubst-on-templates.sh: Running envsubst on /etc/nginx/templates/includes/cors.conf.template to /etc/nginx/includes/cors.conf
nginx-modsecurity  | 20-envsubst-on-templates.sh: Running envsubst on /etc/nginx/templates/includes/proxy_backend_ssl.conf.template to /etc/nginx/includes/proxy_backend_ssl.conf
nginx-modsecurity  | 20-envsubst-on-templates.sh: Running envsubst on /etc/nginx/templates/includes/location_common.conf.template to /etc/nginx/includes/location_common.conf
nginx-modsecurity  | 20-envsubst-on-templates.sh: Running envsubst on /etc/nginx/templates/includes/proxy_backend.conf.template to /etc/nginx/includes/proxy_backend.conf
nginx-modsecurity  | 20-envsubst-on-templates.sh: Running envsubst on /etc/nginx/templates/nginx.conf.template to /etc/nginx/nginx.conf
nginx-modsecurity  | /docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
nginx-modsecurity  | /docker-entrypoint.sh: Launching /docker-entrypoint.d/90-copy-modsecurity-config.sh
nginx-modsecurity  | /docker-entrypoint.sh: Launching /docker-entrypoint.d/91-update-resolver.sh
nginx-modsecurity  | /docker-entrypoint.sh: Launching /docker-entrypoint.d/92-update-real_ip.sh
nginx-modsecurity  | /docker-entrypoint.sh: Launching /docker-entrypoint.d/93-update-proxy-ssl-config.sh
nginx-modsecurity  | /docker-entrypoint.sh: Launching /docker-entrypoint.d/94-activate-plugins.sh
nginx-modsecurity  | # # #
nginx-modsecurity  | Running CRS plugin activation
nginx-modsecurity  | - - -
nginx-modsecurity  | 
nginx-modsecurity  | - - -
nginx-modsecurity  | Finished CRS plugin activation
nginx-modsecurity  | # # #
nginx-modsecurity  | 
nginx-modsecurity  | /docker-entrypoint.sh: Launching /docker-entrypoint.d/95-configure-rules.sh
nginx-modsecurity  | # # #
nginx-modsecurity  | Running CRS rule configuration
nginx-modsecurity  | - - -
nginx-modsecurity  | Configuring 900000 for BLOCKING_PARANOIA with blocking_paranoia_level=1
nginx-modsecurity  | Configuring 900110 for ANOMALY_INBOUND with inbound_anomaly_score_threshold=5
nginx-modsecurity  | Configuring 900110 for ANOMALY_OUTBOUND with outbound_anomaly_score_threshold=4
nginx-modsecurity  | - - -
nginx-modsecurity  | Finished CRS rule configuration
nginx-modsecurity  | # # #
nginx-modsecurity  | 
nginx-modsecurity  | /docker-entrypoint.sh: Ignoring /docker-entrypoint.d/configure-rules.conf
nginx-modsecurity  | /docker-entrypoint.sh: Configuration complete; ready for start up
```

