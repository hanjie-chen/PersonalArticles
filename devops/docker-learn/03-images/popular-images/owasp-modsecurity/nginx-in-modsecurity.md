在 owasp/modsecurity 这个镜像中，存在 nginx 作为 reverse proxy 的镜像

需要注意的是和普通的 nginx 不一样

一般来说对于普通的 nginx contianer, 比如说 nginx-alpine, 我们一般直接把本地的 conf 文件复制或者挂载到  `/etc/nginx/conf.d/default.conf` 路径中

但是对于 owasp/modsecurity:nginx 来说，则是使用一种通过模板和环境变量自动生成配置的机制

在 readme 文件的这个部分有所提及：[coreruleset/modsecurity-crs-docker: Official ModSecurity Docker + Core Rule Set (CRS) images](https://github.com/coreruleset/modsecurity-crs-docker/?tab=readme-ov-file#nginx-based-images-breaking-change、)

> Nginx based images are now based on upstream nginx. This changed the way the config file for nginx is generated.

而如果这种方式（通过模板和环境变量自动生成配置）满足不了你的需要，你需要自定义 default.conf 的内容，然后不要将其直接挂载到 /etc/nginx/conf.d/default.conf，而应该：

1. 准备你的自定义配置文件：在你的宿主机上创建一个文件，包含你想要的 Nginx 配置（例如，在 ./nginx-modsecurity/conf.d/my-custom-default.conf）。
2. 将其挂载到 `template` 路径：在你的 compose.yaml 中，将这个自定义文件挂载到容器内对应的模板文件路径。对于 default.conf，对应的模板路径是 /etc/nginx/templates/conf.d/default.conf.template。

