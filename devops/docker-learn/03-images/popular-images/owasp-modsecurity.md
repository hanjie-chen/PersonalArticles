# OWASP modsecurity

因为在写自己的网站，并且想要省钱，所以只能自己去实现 waf

本来打算使用 `owasp/modsecurity:nginx-alpine` 但是当我去 docker hub 上面一看 [owasp/modsecurity - Docker Image | Docker Hub](https://hub.docker.com/r/owasp/modsecurity) 发现已经停止维护了

> This repository has been archived.
>
> We used to build `owasp/modsecurity-crs` via `owasp/modsecurity` (this repository), but it has become error prone and cumbersome. We have opted to merge the two repositories and will no longer build `owasp/modescurity`.

不过好在 `owasp/modsecurity-crs` 独立出来了 [owasp/modsecurity-crs - Docker Image | Docker Hub](https://hub.docker.com/r/owasp/modsecurity-crs) 可以使用这个 contianer 来代替