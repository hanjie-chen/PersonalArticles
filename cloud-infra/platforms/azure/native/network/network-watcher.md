network watcher 这个玩意会随着你创建 vnet 自动创建

在 microsoft documnet: [Enable or disable Azure Network Watcher | Microsoft Learn](https://learn.microsoft.com/en-us/azure/network-watcher/network-watcher-create?tabs=portal) 提到

> By default, Network Watcher is automatically enabled. When you create or update a virtual network in your subscription, Network Watcher will be automatically enabled in your Virtual Network's region.

也就是说 vnet 的 region 创建在哪里，就会自动创建出一个相关 region 的 network watcher
