你说得没错, 除了 `frontmatter.load()` 函数之外, frontmatter 库还提供了 `frontmatter.loads()` 函数。

# `frontmatter.loads()` function

`frontmatter.loads()` 函数与 `frontmatter.load()` 函数类似, 但它接受一个字符串作为参数, 而不是文件对象。这意味着你可以直接将包含前言的文本内容传递给 `loads()` 函数, 而无需先将其保存到文件中。下面是一个使用 `frontmatter.loads()` 函数的示例:

```python
import frontmatter

content = """
---
title: Hello, World!
date: 2023-04-20
tags:
  - python
  - frontmatter
---

This is the content of the post.
"""

post = frontmatter.loads(content)

print(post.metadata)
print(post.content)
```

在这个例子中, 我们将包含前言的文本内容存储在 `content` 变量中, 然后直接将其传递给 `frontmatter.loads()` 函数。函数返回一个 `Post` 对象, 其 `metadata` 属性包含解析后的元数据字典, `content` 属性包含前言后的文本内容。

#### frontmatter.load()和 frontmatter.loads()的区别

- `frontmatter.load()`: 接受一个文件对象作为参数, 用于读取包含前言的文件。
- `frontmatter.loads()`: 接受一个字符串作为参数, 用于解析包含前言的文本内容。

根据你的需求, 你可以选择使用 `load()` 函数读取文件, 或者使用 `loads()` 函数直接处理文本内容。



# `load()` function

```python
import frontmatter

with open('example.md') as f:
    post = frontmatter.load(f)

print(post.metadata)
print(post.content)
```

在这个例子中,`load()`函数读取包含前言的Markdown文件,并返回一个`Post`对象。`metadata`属性包含解析后的元数据字典,`content`属性包含前言后的文件内容。