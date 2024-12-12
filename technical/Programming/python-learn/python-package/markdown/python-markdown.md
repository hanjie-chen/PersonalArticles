---
Title: Python Makrdown 使用指南
Author: 陈翰杰
Instructor: Sonnet 3.5
CoverImage: ./images/cover_image.jpeg
RolloutDate: 2023-XX-XX
---

```
BriefIntroduction: 
python markdown 使用指南
```

<!-- split -->

# Before we begin

因为一直使用 Typora + github 来做笔记和同步，现在需要搭建一个自己的网站，所以需要将 .md 文件渲染为 .html文件，于是找上了python-markdown 这个python library 

好消息是 Typora 有主题供我选择，可以直接拿到 css 源文件，供我参考设计出自己的样式，

# Basic usage

基本使用如下：
```python
import markdown
html = markdown.markdown(your_text_string)
```

## `markdown.markdown` function

参数

```python
markdown.markdown(text, [ ,**kwargs])
```

### text

这个参数需要 [unicode string](/PersonalArticles/technical/Programming/python-learn/python-language/Python_Basic/unicode.md)



# Reference

documents: [Python-Markdown — Python-Markdown 3.7 documentation](https://python-markdown.github.io/)

github: [Python-Markdown/markdown: A Python implementation of John Gruber’s Markdown with Extension support.](https://github.com/Python-Markdown/markdown)