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

1. 或许可以在我的树莓派上连接上 google iap(使用google sdk), 然后链接到我的machine