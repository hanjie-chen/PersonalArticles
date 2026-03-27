# Title: Font Loading Optimization



# background

我的个人网站使用两套自定义字体：

- 英文与代码优先使用 `JetBrainsMono`
- 中文优先使用 `PingFangSC`

问题在于，英文字体很快加载完成，中文在首屏初始阶段会先回退到系统字体，过一段时间后，页面才慢慢切换到 PingFangSC

这个问题在首页、导航、按钮、分栏标题等固定 UI 文案上尤其明显。

问题的核心并不是字体选择错误，而是中文字体文件过大。

当时的字体资源情况：

- `JetBrainsMono-Regular.woff2`: 92 kB
- `PingFang-SC-Regular.ttf`: 10 MB

英文只需要加载一个很小的 `woff2` 文件，而中文直接依赖一个超过 `10MB` 的 `ttf` 文件。



# Optimization

下面是我做的三轮优化

## 第一轮优化

### 为 PingFangSC 生成 `woff2`

先把完整中文字体从 `ttf` 转成 `woff2`。新生成的 woff2 文件只有原来的一半大小（5 MB），这一步已经明显降低了完整中文字体的传输体积。

### 增加 `local(...)`

在 font.css 中为两个字体都补上了 `local(...)`，让浏览器在有本地同名字体时优先复用本地资源，而不是每次都重新下载。

## 第二轮优化：UI Subset

对于我们的网站来说，刚刚第一眼进入的 home, about me 界面并没有使用到很多字，所以我们没有必要背完整字库。

于是第二轮优化就是：固定 UI 文案优先用一个很小的中文子集字体，动态正文继续保留完整 `PingFangSC` 兜底

### 生成 UI 文案字符集

新增了一个脚本 build_pingfang_ui_subset.py，用来扫描 `web-app/templates/*.html`

然后提取其中的固定中文 UI 字符，生成：`web-app/static/font/PingFangSC/PingFang-SC-UI-subset.txt`

这份 `.txt` 文件会作为 subset 构建输入

### 生成 UI 子集字体

基于上面的字符集，使用 `pyftsubset` 生成：`web-app/static/font/PingFangSC/PingFang-SC-UI-subset.woff2`

最终的大小 `PingFang-SC-UI-subset.woff2` 仅有 41 kb，比完整的 `PingFang-SC-Regular.woff2` 小很多，更适合首页、导航、按钮、固定标题这类 UI 文案。

### 调整字体回退链

在 `web-app/static/font/font.css` 中，当前字体优先级变成：

1. `JetBrainsMono`
2. `PingFangSCUI`
3. `PingFangSC`
4. 系统中文字体

也就是说英文和代码首先走 `JetBrainsMono`，固定中文 UI 文案优先命中 `PingFangSCUI`，动态正文或超出 UI 子集覆盖范围的字符，再回退到完整 `PingFangSC`

## 第三步：预加载 UI Subset

为了让固定 UI 文案更早稳定下来，在 `web-app/templates/base.html` 中加入了：

```html
<link
  rel="preload"
  href="{{ asset_url('font/PingFangSC/PingFang-SC-UI-subset.woff2') }}"
  as="font"
  type="font/woff2"
  crossorigin
>
```

这样浏览器可以在更早阶段就开始拉取这个小字体文件，而不是等 CSS 和文本真正触发到字体选择时才去下载。

# 最终结果

这轮优化完成后，加载速度很明显比之前要快了。不需要慢吞吞等中文字体加载完成

理论上可以继续细分到，每篇文章一个子集，但当前阶段没有这么做，因为构建复杂度会明显上升，维护成本更高，缓存命中会变差，动态文章内容字符集更难长期维护

所以当前选择的是更稳的折中方案：一个全站固定 UI 文案子集，一个完整中文字体兜底
