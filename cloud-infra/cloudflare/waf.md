# cloudflare waf

[WAF Managed Rules · Cloudflare Web Application Firewall (WAF) docs](https://developers.cloudflare.com/waf/managed-rules/)

这篇文章中提到了就算是 free plan 的用户，也会有一个基础的 waf 防护，所以可以稍微依靠一下，然后我在后端使用一个 nginx 上面挂载一个 owasp 全面的waf 来进一步保证安全性。

但是我没有找到关于 cloudflare free managed ruleset 的具体内容，以后可以找找看