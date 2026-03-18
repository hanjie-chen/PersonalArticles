# mihomo-proxy

使用 mihomo 作为树莓派 ubuntu 的代理，并且开启全局模式

下面的命令可以用于测试是否可以联通 chatgpt，以及位置

```shell
curl -sS https://chatgpt.com/cdn-cgi/trace | egrep '^(ip=|loc=|colo=|http=)'
```



其中最重要的 config.yml 中关于 dns 的配置

```yaml
dns:
  enable: true
  prefer-h3: false
  listen: 127.0.0.1:1053
  ipv6: false
  enhanced-mode: redir-host
  respect-rules: true

  default-nameserver:
    - 1.1.1.1
    - 8.8.8.8

  proxy-server-nameserver:
    - 1.1.1.1
    - 8.8.8.8

  nameserver:
    - https://1.1.1.1/dns-query#RULES
    - https://8.8.8.8/dns-query#RULES

  fallback:
    - https://1.1.1.1/dns-query#RULES
    - https://8.8.8.8/dns-query#RULES

  fallback-filter:
    geoip: false
```

- respect-rules: true

  让 dns 查询也跟着 proxy 走
