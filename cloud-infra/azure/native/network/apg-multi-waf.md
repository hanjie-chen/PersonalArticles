等我的网站好了之后，做一个实验关于 APG multiple waf 的实验

一个 waf-01 绑在一整个 APG 上面，然后一个 waf-02 绑在这个 APG 的一个 listener-01 上面，请问是那个 waf 会生效呢？还是都会生效呢？

todo:

需要在 waf-01, waf-02 上面设计特殊的 rule, 使得 3 种情况分别出现特殊的显示：

1. 只有 waf-01 生效
2. 只有 waf-02 生效
3. waf-01, waf-02 同时生效

其实关于这方面的一篇 Microsoft document

[Azure Web Application Firewall (WAF) policy overview | Microsoft Learn](https://learn.microsoft.com/en-us/azure/web-application-firewall/ag/policy-overview#global-waf-policy)

文中提到

> Say your application gateway has a global policy applied to it. Then you apply a different policy to a listener on that application gateway. The listener's policy now takes effect for just that listener. The application gateway’s global policy still applies to all other listeners and path-based rules that don't have a specific policy assigned to them.

看上去应该是 waf-02 生效，需要设计一个实验验证