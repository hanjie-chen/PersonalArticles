# Unicode string & UTF-8

1. **Unicode String vs UTF-8**
- Unicode string 是一个抽象的概念，它是字符的序列，每个字符都有一个唯一的编码点(code point)
- UTF-8 是 Unicode 的一种具体编码实现方式，是一种将 Unicode 字符编码成字节序列的方法

2. **在 Python 中的体现**
- Python 中的 str 类型就是 Unicode 字符串
- 当我们从文件读取时，文件中的内容是以特定编码（如 UTF-8）存储的字节序列
- 使用 `open()` 时指定 `encoding='utf-8'`，Python 会自动将 UTF-8 编码的字节转换为 Unicode 字符串

3. **举例说明**
```python
# 从文件读取（UTF-8编码的字节 -> Unicode字符串）
with open("file.txt", "r", encoding="utf-8") as f:
    text = f.read()  # text现在是Unicode字符串(str类型)

# 写入文件（Unicode字符串 -> UTF-8编码的字节）
with open("output.html", "w", encoding="utf-8") as f:
    f.write(text)
```

简单来说：
- UTF-8 是编码方式（存储格式）
- Unicode string 是 Python 中的字符串表示方式（内存中的格式）
- 使用 `encoding="utf-8"` 是将 UTF-8 编码的文件内容转换为 Python 的 Unicode 字符串的过程

所以，UTF-8 和 Unicode string 不是一回事，而是通过编码转换建立关联的两个概念。当我们使用 `encoding="utf-8"` 打开文件时，Python 会自动处理这个转换过程，确保我们在程序中使用的是 Unicode 字符串。

# something related

[Library Reference — Python-Markdown 3.7 documentation](https://python-markdown.github.io/reference/#markdown)

`markdown.markdown()` 函数的第一个参数需要 unicode 字符串（Python 的 str 类型）