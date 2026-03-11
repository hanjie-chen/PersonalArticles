# mihomo-proxy

使用 mihomo 作为树莓派 ubuntu 的代理，并且开启全局模式

测试是否可以联通 chatgpt，以及位置

```shell
$ curl -sS https://chatgpt.com/cdn-cgi/trace | egrep '^(ip=|loc=|colo=|http=)'
ip=82.153.135.176
colo=SIN
http=http/2
loc=SG
```

