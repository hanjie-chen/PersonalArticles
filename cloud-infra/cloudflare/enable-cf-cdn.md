![cf](./images/cf.jpg)

# domian hold in cloudflare

当我们在够买了一个 domain 之后，可以选择将 domian 的 DNS 托管在 cloudflare 上面

因为 Cloudflare 的 DNS 性能更好（速度更快，通常几秒内生效）而 domain provider 的 DNS 服务在全球范围内的分布并不均衡，可能会导致解析速度慢，Cloudflare 在全球有大量的数据中心，提供低延迟、高性能的 DNS 解析。

以 namecheap 为例，可以根据这篇文章将 domain 托管到 cf 上： [How to set up DNS records for your domain in a Cloudflare account - Hosting - Namecheap.com](https://www.namecheap.com/support/knowledgebase/article.aspx/9607/2210/how-to-set-up-dns-records-for-your-domain-in-a-cloudflare-account/)

# enable cloudflare cdn

cloudflare 如何设置网站真正的 backend(origin)

在 Cloudflare 中，没有专门的 backend 单独设置页面，默认情况我们是在 DNS 中设置的：

在 Cloudflare Dashboard 的 DNS 选项卡中，设置一条 DNS 记录（例如 CNAME 或 A 记录），并且启用了 Proxy（橙色云图标），Cloudflare 自动将这条 DNS 记录指向的地址视为 backend(origin)。

也就是说：

- 你不需要额外配置 backend(origin)，DNS 中 CNAME 或 A 记录的目标地址默认就是 Cloudflare CDN 的 backend(origin)。
- 当用户请求访问你的域名时，Cloudflare 会自动地将请求代理到你设置的 DNS 目标地址上。

举个例子：假设你当前 DNS 设置如下：

| Type  | Name | Content              | Proxy status |
| ----- | ---- | -------------------- | ------------ |
| CNAME | www  | yoursite.azurefd.net | 🟠 Proxied    |

那么：

- 用户访问 `www.example.com` 时，请求首先进入 Cloudflare CDN。
- Cloudflare CDN 检查是否有缓存内容：
  - 如果有缓存，直接返回给用户；
  - 如果没有缓存，Cloudflare 会自动将请求回源至 `yoursite.azurefd.net`（你 DNS 中填写的目标地址），因此这个地址自动成为了 Cloudflare 的 backend(origin)。

## https

为了强制用户端全程 https, 我们可以打开这里两个设定：

- Always Use HTTPS: 用户访问 http://hanjie-chen.com 时，Cloudflare回 301 到 https://...。
- Automatic HTTPS Rewrites: 如果页面里有 http://xxx.js 这类链接，Cloudflare尝试改成 https://xxx.js，减少 mixed content 报错。

在 domian 的 `SSL/TLS --> Edge Certificate` 界面，可以看到打开这里2个选项

