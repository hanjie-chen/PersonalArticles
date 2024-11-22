---
Title: XXXX
Author: 陈翰杰
Instructor: chatGPT 3.5
CoverImage: ./images/cover_image.jpg
RolloutDate: 2023-XX-XX
---

```
BriefIntroduction: 
这里存放文章简介，原本的想法的类似与论文的摘要功能，我想着要不要把chatGPT3.5接入进来。让她帮我生成文章简介，看看我自己写的文章简介和她写的文章简介哪一个更好。
考虑是否删除cover_image 因为都是默认的 ./images/cover_image.(jpg, png, webp)
```

<!-- split -->

![cover image](./images/cover_image.jpeg)

# 写在前面/Before we beginning

介绍本文的背景和自己的想法，右边为文章目录，左边是同一个 category 目录下的文章 link 

这个结构参考 Microsoft Learn document 和 Docker document

使用 `写在前面` 还是 `Before we beginning` 取决于整体标题风格，例如如果都是英文标题，那么同样保持英文标题

# Title: XXXX

这里写文章的==正文内容==

以下为正文内容[^引用1]这个地方可以引用是可以直接跳转的，如果页面足够长的话。

还有一些Latex数学公式的支持

```math
\begin{pmatrix}
a_{11} & a_{12} \\
a_{21} & a_{22} \\
\end{pmatrix}
```



# Part 1

part 1 content

> quota other thing, or actually note?

# Part 2

part 2 content



# Math formula support/数学公式支持

- `$$...$$` 是传统的 LaTeX 分隔符
- ````math...```` 是 GitHub Flavored Markdown (GFM) 的特定语法

行内公式：这是一个行内公式 $f(x) = x^2$

#### 块级公式：

````math
\begin{bmatrix}
Bias^{hidden}_{1\times m}\\
Weights^{hidden}_{n\times m}
\end{bmatrix}_{(n+1)\times m}=
\begin{bmatrix}
b_0^{hidden} & b_1^{hidden} & \cdots & b_{m-1}^{hidden} \\
w_{00}^{hidden} & w_{01}^{hidden} & \cdots & w_{0(m-1)}^{hidden} \\
w_{10}^{hidden} & w_{11}^{hidden} & \cdots & w_{1(m-1)}^{hidden} \\
\vdots & \vdots & \ddots & \vdots \\
w_{(n-1)0}^{hidden} & w_{(n-1)1}^{hidden} & \cdots & w_{(n-1)(m-1)}^{hidden}
\end{bmatrix}_{(n+1)\times m}
````

为了获得最佳的跨平台兼容性，打算采用：

- 行内公式：`$...$`
- 块级公式：````math````

# Appendix

附加材料

# 参考文献

[^引用1]: chj is good