# Cloudflare Access

Cloudflare Access 是一个给任何网页/服务加一把锁的工具，属于 Cloudflare Zero Trust 产品线。

### 核心特性

- 零信任（Zero Trust）：不信任任何 IP 或网络。即便黑客知道了你的 IP，只要没有你的身份授权，他们连你的服务器登录框都看不见。
- 多种登录方式：可以设置用 Google 账号、GitHub 账号，甚至是发送到你邮箱的 One-Time Pin（临时验证码）来登录。
- 无需客户端：你不需要在电脑或手机上装任何软件，只要有浏览器就能登录。

### 免费额度

Cloudflare Access 前 50 个用户完全免费。

意思是可以创建无限个这样的保护规则（Applications），但是 free plan 只有 50 人能够通过身份验证进入。

例如

假设设置了 Cloudflare Access，要求通过 Google 账号登录：

1. 你用自己的邮箱登录了后台，占用额度是 1 个用户。
2. 你想让你的一个好朋友也帮你看一下小说初稿，你授权了他的邮箱 `friend@gmail.com`，占用额度是 2 个用户。
3. 即便你和你的朋友同时访问了你域名下 100 个不同的加密路径，只要你们还是这两个账号，Cloudflare 依然只算你们 2 个用户。

## 如何使用

在左侧最外层的导航栏，找到 Zero Trust（通常在左侧边栏的中部）。

因为 Zero Trust 是 Cloudflare 的独立子系统，第一次使用需要一个简单的“激活”过程。激活成功后，

会进入一个新的控制台（Zero Trust Dashboard）。在里面找到 Access controls -> Applications。

## 配置钥匙 (Add an IdP)

Cloudflare 需要知道通过什么方式验证你的身份。在左侧边栏找到 Intergrations --> Identity providers

选择添加 Add an identity provider, 这里我们选择最简单的 One-time PIN(OTP)

它不需要去 Google 或 GitHub 申请复杂的 API Key，只需要输入邮箱，CF 会发验证码给你。

## add policy

通常只需要填写 basci information, add rules 即可

### Basic information

policy: hanjie-only

action: allow

session duration: same as application...

### Add rules

selector: emails

value: （写上邮箱）

### Connection context

用来控制远程桌面（RDP）连接时的安全细节的。

- Text clipboard control: 决定你是否可以把本地的文字复制粘贴到远程服务器里。
- 建议：保持默认的 `Off` 即可。

### Additional settings (optional) 

这些是“地狱级”的安全增强选项

- Purpose justification: 开启后，你每次登录不仅要输验证码，还要写一段话解释“我为什么要进去”，这通常用于审计。
- Temporary authentication (Beta)：临时授权，需要专门的审批人同意你才能进去。
- 建议：全部保持 OFF 状态。

## add an application

以保护我的网站后台界面为例也就是 hanjie-chen.com/web-log 这个 path

### select type

选择 self-hosted

### configuration application

application name: 随意

session duration: 从成功登录验证到下一次需要重新登录之间的时间长度。选择默认的 24 hours

Add public hostname:

- Input method: Default
- Subdomain: （保持空）
- Domain: hanjie-chen.com
- Path: web-log

Login methods: 选择默认的 Accept all availabe identity providers

### Experience settings(optional)

这一页看作是“装修”页面，它决定了你的登录界面好不好看。可以指节诶跳过

### Advanced settings(optional)

这些是针对 Web 开发的高级安全策略，全部保持默认即可：

- CORS settings：跨域资源共享。如果你不是在写前后端分离的 API 调用，不需要动它。
- Cookie settings：控制登录 Cookie 的安全属性（如 HttpOnly）。
- 401 Response：当有人没登录就访问时，是返回一个登录页还是直接扔回一个 401 错误码。
- Managed OAuth (Beta)：让 Cloudflare 帮你管理更复杂的 OAuth 流程。