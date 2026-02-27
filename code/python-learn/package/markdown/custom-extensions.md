

对于某些想要自定义的情况，我们需要写自己的插件。这篇文档讲了如何写自己的插件： [Extension API — Python-Markdown 3.7 documentation](https://python-markdown.github.io/extensions/api/)

例如，想要实现 GFM admonition 的话，可以参考这个 [dahlia/markdown-gfm-admonition: An extension of Python Markdown that enables the admonition syntax of GFM](https://github.com/dahlia/markdown-gfm-admonition)

e.g.

```python
import re
from typing import List, Optional

from markdown.core import Markdown
from markdown.extensions import Extension
from markdown.blockprocessors import BlockProcessor
from markdown.blockparser import BlockParser
from xml.etree.ElementTree import Element, SubElement

class Gfm_Admonition_Extension(Extension):
    def extendMarkdown(self, md: Markdown) -> None:
        md.registerExtension(self)
        md.parser.blockprocessors.register(
            Gfm_Admonition_Processor(md.parser),
            "gfm_admonition",
            105
        )


class Gfm_Admonition_Processor(BlockProcessor):
    PATTERN = re.compile(r"""
        ^\s*                                                # 可能的前导空白
        \[!\s*(note|tip|important|warning|caution)\s*\]     # 匹配 admonition 标签，支持小写
        (?:$|\s*\n)                                         # 行尾或者换行
    """, re.VERBOSE | re.IGNORECASE)
    
    def __init__(self, parser: BlockParser):
        super().__init__(parser)

    def test(self, parent: Element, block: str) -> bool:
        if parent.tag != "blockquote":
            return False
        match = self.PATTERN.match(block)
        return match is not None
    
    def run(self, parent: Element, blocks: List[str]) -> Optional[bool]:
        if not blocks:
            return False
        match = self.PATTERN.match(blocks[0])
        if not match:
            return False
        
        # 去掉匹配部分，剩下的内容会作为内部块内容
        blocks[0] = blocks[0][match.end():]
        admonition_type = match.group(1).lower()  # 统一转换为小写

        # 将原来的 blockquote 改为 div，并设置 CSS 类方便样式定制
        parent.tag = "div"
        parent.set("class", f"admonition {admonition_type}")

        # 添加一个标题子节点
        title = SubElement(parent, "p")
        title.set("class", "admonition-title")
        title.text = admonition_type.capitalize()

        # 将剩余块内容继续解析到这个 div 中
        self.parser.parseBlocks(parent, blocks)
        blocks.clear()

        return True
    
def make_Extension(**kwargs):
    return Gfm_Admonition_Extension(**kwargs)
```



## 导入部分

`import re` 用于正则表达式处理，匹配 Markdown 中的特定标记。

`from typing import List, Optional` 提供类型提示，提升代码可读性和维护性（例如在声明 `blocks` 是列表、返回值可以是 `bool` 或 `None`）。

Markdown 相关导入

`from markdown.core import Markdown`：用于在扩展中操作 Markdown 转换器对象。

`from markdown.extensions import Extension`：所有扩展都需要继承该基础类。

`from markdown.blockprocessors import BlockProcessor`：扩展中需要处理块级元素时，通常要扩展 BlockProcessor。

`from markdown.blockparser import BlockParser`：用于解析 Markdown 块级元素，此处用来作为 BlockProcessor 的参数。

`from xml.etree.ElementTree import Element, SubElement` 标准库中的 XML 模块，用于构造和修改 HTML（或 XML）元素。这里用来创建新的 DOM 元素（如 `<div>` 和 `<p>` 标签）。

## 扩展类：`Gfm_Admonition_Extension`

```python
class Gfm_Admonition_Extension(Extension):
    def extendMarkdown(self, md: Markdown) -> None:
        md.registerExtension(self)
        md.parser.blockprocessors.register(
            Gfm_Admonition_Processor(md.parser),
            "gfm_admonition",
            105
        )
```

继承 `Extension` 类
必须定义一个扩展类，所有扩展都应继承 `markdown.extensions.Extension`。这是**必须的部分**。

`extendMarkdown` 方法

`md.registerExtension(self)`：向 Markdown 转换器注册当前扩展实例。这一步确保扩展能在转换过程中发挥作用。

注册 BlockProcessor：

使用 `md.parser.blockprocessors.register` 方法注册一个块处理器。参数说明：

- 第一个参数是实例化的 `Gfm_Admonition_Processor`，传入当前解析器 `md.parser`。
- 第二个参数 `"gfm_admonition"` 是块处理器的名称，可以任意取，但建议使用有意义的名称。
- 第三个参数 `105` 是优先级；数字越低表示越早执行（优先级排序由 Markdown 决定），这里设置一个合适的优先级使该扩展在正确的顺序中运行。

## 块处理器类：`Gfm_Admonition_Processor`

```python
class Gfm_Admonition_Processor(BlockProcessor):
```

继承 `BlockProcessor` 类，当需要处理 Markdown 的块级语法时，必须继承 `BlockProcessor` 并实现 `test()` 与 `run()` 方法。

### `__init__()` 方法

```python
    def __init__(self, parser: BlockParser):
        super().__init__(parser)
```

通过 `super().__init__(parser)` 调用父类（BlockProcessor）的构造函数，将 Markdown 的 block parser 传入。固定格式，所有自定义 BlockProcessor 类都需要实现构造函数，并调用父类构造函数以确保构造器链正确。



### `test` 方法

```python
    def test(self, parent: Element, block: str) -> bool:
        if parent.tag != "blockquote":
            return False
        match = self.PATTERN.match(block)
        return match is not None
```

作用：

- 判断传入的块（文本）是否应由这个处理器处理。
- 检查当前块是否位于一个 `<blockquote>` 中（通常 GitHub Flavored Markdown 的 admonition 语法要求嵌在引用中）。
- 用正则表达式 `PATTERN` 进行匹配，如果匹配成功则返回 `True`。

必要性：
`test` 方法是 BlockProcessor 必须实现的。它决定了 Markdown 文本中的哪个块需要由该处理器来转换。

### `run()` 方法

```python
    def run(self, parent: Element, blocks: List[str]) -> Optional[bool]:
        if not blocks:
            return False
        match = self.PATTERN.match(blocks[0])
        if not match:
            return False
        
        # 去掉匹配部分，剩下的内容会作为内部块内容
        blocks[0] = blocks[0][match.end():]
        admonition_type = match.group(1).lower()  # 统一转换为小写

        # 将原来的 blockquote 改为 div，并设置 CSS 类方便样式定制
        parent.tag = "div"
        parent.set("class", f"admonition {admonition_type}")

        # 添加一个标题子节点
        title = SubElement(parent, "p")
        title.set("class", "admonition-title")
        title.text = admonition_type.capitalize()

        # 将剩余块内容继续解析到这个 div 中
        self.parser.parseBlocks(parent, blocks)
        blocks.clear()

        return True
```

必要性：
**`run` 方法也是 BlockProcessor 必须实现的**。当 `test()` 返回 True 后，`run()` 负责实际处理这个块，把 Markdown 转换成 HTML 元素。

详细说明：

1. **检查块是否为空**

   ```python
   if not blocks:
       return False
   ```

   如果没有可处理的块，返回 `False`，表示该处理器没有执行操作。

2. **匹配正则**

   ```python
   match = self.PATTERN.match(blocks[0])
   if not match:
       return False
   ```

   再次验证是否匹配预期格式（防御性检查），确保取到有效的 `match` 对象。

3. **更新块内容**

   

   ```python
   blocks[0] = blocks[0][match.end():]
   ```

   剔除掉标记 `[!note]` 部分，剩余部分（如标注的内容）仍需解析。这样后续 `self.parser.parseBlocks` 可以正确处理后续内容。

4. **获取类型**

   

   ```python
   admonition_type = match.group(1).lower()
   ```

   从正则捕获组中取得 admonition 类型（例如 note、tip 等），并转换为小写，方便后续设置样式类。

5. **修改父节点**

   

   ```python
   parent.tag = "div"
   parent.set("class", f"admonition {admonition_type}")
   ```

   - 将原本是 `<blockquote>` 的父节点改为 `<div>`，通常这种结构更符合 HTML 语义。
   - 设置 `class` 属性，既包含通用的 `admonition` 类，也包含特定类型（如 `note`），便于通过 CSS 定制样式。

6. **添加标题子节点**

   ```python
   title = SubElement(parent, "p")
   title.set("class", "admonition-title")
   title.text = admonition_type.capitalize()
   ```

   - 使用 `SubElement` 在父节点中创建一个 `<p>` 标签作为“标题”。
   - 设置类名 `admonition-title`（你可以在 CSS 中为这个类定义特殊样式）。
   - 将文本内容设置为类型名称的首字母大写形式（例如 “Note”）。

7. 继续解析剩余块

   ```python
   self.parser.parseBlocks(parent, blocks)
   ```

   把剩余的块内容继续解析为该 `<div>` 的子元素，这保证多行内容也能正确转换为 HTML。

8. 清空块列表并返回

   ```python
   blocks.clear()
   return True
   ```

   清理已处理的块，并返回 `True` 表示该块已被成功处理。

## `makr_Extension` 工厂函数

```python
def make_Extension(**kwargs):
    return Gfm_Admonition_Extension(**kwargs)
```

作用：
这是一个工厂函数，用于产生扩展的实例。

必要性：
虽然你可以直接实例化扩展类，但很多 Markdown 工具和配置方式要求模块中暴露一个名为 `makeExtension`（或类似）的函数。当用户通过类似配置字符串的方式引入扩展时，Markdown 库会调用这个工厂函数生成扩展实例。

为什么使用工厂函数：
通过工厂函数可以统一管理创建实例时所需的参数，且有助于将来扩展或调整初始化逻辑，所以这也是一种常见的设计模式。