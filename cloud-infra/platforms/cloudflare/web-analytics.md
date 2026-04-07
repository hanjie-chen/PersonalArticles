# Web analytics

## 原理

Web Analytics 依赖一个 RUM beacon，也就是浏览器里运行的 JS snippet。

原因是它要采集的是用户浏览器里的真实体验数据，比如：

- 页面加载时间
- Core Web Vitals
- 浏览器端导航 timing
- 页面浏览事件

这些数据只有“用户浏览器”知道，Cloudflare 的边缘代理单靠转发 HTTP 请求是拿不到完整信息的。  

这些只能靠浏览器执行 JS 后再回传 beacon。

## enable web analytics

location: Cloudflare Dashboard --> Analytics & logs --> Web analytics

如果 domian 托管在 cf 上面，可以直接选择 automatic setup（Cloudflare 会自动注入脚本）。也就是下面的步骤

1. Add a site
2. 在下拉框里选你的 hostname, 例如 `hanjie-chen.com`
3. 点 Done

如果一切正常，Cloudflare 就会对这个 proxied hostname 启用 automatic setup。

## check status

之后你可以点 `Manage site` 看状态，通常会看到类似这些选项：

- `Enable`
- `Enable, excluding visitor data in the EU`
- `Enable with JS Snippet installation`
- `Disable`

## free plan

source: [Web Analytics limits](https://developers.cloudflare.com/web-analytics/limits/)

- Free plan 对 proxied sites 可以开 Web Analytics
- 但 `Rules` 数量在 Free plan 是 `0`
- 也就是说免费版基本是“整站开”，不能很细地按 path 做 Web Analytics 规则
