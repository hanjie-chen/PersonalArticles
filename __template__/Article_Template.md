---
Title: Articles Template
Author: 陈翰杰
Instructor: chatGPT 3.5
CoverImage: ./images/cover_image.jpeg
RolloutDate: 2023-01-01
---

```
BriefIntroduction: 
这里存放文章简介，原本的想法的类似与论文的摘要功能，我想着要不要把chatGPT3.5接入进来。让她帮我生成文章简介，看看我自己写的文章简介和她写的文章简介哪一个更好。
封面图片默认路径 ./images/cover_image.jpg [png, webp, ...] 还是需要保留，因为同一个category（path）下面共用同一个images文件夹，所以可能不一定都叫做cover_image
```

<!-- split -->

![cover image](./images/cover_image.jpeg)

# 写在前面/Before we beginning/Background

介绍本文的背景和自己的想法，右边为文章目录，左边是同一个 category 目录下的文章 link 

这个结构参考 Microsoft Learn document 和 Docker document

使用 `写在前面` 还是 `Before we beginning` 取决于整体标题风格，例如如果都是英文标题，那么同样保持英文标题

这篇文章用于测试我会用到的大部分 markdown 功能

# Title: 文章模板

这里写文章的==正文内容==

以下为正文内容 [^引用 1] 这个地方可以引用是可以直接跳转的，如果页面足够长的话。

还有一些 Latex 数学公式的支持

引用本仓库其他的已经存在的文章使用基于仓库根目录的绝对路径，例如

[git 笔记](/tools-guide/git-guide/Git使用指南.md)

```markdown
[git 笔记](/tools-guide/git-guide/Git使用指南.md)
```

因为这在 github 上面也能正确解析 特别说明：以 `/` 开头代表从仓库根目录开始

# Part1

part 1 content

> quota other thing, or actually note
>
> if I get mutil layer quota what it will shows?

差异高亮显示

```diff
- 这行被删除了
+ 这行是新增的
```

> [!NOTE]
> 这是一个普通提示信息

> [!TIP]
> 这是一个提示

> [!IMPORTANT]
> 这是一个重要信息

> [!WARNING]
> 这是一个警告信息

> [!CAUTION] 
> 这是一个危险警告

# Part 2

emoji 表情支持 比如

```emoji
:peach:
:x:
:heavy_check_mark:
```

:peach:

:x:

:heavy_check_mark:

markdown emoji 大全 [Complete list of github markdown emoji markup](https://gist.github.com/rxaviers/7360908)

# Part 3: Math formula support

- `$$...$$` 是传统的 LaTeX 分隔符
- `math...` 是 GitHub Flavored Markdown (GFM) 的特定语法

行内公式：这是一个行内公式 $f(x) = x^2$

## 块级公式

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
- 块级公式：```` math ````

## 行内公式

不过这个块级公式在 Typora 中相比于行内公式似乎显示有点小，打算在 Typora css 中调整一下
$$
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
$$


# Appendix

附加材料

- [x] 主任务
  - [ ] 子任务 1
  - [ ] 子任务 2

# Reference

[^引用 1]: chj is good