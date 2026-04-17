<!-- source_blob: 10e3fd4c92e82e563475626f3811a60dbe113bc7 -->

# Domain DNS Hosting

After purchasing a domain, you can choose to host the domain's DNS on Cloudflare.

This is because Cloudflare's DNS performance is often better than that of the domain provider.

Using Namecheap as an example, you can follow this article to host your domain on Cloudflare: [How to set up DNS records for your domain in a Cloudflare account - Hosting - Namecheap.com](https://www.namecheap.com/support/knowledgebase/article.aspx/9607/2210/how-to-set-up-dns-records-for-your-domain-in-a-cloudflare-account/)

# Enable Cloudflare CDN

How does Cloudflare set the actual backend (origin) of a website?

In Cloudflare, there is no separate page specifically for backend settings. By default, this is configured in DNS:

In the DNS tab of the Cloudflare Dashboard, if you set a DNS record (such as a CNAME or A record) and enable Proxy (the orange cloud icon), Cloudflare automatically treats the address pointed to by that DNS record as the backend (origin).

In other words:

- You do not need to configure the backend (origin) separately. The target address of the CNAME or A record in DNS is, by default, the backend (origin) for the Cloudflare CDN.
- When users request access to your domain, Cloudflare automatically proxies the request to the DNS target address you configured.

For example, suppose your current DNS settings are as follows:

| Type  | Name | Content              | Proxy status |
| ----- | ---- | -------------------- | ------------ |
| CNAME | www  | yoursite.azurefd.net | 🟠 Proxied    |

Then:

- When a user visits `www.example.com`, the request first enters the Cloudflare CDN.
- The Cloudflare CDN checks whether cached content is available:
  - If cached content exists, it is returned directly to the user;
  - If not, Cloudflare automatically forwards the request to `yoursite.azurefd.net` (the target address you entered in DNS), so this address automatically becomes Cloudflare's backend (origin).

## HTTPS

To force users to use HTTPS throughout the entire visit, we can enable these two settings:

- Always Use HTTPS: When a user visits http://hanjie-chen.com, Cloudflare returns a 301 redirect to https://...
- Automatic HTTPS Rewrites: If the page contains links such as http://xxx.js, Cloudflare attempts to rewrite them to https://xxx.js, reducing mixed content errors.

On the domain's `SSL/TLS --> Edge Certificate` page, you can see these two options and enable them.
