---
Title: Python Makrdown 使用指南
Author: 陈翰杰
Instructor: o1
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

可以使用official extensions, third party extensions 和 自己写的extensions



# Reference

documents: [Python-Markdown — Python-Markdown 3.7 documentation](https://python-markdown.github.io/)

github: [Python-Markdown/markdown: A Python implementation of John Gruber’s Markdown with Extension support.](https://github.com/Python-Markdown/markdown)

