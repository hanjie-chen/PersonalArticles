# Anthropic API on Azure Marketplace

## Azure marketplace

简单说就是微软的云端应用商店。第三方软件厂商（ISV）可以把自己的产品上架到这里，Azure 用户直接在里面购买和部署，费用统一走 Azure 账单。

里面有 SaaS 应用、虚拟机镜像、容器、开发工具、AI 服务等数千种产品，微软对每笔交易收取 3% 的服务费，企业可以设置 Private Marketplace 来管控员工能买哪些产品

例如，Anthropic 的 Claude 就是以第三方 Marketplace 商品的形式在上面销售的。

## anthropic api

Claude 模型跑在 Anthropic 自己的基础设施上，Azure 只是一个"门面"。

> 根据 Anthropic 官方文档明确说的：
>
> "In this preview platform integration, Claude models run on Anthropic's infrastructure."

Anthropic负责模型推理、prompt/response 数据处理、数据留存策略。

Microsoft/Azure 负责订阅管理、计费、认证（API Key / Entra ID）、API 端点路由、使用量元数据

本质上是一个中转站。请求通过 Azure 端点进来，经过认证和计费层，然后转发到 Anthropic 的基础设施上执行推理。这也解释了为什么按 Anthropic 标准定价计费——因为模型实际就跑在 Anthropic 那边。

## limit

### what you can see

- 可以在 Azure Cost Management 中查看费用，但费用出现在 Marketplace 类别下（不是原生 Azure 服务）
- 基础监控指标，通过 Azure Monitor 可追踪 API 调用量、延迟、错误率等。
- Token 使用量，API 响应中的 usage 对象会返回详细的 token 消耗信息。
- 诊断日志，启用 Diagnostic Settings 后，可以路由到 Log Analytics，用 Kusto 查询

### what you can't see

- 对话内容（输入/输出），默认不记录。 
- Source IP 同样默认不记录

如果想看这些东西，那么需要额外部署网关架构（如 Azure API Management）让所有请求经过网关

## apim or native api?

如何判断 API 是否架了网关？我们可以查看端点 URL：

- `*.services.ai.azure.com/anthropic/` 直连 Foundry 端点
- `*.azure-api.net/*` 经过 Azure API Management 网关
- `localhost:* or self-define domian` 经过 Kong / 自建网关

如果在 Foundry 资源上启用了 AI Gateway（APIM），URL 格式会变，通常会出现 azure-api.net 的域名。