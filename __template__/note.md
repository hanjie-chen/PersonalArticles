---
RolloutDate: 2023-01-01
---

# Note Template

![cover image](./resources/images/cover_image.jpeg)

## Format

写笔记时以这篇模板的格式为准：

- 第一行是笔记标题，也是全篇唯一的 `#` 一级标题；正文章节从 `##` 开始。没有 `#` 标题的笔记，网站显示文件名
- 文件开头的 front matter 可以省略，只用来写 `RolloutDate: YYYY-MM-DD`，表示写作日期；更新日期由网站从 git 提交记录读取
- 图片用相对路径引用，例如上面的封面图
- 引用本仓库的其他笔记，使用从仓库根目录开始的路径，以 `/` 开头，这样在 GitHub 上也能正确跳转，例如 [git 命令速查](/tools/git/commands.md)

```markdown
[git 命令速查](/tools/git/commands.md)
```

## Before we beginning/Background

介绍本文的背景和自己的想法，网站上右侧为本页目录

这个结构参考 Microsoft Learn document 和 Docker document

使用 `写在前面` 还是 `Before we beginning` 取决于整体标题风格，例如如果都是英文标题，那么同样保持英文标题

这篇文章用于测试我会用到的大部分 markdown 功能

---

这里写文章的==正文内容==

以下为正文内容 [^引用 1] 这个地方可以引用是可以直接跳转的，如果页面足够长的话。

还有一些 Latex 数学公式的支持

## Part1

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

## Part 2

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

## Part 3: Math formula support

- `$$...$$` 是传统的 LaTeX 分隔符
- `math...` 是 GitHub Flavored Markdown (GFM) 的特定语法

行内公式：这是一个行内公式 $f(x) = x^2$

### 块级公式

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

### 行内公式

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


## Appendix

附加材料

- [x] 主任务
  - [ ] 子任务 1
  - [ ] 子任务 2

## Reference

[^引用 1]: chj is good
