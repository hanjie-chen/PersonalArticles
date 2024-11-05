#### 为什么 `frontmatter` 不自动将日期字符串转换为 `date` 对象？

默认情况下，`frontmatter` 使用了 `safe_load`：

- `PyYAML` 的 `safe_load` 方法只解析基本的数据类型，例如字符串、整数、列表、字典等。
- 不会自动解析日期字符串为 `date` 或 `datetime` 对象。
- 这样做是为了防止加载可能存在安全风险的自定义对象。

您可以选择使用 `full_load`，但不建议：

- `full_load` 方法可以解析更多的数据类型，包括日期、时间等。
- 但是使用 `full_load` 存在安全风险，可能会执行任意的代码，导致安全问题。
- 因此，**不建议**在未完全信任的环境中使用 `full_load`。

最佳实践是手动解析日期字符串：

- 这样可以确保代码的安全性和可控性。
- 也能够根据需要调整日期格式和解析方式。

***

如果您希望深入了解 `PyYAML` 对日期等高级数据类型的处理，可以参考以下信息：

**`PyYAML` 的日期解析：**

- 在使用 `yaml.load` 或 `yaml.full_load` 时，`PyYAML` 会尝试将符合 YAML 日期格式的字符串解析为 `datetime.datetime` 对象。
- 例如，`2024-09-19` 会被解析为 `datetime.datetime(2024, 9, 19, 0, 0)`。

安全风险：

- 使用 `yaml.full_load` 或 `yaml.load`（未指定 Loader）可能会加载任意的 YAML 标签，导致执行任意代码的风险。
- 因此，`yaml.safe_load` 是推荐的解析方法。

示例：

如果您想尝试使用 `yaml.full_load` 来自动解析日期，可以进行如下测试：

```
pythonCopyimport yaml

yaml_content = '''
RolloutDate: 2024-09-19
'''

data = yaml.full_load(yaml_content)
print(data)
print(type(data['RolloutDate']))
```

输出：

```
arduinoCopy{'RolloutDate': datetime.datetime(2024, 9, 19, 0, 0)}
<class 'datetime.datetime'>
```

- 可以看到，`RolloutDate` 被解析为了 `datetime.datetime` 对象。
- **但是**，强烈建议不要在生产环境中使用 `yaml.full_load`，除非您完全信任数据的来源。