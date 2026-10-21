# WAF

即 Web Application Firewall, 工作在 L7 (HTTP)，检查请求内容 (URL / headers / body)，区别于传统防火墙 (L3/L4, TCP/IP 层防火墙)。

WAF = engine + rule set
- engine: 负责拦截/解析 HTTP 请求，按规则匹配并执行动作 (block/log/pass)。比如 ModSecurity
- rule set: 定义"什么样的请求算攻击"，纯文本，不能独立运行。比如 OWASP CRS (Core Rule Set)

所以 GitHub 上 ModSecurity 和 CRS 是两个独立项目，由不同团队维护。

## OWASP 与 CRS

OWASP ( Open Worldwide Application Security Project ) 一个安全领域的非营利基金会：法律外壳是基金会（有资金、有全球分会），工作方式是开源社区（项目都在 GitHub 上，任何人可以提 issue / PR）。

不卖产品，产出全部免费 —— 所以 CRS 能被各家厂商随便拿去用。

名下两个最有名的产出：

- OWASP Top 10: "Web 应用十大安全风险"榜单，每几年更新一次，给人看的行业共识文档（面试、合规审计常见）
- OWASP CRS ( Core Rule Set ): 给 WAF engine 跑的检测规则集

两者有很大交集但互不包含：
- CRS 覆盖的攻击类型远多于 10 个：SQLi, XSS, RCE, LFI/RFI, 协议违规, 扫描器探测等，共几百条规则
- Top 10 里有些条目 CRS 管不了：如 Insecure Design、Vulnerable Components —— 这些是代码/架构层问题，WAF 在 HTTP 层看不出来

## Cloud WAF 与 Managed Rule

云厂商的 WAF 产品中常见 managed rule，"managed" 指运维责任归厂商（厂商负责引擎运行和规则更新，用户只做开关配置），和 managed database / managed kubernetes 的 "managed" 是同一个意思。

规则来源各家不同：Azure 直接采用 CRS，AWS 用自家私有规则，Cloudflare 两者并存。

例如在 Application Gateway WAF policy 里看到的 managed rule set（如 OWASP 3.2 / CRS 3.1），就是 CRS —— 微软直接拿来用了。

对比：

- 自建容器: nginx + ModSecurity + CRS → 自己装、自己配、自己升级
- Azure: Gateway + 微软自研引擎 + CRS → 微软负责引擎运行和规则更新，在 portal 上开关

需要注意的是，Azure 的引擎并不是 ModSecurity 本体，而是微软自己的实现，只是执行的规则逻辑来自 CRS；此外微软还在 CRS 之外加了自家规则（Bot protection、Azure-specific 规则组）。

## ModSecurity 与 WAF 容器

前文一直把 engine 当作一个整体，这里展开讲.

ModSecurity 不是独立运行的程序，而是一个库 (libmodsecurity)，自己不能监听端口、接收请求，必须依附于某个 web server 里工作。

这就是为什么有个容器叫 nginx-modsecurity 而不是拆成两个容器 —— 本来就不可分。

请求处理链条：

request → nginx → ModSecurity-nginx connector → libmodsecurity (引擎本体，检查请求) → 返回判定 → nginx access/deny

> [!note]
>
> 名字里的 "mod" 是 Apache 模块命名惯例 (如 mod_rewrite)，ModSecurity 最早就是 Apache 专属模块；v3 重写为独立库 libmodsecurity 后，才能通过 connector 接入 nginx 等其他 server。

比如说这个 image: owasp/modsecurity-crs:4-nginx-alpine（OWASP CRS 项目官方维护的镜像：nginx + connector + libmodsecurity + CRS 4.x 全部打包好）
