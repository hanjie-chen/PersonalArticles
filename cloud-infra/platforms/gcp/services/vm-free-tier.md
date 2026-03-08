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

machien type: e2-micro

入栈流量是免费的

所以只需要满足这里几个条件就可以白嫖了。我创建了一台这样子的机器，不知道最终是否会收费来着。



## region and zone

你可以把它们想象成“城市”和“机房大楼”的关系。

#### Region (区域) —— 城市级

- 定义： 这是一个独立的地理区域，比如“新加坡” (`asia-southeast1`) 或“爱荷华州” (`us-central1`)。
- 距离： 区域之间通常相隔几百甚至几千公里。
- 用途： 主要是为了合规性（数据存在哪个国家）和延迟（选离用户近的地方）。

#### Zone (可用区) —— 机房级

- 定义： 它是 Region 内部的一个或多个数据中心。一个 Region 通常包含至少 3 个 Zone。
- 命名： 名字是在 Region 后面加个字母，例如 `us-central1-a`。
- 距离： Zone 之间距离很近（通常在同一城市的不同电力/网络网格上），延迟极低（<1ms）。
- 用途： 主要是为了高可用（HA）。如果 `zone-a` 的空调或电力坏了，你的应用如果在 `zone-b` 也有备份，就不会挂掉。
