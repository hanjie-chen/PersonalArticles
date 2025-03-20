对于网站，想要自定义字体，可以选择下载到本地。

参考这篇文章 [免费引入商用黑体字体系列整理及 CSS 字体引入亲妈式教程（20240915更新） – 风记星辰](https://www.thyuu.com/62610#976c19ac-7ff8-4d2e-ad71-9d195d848c74-link)

提到了很多好用的字体

其中考虑阿里巴巴：[阿里巴巴普惠体](https://www.alibabafonts.com/#/font) 开源免费

Google Font: [Selection - Google Fonts](https://fonts.google.com/selection)

因为我使用之前的字体 Pingfang 简体 Regular的时候，发现有几个字符没有覆盖到，导致使用了微软雅黑的font, 非常的不和谐，所以我想要使用其他的字体看看

发现苹果的PingFang 简体其实就是华康金刚黑，但是其实是需要商业授权，所以我还是偏向于开源和免费的字体

字体文件分为 ttf 文件和 woff2 文件，后者是为 web 字体专门优化的，更加适合浏览器的方案。但是很多都没有提供woff2的版本，比如说google的字体

考虑到其实一个完整字体文件是比较大的 10M 左右，其实存在优化方案

这些 @font-face 规则定义了 Noto Sans SC 字体在不同 Unicode 范围内的字形。每个 @font-face 规则都指定了一个 .woff2 格式的字体文件 URL，并通过 unicode-range 属性定义了该字体文件覆盖的 Unicode 字符范围。

浏览器会根据网页中实际使用的字符，自动下载所需的字体文件。因此，您无需手动选择要下载的 URL。

但是，我建议您直接在网页中使用 Google Fonts 提供的 @import 或 <link> 方式引入字体，让浏览器自动处理字体文件的加载。这样可以减少不必要的网络请求，提高网页性能。如果您确实需要在本地托管字体文件，可以考虑使用字体子集化工具（如 FontSquirrel 的 Webfont Generator），根据网页实际使用的字符生成优化后的字体文件，而不是加载完整的字体文件。

Google Fonts 提供的 @font-face 规则中的 unicode-range 属性，就是一种字体子集化的实现方式。

Unicode-range 属性定义了每个字体文件所包含的 Unicode 字符范围。这样，浏览器可以根据网页中实际使用的字符，只下载覆盖这些字符的字体文件，而不是加载整个字体。这种按需加载的方式可以显著减少字体文件的大小，提高网页加载速度。

这与使用字体子集化工具（如 FontSquirrel 的 Webfont Generator）的目的类似。这些工具可以根据您提供的一组字符，生成只包含这些字符的字体子集文件。

不过，Google Fonts 的方式更加自动化和灵活。它预先为每个字体生成了多个子集文件，并通过 @font-face 规则的 unicode-range 属性来定义每个子集的字符范围。浏览器会自动分析网页内容，并下载所需的字体子集文件。

相比之下，使用字体子集化工具通常需要手动提供字符集，生成子集文件，并手动在 CSS 中引用这些文件。如果网页内容发生变化，可能还需要重新生成字体子集。

因此，如果您的网页主要使用 Google Fonts 提供的字体，直接使用其提供的 @import 或 <link> 方式引入字体是最简单高效的。Google Fonts 会自动处理字体子集化和按需加载。而如果您使用自定义字体，则可以考虑使用字体子集化工具来优化字体文件，提高网页性能。



# Pingfang SC

目前完整的pingfang SC我只找到这一个ttf的格式 [zongren/font: 个人博客所用的中文字体](https://github.com/zongren/font) 其他的链接下载的似乎并没有包含所有的字体

大约10M 左右的大小，是否可以考虑将其转换为woff2呢？