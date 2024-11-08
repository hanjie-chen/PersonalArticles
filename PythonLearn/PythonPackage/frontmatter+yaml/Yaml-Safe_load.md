# Yaml Safe_load

首先，PyYAML 的官方 GitHub 仓库是 https://github.com/yaml/pyyaml。这是查找源代码的最佳起点。[1]

要查看 `safe_load` 的具体实现，您需要查看 PyYAML 仓库中的以下文件：

1. `lib/yaml/__init__.py`：这个文件包含了 `safe_load` 函数的定义。
2. `lib/yaml/constructor.py`：这个文件包含了 `SafeConstructor` 类，它负责实际的 YAML 解析过程。
3. `lib/yaml/loader.py`：这个文件定义了 `SafeLoader` 类，它使用 `SafeConstructor` 来加载 YAML 数据。

以下是 `safe_load` 函数的大致实现（在 `__init__.py` 中）：

```python
def safe_load(stream):
    """
    Parse the first YAML document in a stream
    and produce the corresponding Python object.
    Resolve only basic YAML tags.
    """
    return load(stream, SafeLoader)
```

这个函数实际上是调用了 `load` 函数，但使用了 `SafeLoader` 作为加载器。[1]

`SafeLoader` 类（在 `loader.py` 中）继承自 `Reader`、`Scanner`、`Parser`、`Composer`、`SafeConstructor` 和 `Resolver`。其中，`SafeConstructor` 是关键，它定义了如何构造 Python 对象。[1]

在 `constructor.py` 中，`SafeConstructor` 类定义了一系列的 `construct_*` 方法，用于处理不同类型的 YAML 标签。

值得注意的是，`safe_load` 只处理一个基本的 YAML 子集，不包括可能导致任意代码执行的复杂结构。这就是为什么它被认为是"安全"的。[3]

也就是说其中constructor.py这个文件中，是真正的关于safe_load的源代码

