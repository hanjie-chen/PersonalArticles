# mihomo-proxy

因为我在 windows 上使用 clash 作为 proxy，所以使用的是 clash 格式的订阅，所以在树莓派上面也打算使用兼容类似格式的代理。

在 gpt5 的推荐下，使用 mihomo 作为树莓派 ubuntu 的代理，并且开启全局模式。首先我们下载好 mihomo，然后做配置

# config.yml

其配置文件位于 /etc/mihomo/config.yml

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

  让 dns 查询也跟着 proxy 走，防止 dns 污染

## proxy group

专门给 openai url 配置 singpore 节点，其他的则是走自动选择

```shell
proxy-groups:
  - name: PROXY_AUTO
    type: url-test
    use:
      - sub
    url: http://www.gstatic.com/generate_204
    interval: 300
    tolerance: 100

  - name: OPENAI_SG
    type: select
    use:
      - sub
    filter: "(?i)singapore|新加坡|\\bsg\\b"
```

# openai

下面的命令可以用于测试是否可以联通 chatgpt，以及位置

```shell
curl -sS https://chatgpt.com/cdn-cgi/trace | egrep '^(ip=|loc=|colo=|http=)'
```

### 查看proxy-auto当前使用的节点

```shell
curl -s -H 'Authorization: Bearer 1236547' \
  http://127.0.0.1:9090/group/PROXY_AUTO \
| jq -r '.now'
```

### 查看 open-sg 使用的节点

```shell
curl -s -H 'Authorization: Bearer 1236547' \
  http://127.0.0.1:9090/group/OPENAI_SG \
| jq -r '.now'
```

测试延迟

```shell
name=$(curl -s -H 'Authorization: Bearer 1236547' \
  http://127.0.0.1:9090/group/OPENAI_SG | jq -r '.now')

enc=$(jq -rn --arg v "$name" '$v|@uri')

curl -s -G -H 'Authorization: Bearer 1236547' \
  --data-urlencode 'url=https://chatgpt.com/cdn-cgi/trace' \
  --data-urlencode 'timeout=8000' \
  "http://127.0.0.1:9090/proxies/$enc/delay"
```

# 重启 mihomo 

在修改完成配置文件之后，往往需要重启 mihomo: `sudo systemctl restart mihomo`
