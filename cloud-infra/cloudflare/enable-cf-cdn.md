# enable cloudflare cdn

#### Cloudflare 是如何定义 Origin 的？

**在 Cloudflare 中，没有专门叫做“Origin”的单独设置页面（除非你使用专门的产品如 Cloudflare Load Balancer 或 Cloudflare Workers 中明确设定原点）。**默认情况下：

- 当你在 Cloudflare Dashboard 的 DNS 选项卡中，设置一条 DNS 记录（例如 CNAME 或 A 记录），并且启用了 Proxy（橙色云图标），Cloudflare 自动将这条 DNS 记录指向的地址视为**Origin（源站）**。

也就是说：

- 你不需要额外配置 Origin，DNS 中 CNAME 或 A 记录的目标地址默认就是 Cloudflare CDN 的回源地址（Origin）。
- 当用户请求访问你的域名时，Cloudflare 会自动地将请求代理到你设置的 DNS 目标地址上。

**举个例子：**假设你当前 DNS 设置如下：

| Type  | Name | Content              | Proxy status |
| ----- | ---- | -------------------- | ------------ |
| CNAME | www  | yoursite.azurefd.net | 🟠 Proxied    |

那么：

- 用户访问 `www.example.com` 时，请求首先进入 Cloudflare CDN。
- Cloudflare CDN 检查是否有缓存内容：
  - 如果有缓存，直接返回给用户；
  - 如果没有缓存，Cloudflare 会自动将请求回源至 **`yoursite.azurefd.net`**（你 DNS 中填写的目标地址），因此这个地址自动成为了 Cloudflare 的 Origin。

#### 🌟 你当前的情况总结：

- **是的！你理解得没错：DNS 中设置 CNAME 记录，并开启 Proxy 后，这个 CNAME 目标地址会自动成为 Cloudflare 的 Origin 地址，无需额外设置。**
- 你不需要寻找额外的 Origin 配置页面，因为 Cloudflare 已经自动为你完成了这一步。