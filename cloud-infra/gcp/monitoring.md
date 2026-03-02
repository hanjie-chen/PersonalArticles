# monitoring

首先我们要创建一个通知方式，以邮箱为例

Monitoring -> Alerting -> Edit notification channels -> Email -> Add new，

填邮箱并确认邮件。

## Uptime check

Uptime Check（运行状况检查）是一个从外部模拟用户访问的“探测器”。它会定期向服务发送请求，确认服务是否活着以及响应速度。

Uptime Check 会从全球多个指定的区域（如北美、欧洲、亚太等）发送 HTTP、HTTPS 或 TCP 请求。

- 多点监测：防止因为某个地区的网络波动导致误报。只有当多个地区的探测都失败时，才会触发真正的警报。
- 检查频率：可以设置每 1、5、10 或 15 分钟检查一次。

你可以监控部署在任何地方的服务，不仅限于 GCP 内部：

- URL/主机名：任何公开的网站或 API 接口。
- GCP 资源：App Engine、Compute Engine (VM)、Cloud Run 服务、以及 GKE 的 Load Balancer。
- 私有网络：通过配置 Private Uptime Checks，也可以监控 VPC 内部（非公开）的服务。

除了基本的连接成功，你还可以定义更严格的成功标准：

- 状态码匹配：默认 2xx 为成功，你也可以指定特定的状态码。
- 内容匹配 (Content Matching)：检查返回的 HTML 或 JSON 中是否包含（或不包含）特定的字符串。这非常有用，可以防止那种“网页能打开但内容报错”的尴尬情况。
- 超时设置：如果响应超过预设秒数，也视为失败。

### charge

每个月前 1M 免费

https://cloud.google.com/stackdriver/pricing#monitoring-pricing-summary

中指出： 1 million executions per Google Cloud project

