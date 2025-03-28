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



## `CRS version`

格式为

```
<major>.<minor>.<patch>
```

其中 `<major>` `<minor>` `<patch>` 3者都可以省略，例如 `4.12.0`, `4.12`, `4`, `none` 都是可以的

*   `4.12.0`: 特定的补丁版本。最稳定，但可能稍微落后于小版本更新。
*   `4.12`: 指向 `4.12.x` 小版本系列中的最新构建。稳定性与新功能之间的良好平衡。
*   `4`: 指向 `4.x.x` 大版本系列中的最新构建。更新更频繁，可能包括小版本升级。
*   `none`: 只想

## `web server`

格式为

```
<web server>-<os>
```

其中 `<os>` 为可选，例如指定 web server 例如 `nginx` 或者 `nginx-alpine`

如果添加了 `-alpine` 则说明使用了 alpine linux 构建，如果不加那么使用默认的 debian 构建

## `date`

格式为

```
YYYYMMDDHHMM
```

例如 `202503230103`