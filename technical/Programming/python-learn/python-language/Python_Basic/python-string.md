# 切片操作

从第一个字符开始截取到末尾

```python
# 使用 [1:] 从索引1开始截取到末尾
text = "Hello"
new_text = text[1:]  # 结果: "ello"
```

# f-string

Python 的 f-string（格式化字符串字面值），是 Python 3.6+ 引入的一个很方便的特性。

让我详细解释一下：

**基本语法**：

```python
name = "Alice"
age = 25
# f-string的用法
message = f"My name is {name} and I am {age} years old"
# 输出：My name is Alice and I am 25 years old
```

**f-string 的其他功能**：

```python
# 可以在{}中使用表达式
x = 10
print(f"2倍是 {x * 2}")  # 输出：2倍是 20

# 可以调用函数
name = "python"
print(f"大写: {name.upper()}")  # 输出：大写: PYTHON

# 可以格式化数字
price = 123.456
print(f"价格: {price:.2f}")  # 输出：价格: 123.46

# 可以使用字典
data = {"name": "Bob", "age": 30}
print(f"姓名: {data['name']}")  # 输出：姓名: Bob
```

**一些高级用法**：

```python
# 对齐和填充
number = 42
print(f"{number:0>5}")  # 输出：00042

# 使用变量说明符
debug = True
print(f"{number=}")  # 输出：number=42

# 表达式中使用引号
print(f"{'quoted'}")  # 输出：quoted

# 多行f-string
message = f"""
名字: {name}
年龄: {age}
"""
```

# `split()` function

`split()` 函数 Python String 对象的一个非常有用的内置方法。它的主要功能是将字符串分割成一个列表，其中每个元素都是原字符串的一个子串。

## basic grammer

```python
str.split(sep = None, maxsplit =-1)
```

- sep: 分隔符，默认为 None
- maxsplit: 最大分割次数，默认为-1（表示不限制）

## parameter

如果不指定任何参数，split()会使用空白字符（空格、制表符、换行符等）作为分隔符，并且会删除字符串开头和结尾的空白字符。

```python
text = "  Hello  World  Python  "
result = text.split()
print(result)  # 输出: ['Hello', 'World', 'Python']
```

### sep parameter

可以指定一个字符串作为分隔符，例如：

```python
text = "apple,banana,orange,grape"
result = text.split(',')
print(result)  # 输出: ['apple', 'banana', 'orange', 'grape']
```

### maxsplit parameter

可以限制分割的次数，例如：

```python
text = "one two three four five"
result = text.split(' ', 2)
print(result)  # 输出: ['one', 'two', 'three four five']
```

# raw string

r-prefix 的作用

在 Python 中, 字符串前面加上字母 `r` 表示原始字符串(raw string), 它的作用是告诉 Python 解释器这个字符串是原始的, 不需要进行转义处理。在正则表达式中, 我们经常需要使用一些特殊字符, 如 `\d` 表示数字、`\s` 表示空白字符等。但是在 Python 的普通字符串中, `\` 本身也是一个转义字符。为了避免 `\` 被当做转义字符处理, 我们可以在正则表达式字符串前面加上 `r` 前缀, 表示这是一个原始字符串。例如:

```python
pattern1 = '\\d{3}'  # 需要使用\\转义\
pattern2 = r'\d{3}'  # 使用r前缀,不需要转义
```

`pattern1` 和 `pattern2` 表示的是同一个正则表达式, 但是使用 `r` 前缀更加简洁明了

# `strip()` funciton

`strip()` 是Python字符串的一个内置方法,用于去除字符串首尾的空白字符(包括空格、制表符、换行符等)。语法如下:

```python
str.strip([chars])
```

- 如果不传参数,默认去除首尾的空白字符
- 如果传入参数`chars`,则去除首尾所有属于`chars`的字符

e.g.

```python
text = '  hello world!  \n'
print(text.strip())  # 输出 'hello world!'

text = 'www.example.com'
print(text.strip('wmco.'))  # 输出 'example'
```

# `lstrip()` function

lstrip() 是Python字符串对象的内置方法,用于返回原字符串的一个副本,其中前导空格或指定字符被移除。函数语法:

```python
str.lstrip([chars])
```

参数说明:

- `chars` (可选):指定要移除的字符集合,默认为空格。

函数返回一个新的字符串,原字符串保持不变。

#### 使用示例

不带参数使用lstrip(),移除字符串前面的空格:

```python
text = "   Hello, world!   "
print(text.lstrip())  # 输出: "Hello, world!   "
```

指定要移除的字符:

```python
text = "www.example.com"
print(text.lstrip("w."))  # 输出: "example.com"
```

上例中,"w."作为参数传给lstrip(),它将移除字符串开头的所有'w'和'.'字符。

#### 注意事项

- lstrip()只移除字符串开头(左侧)的指定字符,字符串末尾的字符不受影响。
- 如果不指定chars参数,lstrip()默认移除空格,包括空格符、制表符和换行符等。
- 要同时去除字符串两端的空格或指定字符,可以使用**strip()**方法。
- 要只去除字符串末尾的空格或指定字符,可以使用**rstrip()**方法。
