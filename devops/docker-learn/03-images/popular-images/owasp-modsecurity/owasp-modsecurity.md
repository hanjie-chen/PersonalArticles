# OWASP modsecurity

因为在写自己的网站，并且想要~~省钱~~，自己动手学习 waf 和 owasp crs，所以只能自己去实现 waf

本来打算使用 `owasp/modsecurity:nginx-alpine` 但是当我去 docker hub 上面一看 [owasp/modsecurity - Docker Image | Docker Hub](https://hub.docker.com/r/owasp/modsecurity) 发现已经停止维护了

> This repository has been archived.
>
> We used to build `owasp/modsecurity-crs` via `owasp/modsecurity` (this repository), but it has become error prone and cumbersome. We have opted to merge the two repositories and will no longer build `owasp/modescurity`.

不过好在 `owasp/modsecurity-crs` 独立出来了 [owasp/modsecurity-crs - Docker Image | Docker Hub](https://hub.docker.com/r/owasp/modsecurity-crs) 可以使用这个 contianer 来代替



## modsecurity-crs tag

modsecurity-crs image 的 tag 组成是

```
<CRS version>-<web server>-<date>
```



### `CRS version`

```
<major>.<minor>.<patch>
```

其中 `<major>` `<minor>` `<patch>` 3者都可以省略，例如 `4.12.0`, `4.12`, `4`, `none` 都是可以的

*   `4.12.0`: 特定的补丁版本。最稳定，但可能稍微落后于小版本更新。
*   `4.12`: 指向 `4.12.x` 小版本系列中的最新构建。稳定性与新功能之间的良好平衡。
*   `4`: 指向 `4.x.x` 大版本系列中的最新构建。更新更频繁，可能包括小版本升级。
*   `none`: 只想

### `web server`

```
<web server>-<os>
```

其中 `<os>` 为可选，例如指定 web server 例如 `nginx` 或者 `nginx-alpine`

如果添加了 `-alpine` 则说明使用了 alpine linux 构建，如果不加那么使用默认的 debian 构建

### `date`

```
<YYYY>-<MM>-<DD>-<HH>-<MM>
```

例如 `202503230103`

## health check

在 [coreruleset/modsecurity-crs-docker: Official ModSecurity Docker + Core Rule Set (CRS) images](https://github.com/coreruleset/modsecurity-crs-docker) 上面提到，这个 image 存在一个 healthcheck

> We add healthchecks to the images, so that containers return HTTP status code 200 from the `/healthz` endpoint. When a container has a healthcheck specified, it has a *health status* in addition to its normal status. This status is initially `starting`. Whenever a health check passes, it becomes `healthy` (whatever state it was previously in). After a certain number of consecutive failures, it becomes `unhealthy`. See https://docs.docker.com/engine/reference/builder/#healthcheck for more information.

# OWASP CRS

[CRS Documentation](https://coreruleset.org/docs/) OWASP CRS 文档，有空仔细看看



# Environment variable

在 owasp/modsecurity-crs 镜像中，ModSecurity 和 OWASP CRS 的配置可以通过环境变量进行调整。这些环境变量在容器启动时会被用来动态生成或修改 Nginx 和 ModSecurity 的配置文件。

同时，你也可以通过挂载自定义的 .conf 文件（例如 Nginx 或 ModSecurity 的配置文件）来覆盖默认配置或进行更细粒度的调整。这两种方式并不冲突：

- **环境变量**：适合快速配置，尤其在容器化环境中。
- **.conf 文件**：适合需要复杂或定制化配置的场景。

镜像的入口脚本（entrypoint）会根据环境变量生成配置文件，因此环境变量实际上是一种简化和自动化的配置方式。

这个镜像根据的 tag(web server) 不同存在多类的环境变量

## Common ENV Varialbes

适用于所有镜像变体的通用环境变量。无论底层使用的 Web 服务器是 Apache、Nginx 还是 Openresty，这些变量都可以被识别和使用。



## Apache/Nginx/Openresty ENV Varialbes

针对 Apache/Nginx/Openresty Web Server 生效的环境变量，只在基于 Apache/Nginx/Openresty 的镜像（owasp/modsecurity-crs: apache/nginx/openresty）中生效，用于配置特定的功能



## ModSecurity ENV Varialbes

是专门用于配置 ModSecurity 引擎的环境变量，其实也是算一种 common environment variables 这些环境变量直接控制 ModSecurity 引擎的行为，影响它如何解析和过滤 HTTP 流量。

#### 与 Common ENV Variables 的对比

- **Common ENV Variables**：主要用于配置 Web 服务器的通用行为，例如日志路径（如 Apache 的访问日志）、后端代理地址或 SSL 证书路径。这些变量的生效范围也是全局的，但它们针对的是 Web 服务器本身，而不是 ModSecurity。
- **ModSecurity ENV Variables**：专注于 ModSecurity 引擎的配置，与 Web 服务器的具体类型无关。它们的全局性体现在所有支持 ModSecurity 的镜像中都有效。

### Import variable

` MODSEC_RULE_ENGINE` 是否启用 modsecurity rule 可选 `On` `Off` `DetectionOnly` 默认值是 `On`

`MODSEC_REQ_BODY_ACCESS` 是否检查 request body 可选 `On` `Off` 默认值 `On`

`MODSEC_RESP_BODY_ACCESS` 是否检查 response body 可选 `On` `Off` 默认值 `On`

`MODSEC_AUDIT_LOG` 审计 log 存储路径 默认 `/dev/stdout`

## CRS Specific ENV Varialbes

CRS Specific 环境变量是专门用于配置 OWASP Core Rule Set (CRS) 的环境变量，这些变量允许用户根据自己的应用需求调整 CRS 规则集的行为，和 ModSecurity ENV Variables 一样同样也是全局生效的

通过这些变量，用户可以微调 CRS 的防护策略，使其更适应特定的业务场景。

### Import Variable

`BLOCKING_PARANOIA` 设置 CRS 的偏执级别（Paranoia Level），控制规则严格程度。默认值 `1`

`ANOMALY_INBOUND` 设置入站请求异常得分阈值，超过时触发拦截。默认值 `5`

`ALLOWED_METHODS` 指定允许的 HTTP 方法。默认值 `GET` `HEAD` `POST` `OPTIONS`

`MAX_FILE_SIZE` 限制上传文件的大小。默认值 `unlimited`

# Config file

ModSecurity 是独立于 Nginx 的模块，它的配置方式与 Nginx 的 `default.conf` 有所不同。以下是配置 ModSecurity 的两种主要方法：

#### **方法 1：通过环境变量**
在 `compose.yml` 中，你已经使用了环境变量 `MODSEC_AUDIT_LOG` 来指定日志路径。OWASP ModSecurity CRS 镜像支持许多环境变量，可以用来调整 ModSecurity 和 CRS 的行为。这些变量在容器启动时会被入口脚本读取并应用。常用变量包括：
- `MODSEC_RULE_ENGINE=on`：启用 ModSecurity 规则引擎（默认启用）。
- `BLOCKING_PARANOIA=1`：设置 CRS 的拦截偏执级别（1-4，值越高越严格）。
- `DETECTION_PARANOIA=1`：设置检测偏执级别。
- `ALLOWED_METHODS=GET POST`：限制允许的 HTTP 方法。

**示例**：
```yaml
environment:
  - MODSEC_AUDIT_LOG=/var/log/nginx/modsec-audit.log
  - BLOCKING_PARANOIA=1
  - DETECTION_PARANOIA=1
  - ALLOWED_METHODS=GET POST
```
