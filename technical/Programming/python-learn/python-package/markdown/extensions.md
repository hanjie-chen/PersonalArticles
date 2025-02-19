关于 python markdown extension

# official extensions

python-markdown 原始实现主要关注于 Gruber 定义的核心 Markdown 语法，而对于后来的一些扩展语法，则需要我们显式地启用相应的扩展，不过 python-markdown 这个库已经自带了一些常用的扩展 [^python-markdown-extensions]

## `extra` extensions

这个扩展包含 7 个扩展，使用 `extension=[‘extra’]` 就可以包含这 7 个扩展

| Extension          | Entry Point | my usage           |
| ------------------ | ----------- | ------------------ |
| Abbreviations      | abbr        | :x:                |
| Attribute Lists    | attr_list   | :x:                |
| Definition Lists   | def_list    | :x:                |
| Fenced Code Blocks | fenced_code | :heavy_check_mark: |
| Footnotes          | footnotes   | :heavy_check_mark: |
| Tables             | tables      | :heavy_check_mark: |
| Markdown in HTML   | md_in_html  | :heavy_check_mark: |

可以通过 entry point 和 dot notation 的方式来使用这些扩展

- entry point

  ```python
  my_articles_extensions = ['fenced_code', 'footnotes', 'tables']
  html = markdown.markdown(text, extensions=my_articles_extensions)
  ```

- dot notation

  ```python
  my_articles_extensions = ['markdown.extensions.extra', 'markdown.extensions.abbr']
  html = markdown.markdown(text, extensions=my_articles_extensions)
  ```



### Fenced Code Blocks

由 3 个反引号组成代码块， 例如

````markdown
```python
python code
```
````

### Footnotes

markdown 脚注

### Tables

markdown 表格



## Other extensions

除此之外还有 10 个自带的 extension

| Extension         | Entry Point  | my usage           |
| ----------------- | ------------ | ------------------ |
| Admonition        | admonition   | :x:                |
| CodeHilite        | codehilite   | :heavy_check_mark: |
| Legacy Attributes | legacy_attrs | :x:                |
| Legacy EM         | legacy_em    | :x:                |
| Meta-Data         | meta         | :x:                |
| New-Line-to-Break | nl2br        | :x:                |
| Sane Lists        | sane_lists   | :heavy_check_mark: |
| SmartyPants       | smarty       | :x:                |
| Table of Contents | toc          | :x:                |
| WikiLinks         | wikilinks    | :x:                |

### Admonition

对于 Admonition 我一般使用 github markdown makrdown 语法代替，如下所示

```markdown
> [!note]
> note part
```

### CodeHilite

代码高亮

CodeHilite 必须依赖 pygments 来解析代码，从而在相关位置插入 html 标签使得 css 生效，我目前常用的 code block 语法是围栏代码块语法，为了支持这个而语法需要 enable fenced_code 扩展

### Legacy EM

斜体

Legacy EM 扩展仅影响下划线 `_` 斜体，而不影响星号 `\*` 斜体

> [!note]
>
> disable `Legacy EM`，Python-Markdown 默认智能地处理下划线，以避免在单词中间的下划线导致意外的强调。例如：
>
> - 输入：`_connected_words_`
> - 输出：`<em>connected_words</em>`
> - 整个 `connected_words` 被识别为一个整体，并被渲染为斜体。
>
> enable `Legacy EM` ，Python-Markdown 将恢复原始 Markdown 的行为，即下划线的匹配不考虑单词边界。例如：
>
> - 输入：`_connected_words_`
> - 输出：`<em>connected</em>words_`
> - 只强调了 `connected`，因为第一个 `_` 和随后遇到的第一个 `_` 之间的内容被视为强调。

### New-Line-to-Break 

可以通过添加 `<br>` 标签来实现段落内换行

### Sane Lists 

有序列表和无序列表混合存在的时候 优化表现

### SmartyPants 

智能标点 看上去没什么用，以后再考虑

### Table of Contents

在开头加上一段目录，无用，我会在侧边栏上展现目录

### WikiLink

一段特别的链接，有用，但是我的 Typora 不支持， 所以实际上也没用



# Third party extension

对于官方不支持的 extension, 已经有了很多的实现，可以查看这个wiki

[Third Party Extensions · Python-Markdown/markdown Wiki](https://github.com/Python-Markdown/markdown/wiki/Third-Party-Extensions)

比如说 GFM admonition 实现 可以参考这个 [dahlia/markdown-gfm-admonition: An extension of Python Markdown that enables the admonition syntax of GFM](https://github.com/dahlia/markdown-gfm-admonition)

# Self-defined extension

对于某些想要自定义的情况，我们需要写自己的插件。这篇文档讲了如何写自己的插件： [Extension API — Python-Markdown 3.7 documentation](https://python-markdown.github.io/extensions/api/)

还有这篇文档 [Tutorial 1 Writing Extensions for Python Markdown · Python-Markdown/markdown Wiki](https://github.com/Python-Markdown/markdown/wiki/Tutorial-1---Writing-Extensions-for-Python-Markdown)

当我们写 extensions 的时候，需要明确 extensions 生效的时间，python markdown 的整个解析和渲染大致会经历以下步骤

| No.  | Processors        | Action                                                       |
| ---- | ----------------- | ------------------------------------------------------------ |
| 1    | Pre Processors    | 对原始 Markdown 文本进行预处理                               |
| 2    | Block Processors  | 对文本进行分块（段落、列表、引用块等），转换为一个 ElementTree 结构的块级节点。 |
| 3    | Inline Processors | 处理块级节点中的内联语法（如加粗、斜体、链接等），同样产出 ElementTree 结构的子节点 |
| 4    | Tree Processors   | 整体处理或修改构建好的 ElementTree（可能对树的任何部分进行遍历、修改、插入、删除） |
| 5    | Post Processors   | 在全部渲染完成后，对最终生成的 HTML（或其他格式）文本做最后一步的修饰或替换后输出。 |

我们需要从中选择一个生效时间

接着，我么需要定义2个 class

1. 一个继承自 `Extension` 用来向解析器注册、配置你要使用的 processors
2. 一个继承自 `Processor` 实现对文本或解析树的实际修改逻辑

前者是挂载和配置点，后者是具体干活的执行者

e.g.

```python
class My_Extension(Extension):
    def extendMarkdown(self, md):
        md.blockprocessors.register(MyBlockProcessor(md.parser), 'my_block', 175)
        # ...或其他 processor

class My_Extension_Processor(BlockProcessor):
    def test(self, parent, block):
        # 判断 block 是否匹配
    
    def run(self, parent, blocks):
        # 修改或生成 ElementTree 的逻辑
```







# Reference

[^python-markdown-extensions]: [Extensions — Python-Markdown 3.7 documentation](https://python-markdown.github.io/extensions/)
