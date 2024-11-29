感谢您提供这些详细的源代码信息。让我为您分析一下 frontmatter 库中关于 YAML 解析的关键部分。

在 `frontmatter/default_handlers.py` 文件中，我们可以看到 `YAMLHandler` 类的实现：

```python
class YAMLHandler(BaseHandler):
    FM_BOUNDARY = re.compile(r"^-{3,}\s*$", re.MULTILINE)
    START_DELIMITER = END_DELIMITER = "---"

    def load(self, fm: str, **kwargs: object) -> Any:
        """
        Parse YAML front matter. This uses yaml.SafeLoader by default.
        """
        kwargs.setdefault("Loader", SafeLoader)
        return yaml.load(fm, **kwargs)  # type: ignore[arg-type]

    def export(self, metadata: dict[str, object], **kwargs: object) -> str:
        """
        Export metadata as YAML. This uses yaml.SafeDumper by default.
        """
        kwargs.setdefault("Dumper", SafeDumper)
        kwargs.setdefault("default_flow_style", False)
        kwargs.setdefault("allow_unicode", True)

        metadata_str = yaml.dump(metadata, **kwargs).strip()  # type: ignore[call-overload]
        return u(metadata_str)  # ensure unicode
```

这段代码确认了我们之前的分析：

1. YAML 解析默认使用 `yaml.SafeLoader`：在 `load` 方法中，我们可以看到 `kwargs.setdefault("Loader", SafeLoader)`。这意味着如果没有指定其他加载器，frontmatter 将使用 PyYAML 的 `SafeLoader`。[1]

2. 自动类型转换：`yaml.load(fm, **kwargs)` 会使用 PyYAML 的 `safe_load` 功能。这个函数会自动将某些 YAML 标量（如日期、时间等）转换为相应的 Python 对象。[1]

3. 导出时的设置：在 `export` 方法中，我们可以看到一些默认设置，如 `default_flow_style=False` 和 `allow_unicode=True`。这些设置影响 YAML 的输出格式。[1]

此外，在文件顶部，我们可以看到：

```python
try:
    from yaml import CSafeDumper as SafeDumper
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeDumper
    from yaml import SafeLoader
```

这段代码表明，frontmatter 优先使用 PyYAML 的 C 扩展版本（如果可用），这可以提高性能。如果 C 扩展版本不可用，它会退回到纯 Python 实现。[1]

关于日期的自动解析，这实际上是由 PyYAML 的 `SafeLoader` 处理的。PyYAML 的 `SafeLoader` 会自动识别和解析符合特定格式的日期字符串。这就是为什么您看到 `RolloutDate` 已经被转换为 `datetime.date` 类型的原因。[6]

