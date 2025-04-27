妈了个巴子，遇到一个问题，就是这个  owasp/modsecurity-crs:nginx-alpine 会有启动脚本来自动生成 nginx 相关的 config 文件，如果已经写入（比如说 bind mount）的话会报错

```shell
nginx-modsecurity  | /docker-entrypoint.d/20-envsubst-on-templates.sh: line 53: can't create /etc/nginx/conf.d/default.conf: Permission denied
nginx-modsecurity exited with code 1
```

或者如果 bind mount 了整个

```shell
nginx-modsecurity  | /docker-entrypoint.d/20-envsubst-on-templates.sh: line 53: can't create /etc/nginx/conf.d/logging.conf: Permission denied
nginx-modsecurity exited with code 1
```



# continue

[Nginx-Modsecurity Container St | Google AI Studio](https://aistudio.google.com/prompts/1VvZyI4CrM-HVHQnj1HnlTh6vVwem8D8b)