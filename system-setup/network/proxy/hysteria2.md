当出现这样子的报错的，

```
connect error: http3: parsing frame failed: timeout: no recent network activity
```

然后断连，这其实是因为端口被封了

[connect error: http3: parsing frame failed: timeout: no recent network activity · Issue #1095 · apernet/hysteria](https://github.com/apernet/hysteria/issues/1095)

大概是这个问题，考虑 client 使用端口跳跃，然后 server 配置 port nat 

[端口跳跃 - Hysteria 2](https://v2.hysteria.network/zh/docs/advanced/Port-Hopping/)