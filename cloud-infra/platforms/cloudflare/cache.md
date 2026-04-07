# Cache Rules

free plan 用户拥有 10 条免费规则。

Cache Rules 的本质是告诉 Cloudflare：“当请求满足 XX 条件时，请按 YY 方式缓存”。

- Edge Cache TTL（边缘缓存生命周期）：强制静态资源在 Cloudflare 节点存多久，甚至可以覆盖源站的 `Cache-Control`。
- Browser Cache TTL（浏览器缓存生命周期）：控制访问者浏览器里的缓存时间。
- Cache Deception Armor：防止 Web 缓存欺骗攻击。
- Bypass Cache（绕过缓存）：比如检测到登录 Cookie 时，直接穿透到源站，不走缓存。
- Cache Everything：即使是没有后缀名的 URL，也可以强制缓存为静态页面（这对 web 小说或博客系统的 HTML 加速非常有用）。

## config

location: domian(click in) --> Caching --> Cache Rules

这里有着 2 个选择

- Cache Rules: 控制缓存逻辑
- Cache Response Rules: 修改 request response header

一般来说，我们只需要创建 cache rules



# default cache behavior

即使一条 Cache Rule 都不写，Cloudflare 也会自动缓存一部分内容。

Cloudflare 有一套内置的 "Standard Caching"（标准缓存策略）。

它会自动识别文件的扩展名。如果请求的文件属于以下类型，Cloudflare 默认就会尝试缓存它们：

- 图片：`.jpg`, `.png`, `.gif`, `.webp` 等。
- 样式与脚本：`.css`, `.js`。
- 字体与文档：`.woff2`, `.pdf` 等。

如果说默认缓存是“自动挡”，那么 Cache Rules 就是“手动挡”。

没有 Cache Rules 时：

- CF 只按后缀名缓存。
- HTML 页面默认是不缓存的（因为 CF 认为 HTML 可能是动态生成的，比如登录后的个人信息）。
- CF 会严格遵守你源站（Flask 或 Nginx）返回的 `Cache-Control` 响应头。

有了 Cache Rules 后，你可以打破这些限制：

- 缓存 HTML：你可以强制让 `/articles/1.html` 这种页面也缓存到边缘节点。
- 忽略源站错误：即使你的源站没配置缓存头，你也可以在 CF 侧强制设置 TTL（生存时间）。
- 自定义逻辑：比如“只要是来自上海的请求，缓存 1 小时；其他的缓存 1 天”。

# blog website

对于我的个人博客网站，如何使用 cache rule 来缓存呢？

要缓存的东西有 2 种

- static/ 下面的 js, css 

这里需要注意的是，最好不要缓存 `/`, `/about`, `/articles` 等 html 界面。

因为这样子的话，页面每次都会从源站重新渲染。而我对 css 资源之后会加上一个 query `?v=xxx` 这个 xxx 是这个 css 文件在磁盘上的“最后修改时间”

所以，只要我修改了 css 文件，那么根据这个机制，每次 client 就能从源站拿到最新的 css 文件，避免因为 cache 导致的样式落后。

如果 HTML 页面被缓存，那么可能出现页面里还在引用旧 css 文件的情况。

所以流程其实是这样：

1. 用户请求 `https://hanjie-chen.com`
2. Flask 渲染模板时调用 `_asset_url()`，读取当前磁盘上 CSS 的 `mtime`
3. 模板输出新的 `<link href="/static/css/about-me.css?v=新值">`
4. 浏览器再去请求这个新 URL
5. Cloudflare 发现这是一个新 cache key，就会去源站抓新的 CSS

