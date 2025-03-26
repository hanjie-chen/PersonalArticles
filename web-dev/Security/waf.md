# what is OWASP?

Open Web Application Security Project（开放 Web 应用安全项目）。

OWASP 是一个全球性的非营利组织，致力于提高软件安全性。它由志愿者社区驱动，提供免费的工具、文档和资源，帮助开发者和安全从业者构建更安全的应用程序。

通过开放的方式分享安全知识，减少 Web 应用的漏洞。

#### 著名贡献
- **OWASP Top 10**：列出了 Web 应用中最常见的十大安全风险（如 SQL 注入、跨站脚本攻击 XSS 等），是学习 Web 安全的入门指南。
- **工具和项目**：如 OWASP ZAP（漏洞扫描工具）、OWASP Dependency-Check（依赖检查工具）等。
- **OWASP CRS**：即 Core Rule Set（核心规则集），是与 WAF（如 ModSecurity）配套使用的规则集。





## OWASP CRS（Core Rule Set）
OWASP CRS 是一组预定义的规则集，用于 Web 应用防火墙（WAF），旨在检测和阻止常见的 Web 攻击。

for example:
```
SecRule ARGS "@rx (?i)union.*select" "id:942100,phase:2,block,msg:'SQL Injection Attempt'"
```
这条规则检测 URL 参数中是否包含类似 `union select` 的 SQL 注入模式，如果检测到则拦截请求。



# ModSecurity

是一个 WAF 引擎，负责解析 HTTP 请求、执行规则并决定是否拦截。本身并不包含具体规则，仅提供执行框架。

OWASP CRS：是为 ModSecurity（以及其他支持类似规则的 WAF）设计的规则集，相当于 ModSecurity 的“知识库”。

ModSecurity 是“执行者”，OWASP CRS 是“规则库”。两者结合使用时，ModSecurity 加载 CRS 规则，实时检查流量并阻止恶意请求。

