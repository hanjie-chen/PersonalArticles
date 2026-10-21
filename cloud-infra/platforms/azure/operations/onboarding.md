---
RolloutDate: 2026-05-24
---

# 接手陌生 Azure 环境时如何开始

## Background

当我们从零接手一个已经存在的 Azure 项目时，应该如何开始？

打开交接文档，看到一堆拓扑和说明，脚本，两眼一黑。

打开 Azure Portal，看到一大堆 resource group、Kubernetes、networking、database、monitoring ，然后接着两眼一黑。

所以对于这种情况，我们应该怎么办？

## Core principle

先建框架，再填细节。

不要一开始就进入 Portal 里逐个点资源，因为现在你脑子里没有一个"架构骨架"去挂这些资源。200 个资源摆在你面前，你不知道谁和谁是一组的、谁依赖谁。

也不要直接把所有资源 `az resource list` 出来以后硬看。那样虽然看到了很多东西，但很难判断哪些资源是核心链路，哪些只是辅助设施，哪些已经废弃。

更好的顺序是：

1. 先利用 AI 读一遍文档，然后找到自己需要负责的部分。
2. 对于这个部分，在让 AI 用 Azure CLI 做资源盘点。
3. 接着让 AI 把文档和实际资源对照。
4. 带着具体问题问同事。

## Start from documents

第一步让 AI 先快速翻文档，重点只看几个问题：

- 这个项目用了哪些 Azure 服务？
- 用户流量从哪里进入？
- 请求经过哪些关键组件？
- 数据最终存在哪里？
- 有几套环境，比如 dev、staging、prod？
- 部署、监控、告警、回滚有没有现成说明？

这一步的产出不是详细理解每个服务，而是在脑子里先形成一张粗略地图。

比如可以先得到这样的骨架：

```text
User
-> DNS / Front Door / Application Gateway
-> AKS / App Service / VM
-> Storage / Database / Queue
-> Monitoring / Alerting
```

即使这个骨架一开始不准确，也比没有骨架好。后面盘点资源和问同事时，可以不断修正它。

## Inventory resources with CLI

第二步：用 CLI 做资源盘点，不用 Portal

Portal 信息太多太散，CLI 反而更清晰。比如先按 Resource Group 分组看，因为一般一个 Resource Group 就是一个逻辑单元：

```bash
az group list --output table
```

然后挑一个 Resource Group 看里面有什么：

```bash
az resource list --resource-group <name> --output table
```

这样你拿到的是一个**结构化的清单**，比在 Portal 里点来点去高效得多。

## Compare documents with reality

第三步把文档和实际资源对照。

不要假设文档一定是对的，也不要假设实际资源一定都还在使用。真实项目里经常会出现这些情况：

- 文档提到了 A、B、C，但 Azure 里实际还有 D。
- 文档说系统跑在 App Service，但实际已经迁移到 AKS。
- 某个 resource group 看起来还在，但其实只是历史遗留。
- prod 和 staging 的资源命名规则不一致。
- Terraform、Portal 手工配置、脚本部署混在一起。

这些差异本身就是非常重要的信息。接手项目时，发现差异不是坏事，而是开始真正理解系统的入口。

## Ask teammates with concrete questions

第四步再去问同事。

不要一开始就问：

> 这个项目怎么运维？

这个问题太大，对方很难回答，也容易得到一段很散的介绍。

更好的方式是先自己读文档和盘资源，然后带着具体问题去问：

- 文档里说入口是 Application Gateway，但我看到还有 Front Door，现在流量实际从哪里进来？
- 这个 resource group 里的 App Service 看起来像旧版本，它还在接流量吗？
- prod 的 AKS cluster 是手工维护，还是通过 Terraform 管理？
- Key Vault 里的 secret 更新流程是谁负责？
- 现在告警主要看 Application Insights，还是 Log Analytics workspace？
- 如果线上服务挂了，第一步应该看哪个 dashboard 或 runbook？

这种问题更容易问出有价值的答案，也能让同事知道你已经做过基础功课。

## Practical order

可以把流程压缩成下面这张表：

| Step | Action | Purpose |
| ---- | ------ | ------- |
| 1 | 快速翻文档 | 建立项目骨架 |
| 2 | CLI 盘点资源 | 看清 Azure 里实际有什么 |
| 3 | 文档和实际资源对照 | 找出过时、遗漏和迁移痕迹 |
| 4 | 带着问题问同事 | 补齐关键背景 |
| 5 | 整理自己的 runbook | 把一次接手变成可复用经验 |
