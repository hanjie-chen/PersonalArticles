---
Title: Cloudflare Usage Guide
SourceBlob: 10e3fd4c92e82e563475626f3811a60dbe113bc7
---

```
BriefIntroduction: A guide to using Cloudflare
```

<!-- split -->

# Domain DNS Hosting

After purchasing a domain, you can choose to host the domain's DNS on Cloudflare.

This is because Cloudflare's DNS performance is often better than that of the domain provider.

Using Namecheap as an example, you can follow this article to host your domain on CF: [How to set up DNS records for your domain in a Cloudflare account - Hosting - Namecheap.com](https://www.namecheap.com/support/knowledgebase/article.aspx/9607/2210/how-to-set-up-dns-records-for-your-domain-in-a-cloudflare-account/)

# Enable Cloudflare CDN

How does Cloudflare configure the website's real backend (origin)?

In Cloudflare, there is no separate page dedicated to backend settings. By default, we configure it in DNS:

In the DNS tab of the Cloudflare Dashboard, if you set a DNS record (such as a CNAME or A record) and enable Proxy (the orange cloud icon), Cloudflare automatically treats the address pointed to by that DNS record as the backend (origin).

That means:

- You do not need to configure the backend (origin) separately. The target address of the CNAME or A record in DNS is the backend (origin) for Cloudflare CDN by default.
- When users request your domain, Cloudflare automatically proxies the request to the DNS target address you configured.

For example, suppose your current DNS configuration is as follows:

| Type  | Name | Content              | Proxy status |
| ----- | ---- | -------------------- | ------------ |
| CNAME | www  | yoursite.azurefd.net | 🟠 Proxied    |

Then:

- When a user visits `www.example.com`, the request first goes to Cloudflare CDN.
- Cloudflare CDN checks whether cached content exists:
  - If there is cached content, it returns it directly to the user;
  - If not, Cloudflare automatically routes the request back to `yoursite.azurefd.net` (the target address you entered in DNS), so this address automatically becomes Cloudflare's backend (origin).

## HTTPS

To force HTTPS for the entire user-side connection, we can enable these two settings:

- Always Use HTTPS: when a user visits `http://hanjie-chen.com`, Cloudflare returns a 301 redirect to `https://...`.
- Automatic HTTPS Rewrites: if the page contains links like `http://xxx.js`, Cloudflare tries to rewrite them to `https://xxx.js` to reduce mixed content errors.

In the domain's `SSL/TLS --> Edge Certificate` page, you can see and enable these two options.