其路径为：[pyymal csontructor.py](https://github.com/yaml/pyyaml/blob/main/lib/yaml/constructor.py)



# 日期和时间的转换

在 `SafeConstructor` 类中，有一个 `construct_yaml_timestamp` 方法负责处理日期和时间的转换。这个方法使用正则表达式来匹配 YAML 中的时间戳格式：

```python
timestamp_regexp = re.compile(
    r'''^(?P<year>[0-9][0-9][0-9][0-9])
        -(?P<month>[0-9][0-9]?)
        -(?P<day>[0-9][0-9]?)
        (?:(?:[Tt]|[ \t]+)
        (?P<hour>[0-9][0-9]?)
        :(?P<minute>[0-9][0-9])
        :(?P<second>[0-9][0-9])
        (?:\.(?P<fraction>[0-9]*))?
        (?:[ \t]*(?P<tz>Z|(?P<tz_sign>[-+])(?P<tz_hour>[0-9][0-9]?)
        (?::(?P<tz_minute>[0-9][0-9]))?))?)?$''', re.X)
```

这个正则表达式可以匹配以下格式：
- 仅日期：YYYY-MM-DD
- 日期和时间：YYYY-MM-DD HH:MM:SS
- 带微秒的日期和时间：YYYY-MM-DD HH:MM:SS.ffffff
- 带时区的日期和时间：YYYY-MM-DD HH:MM:SS±HH:MM

在 `construct_yaml_timestamp` 方法中，根据匹配结果创建相应的 Python 对象：

```python
def construct_yaml_timestamp(self, node):
    value = self.construct_scalar(node)
    match = self.timestamp_regexp.match(node.value)
    values = match.groupdict()
    year = int(values['year'])
    month = int(values['month'])
    day = int(values['day'])
    if not values['hour']:
        return datetime.date(year, month, day)
    # ... (处理时间部分的代码)
    return datetime.datetime(year, month, day, hour, minute, second, fraction, tzinfo=tzinfo)
```

如您所见，当只有日期部分时（YYYY-MM-DD），它会返回一个 `datetime.date` 对象。如果包含时间部分，则返回一个 `datetime.datetime` 对象。

# 其他特殊类型的转换

除了日期和时间，`SafeConstructor` 还定义了其他几种特殊类型的转换：

a. 空值（Null）:
```python
def construct_yaml_null(self, node):
    self.construct_scalar(node)
    return None
```

b. 布尔值：
```python
bool_values = {
    'yes':      True,
    'no':       False,
    'true':     True,
    'false':    False,
    'on':       True,
    'off':      False,
}

def construct_yaml_bool(self, node):
    value = self.construct_scalar(node)
    return self.bool_values[value.lower()]
```

c. 整数：
```python
def construct_yaml_int(self, node):
    value = self.construct_scalar(node)
    value = value.replace('_', '')
    sign = +1
    if value[0] == '-':
        sign = -1
    if value[0] in '+-':
        value = value[1:]
    if value == '0':
        return 0
    elif value.startswith('0b'):
        return sign*int(value[2:], 2)
    elif value.startswith('0x'):
        return sign*int(value[2:], 16)
    elif value[0] == '0':
        return sign*int(value, 8)
    elif ':' in value:
        digits = [int(part) for part in value.split(':')]
        digits.reverse()
        base = 1
        value = 0
        for digit in digits:
            value += digit*base
            base *= 60
        return sign*value
    else:
        return sign*int(value)
```

d. 浮点数：
```python
def construct_yaml_float(self, node):
    value = self.construct_scalar(node)
    value = value.replace('_', '').lower()
    sign = +1
    if value[0] == '-':
        sign = -1
    if value[0] in '+-':
        value = value[1:]
    if value == '.inf':
        return sign*self.inf_value
    elif value == '.nan':
        return self.nan_value
    elif ':' in value:
        digits = [float(part) for part in value.split(':')]
        digits.reverse()
        base = 1
        value = 0.0
        for digit in digits:
            value += digit*base
            base *= 60
        return sign*value
    else:
        return sign*float(value)
```

e. 二进制数据：
```python
def construct_yaml_binary(self, node):
    try:
        value = self.construct_scalar(node).encode('ascii')
    except UnicodeEncodeError as exc:
        raise ConstructorError(None, None,
                "failed to convert base64 data into ascii: %s" % exc,
                node.start_mark)
    try:
        if hasattr(base64, 'decodebytes'):
            return base64.decodebytes(value)
        else:
            return base64.decodestring(value)
    except binascii.Error as exc:
        raise ConstructorError(None, None,
                "failed to decode base64 data: %s" % exc, node.start_mark)
```

这些方法被注册为特定 YAML 标签的构造器：

```python
SafeConstructor.add_constructor(
        'tag:yaml.org,2002:null',
        SafeConstructor.construct_yaml_null)

SafeConstructor.add_constructor(
        'tag:yaml.org,2002:bool',
        SafeConstructor.construct_yaml_bool)

SafeConstructor.add_constructor(
        'tag:yaml.org,2002:int',
        SafeConstructor.construct_yaml_int)

SafeConstructor.add_constructor(
        'tag:yaml.org,2002:float',
        SafeConstructor.construct_yaml_float)

SafeConstructor.add_constructor(
        'tag:yaml.org,2002:binary',
        SafeConstructor.construct_yaml_binary)

SafeConstructor.add_constructor(
        'tag:yaml.org,2002:timestamp',
        SafeConstructor.construct_yaml_timestamp)
```

总结：
1. 日期（YYYY-MM-DD）被转换为 `datetime.date` 对象。
2. 完整的时间戳被转换为 `datetime.datetime` 对象。
3. 布尔值（true, false, yes, no, on, off）被转换为 Python 的 `bool` 类型。
4. 整数可以是十进制、十六进制、八进制或者基于60的格式。
5. 浮点数包括普通浮点数、无穷大和 NaN。
6. 二进制数据使用 Base64 编码，并被解码为字节串。

这些转换确保了 YAML 数据可以被安全地加载为相应的 Python 对象，而不会执行任何潜在的危险代码。