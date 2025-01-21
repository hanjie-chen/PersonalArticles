---
Title: Python Makrdown 使用指南
Author: 陈翰杰
Instructor:
CoverImage:
RolloutDate:
---

```
BriefIntroduction: 
python markdown 3.7 使用指南
```

<!-- split -->

# Before we begin

因为一直使用 Typora + github 来做笔记和同步，现在需要搭建一个自己的网站，所以需要将 .md 文件渲染为 .html 文件，于是找上了 python-markdown 这个 python library 

好消息是 Typora 有主题供我选择，可以直接拿到 css 源文件，供我参考设计出自己的样式，

# Basic usage

基本使用如下：
```python
import markdown
html = markdown.markdown(your_text_string)
```

## `markdown.markdown` function

usage

```python
markdown.markdown(text, extensions=['extra', 'meta', MyExtensionClass()])
```

### text

raw makrdown string 这个参数需要 [unicode string](ersonalArticles/technical/Programming/python-learn/python-language/Python_Basic/unicode.md)

### extensions

python-markdown 原始实现主要关注于 Gruber 定义的核心 Markdown 语法，而对于后来的一些扩展语法，则需要我们显式地启用相应的扩展，不过 python-markdown 这个库已经自带了一些常用的扩展 [^python-markdown-extensions]

`extra`

这个扩展包含 7 个扩展，使用 `extension=[‘extra’]` 就可以包含这 7 个扩展

| Extension          | Entry Point | Dot Notation                    | my usage           |
| ------------------ | ----------- | ------------------------------- | ------------------ |
| Abbreviations      | abbr        | markdown.extensions.abbr        | :x:                |
| Attribute Lists    | attr_list   | markdown.extensions.attr_list   | :x:                |
| Definition Lists   | def_list    | markdown.extensions.def_list    | :x:                |
| Fenced Code Blocks | fenced_code | markdown.extensions.fenced_code | :heavy_check_mark: |
| Footnotes          | footnotes   | markdown.extensions.footnotes   | :heavy_check_mark: |
| Tables             | tables      | markdown.extensions.tables      | :heavy_check_mark: |
| Markdown in HTML   | md_in_html  | markdown.extensions.md_in_html  | :heavy_check_mark: |

entry point 使用方式 `extenisons = ['footnotes', tables]`

dot notation 使用方式， 过于麻烦不推荐使用

```python
from markdown.extensions import extra, codehilite

html = markdown.markdown(text, extensions=[extra.makeExtension(), codehilite.makeExtension()])
```

除此之外还有 10 个自带的 extension

| Extension  | Entry Point | Dot Notation | my usage           |
| ---------- | ----------- | ------------ | ------------------ |
| Admonition |             |              | :x:                |
| CodeHilite |             |              | :heavy_check_mark: |
|            |             |              |                    |
|            |             |              |                    |
|            |             |              |                    |
|            |             |              |                    |

对于 Admonition 我一般使用 github markdown style 语法代替

CodeHilite 必须安装 pygments 来解析代码，并且在 html 相关位置插入 html 标签使得 css 生效

# Reference

documents: [Python-Markdown — Python-Markdown 3.7 documentation](https://python-markdown.github.io/)

github: [Python-Markdown/markdown: A Python implementation of John Gruber’s Markdown with Extension support.](https://github.com/Python-Markdown/markdown)

[^python-markdown-extensions]: [Extensions — Python-Markdown 3.7 documentation](https://python-markdown.github.io/extensions/)