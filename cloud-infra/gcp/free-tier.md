听说 gcp 有着 free tier 的机器，我看看是否可以白嫖一个：

根据这个文档

[Free Google Cloud features and trial offer  | Google Cloud Free Program  | Google Cloud Documentation](https://docs.cloud.google.com/free/docs/free-cloud-features)

满足以下条件的 compute engine 是免费的

region:

- Oregon: `us-west1`.
- Iowa: `us-central1`.
- South Carolina: `us-east1`.

disk: 30 GB-months standard persistent disk.

network: 

[Network Service Tiers pricing | Google Cloud](https://cloud.google.com/network-tiers/pricing?hl=en)

- premium tier: 1 GB of outbound data transfer from North America to all region destinations (excluding China and Australia) per month.
- standard tier: 200 GB outbound data

入栈流量是免费的

所以只需要满足这里几个条件就可以白嫖了。我创建了一台这样子的机器，不知道最终是否会收费来着

1. 或许可以在我的树莓派上连接上 google iap(使用google sdk), 然后链接到我的machine因为树莓派使用了tun模式，感觉应该可以无缝连接上

   

简单来说，是的，IAP TCP 转发（用于 SSH/RDP）是完全免费的。

它是 Google Cloud 为了推行“零信任”安全架构而提供的一项基础功能。你只需要为 VM 本身和产生的流量付费，IAP 隧道服务本身不收一分钱。

关于在 Windows Terminal 中连接，答案也是肯定的，而且体验非常棒。

------

### 1. IAP 真的免费吗？

- 功能免费： 使用 IAP 隧道来转发 SSH、RDP 或其他 TCP 流量，不收取任何订阅费或开启费。
- 流量计费： 注意，通过 IAP 隧道传输的数据仍然算作“出站流量”。如果你走的是 Standard Tier，依然享受那 200 GB 的免费额度。
- 唯一收费项： 只有当你需要使用 Chrome Enterprise Premium（用于更高级的应用层身份验证或设备上下文规则）时才收费，普通人 SSH 连个服务器是用不到那个的。

------

### 2. 如何在 Windows Terminal 中使用 IAP？

要在本地终端连接，你需要安装 **Google Cloud CLI**。配置好后，Windows Terminal 就像直连一样方便。

#### **第一步：安装 gcloud CLI**

1. 下载并安装 [Google Cloud SDK](https://www.google.com/search?q=https://cloud.google.com/sdk/docs/install%23windows)。
2. 在 PowerShell 或 CMD 中运行 `gcloud init` 完成登录和项目选择。

#### **第二步：配置防火墙（只需一次）**

去 GCP 控制台，创建一个允许入站的规则：

- **源 IP 范围：** `35.235.240.0/20` （这是 IAP 服务的专用 IP）
- **协议和端口：** TCP 22
- **目标：** 选择你的 VM 或应用到所有实例。

#### **第三步：在 Windows Terminal 连接**

直接输入以下命令即可（它会自动建立隧道并登录）：

PowerShell

```
gcloud compute ssh [你的虚拟机名称] --tunnel-through-iap
```

> **小技巧：** 如果你觉得命令太长，可以在 Windows Terminal 的配置文件（Settings -> JSON 文件）里专门加一个 Profile，把上面的命令放进 `commandline` 项。这样你点击下拉菜单，一键就能进入服务器。

------

### 3. 我是否可以彻底关掉外网 IP？

**可以，而且强烈建议这样做！**

当你配置好 IAP 后，你可以把虚拟机的“外部 IP 地址”设置为 **None**（无）。

- **好处 1：** 没有任何黑客能从公网扫到你的机器（因为根本没有公网 IP）。
- **好处 2：** **省钱！** 谷歌会对分配了但不使用的静态外部 IP 收费。去掉 IP 后，你的 VM 纯内网运行，安全且省心。

### 总结

IAP 是 GCP 给开发者的一个“大礼包”：**免费、极度安全、支持本地终端**。

你想让我帮你写一段可以直接贴进 Windows Terminal 配置文件里的 JSON 代码，让你实现“一键 SSH 登录”吗？