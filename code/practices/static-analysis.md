# Static Analysis

静态代码分析，也就是不运行程序，仅仅阅读代码，就尝试发现问题。

比如写：

```python
import os

name = "Alice"

print(username)
```

Python 真正运行到 `print(username)` 的时候，才会报 `NameError: name 'username' is not defined`

但静态分析工具可以在程序运行之前扫描源代码，然后告诉你：`username not defined`

这就是 Static Analysis。它叫“静态”，是因为：看代码，不运行代码。

而相对的，Dynamic Analysis，则是真正运行程序，观察运行结果，比如说 pytest 测试。

### lint

Lint 可以理解成：静态代码分析的一种，主要检查代码中可疑、不规范、容易出错的地方。

例如：

```python
import os

x = 10
```

`os` 根本没使用。程序完全可以正常运行，但这个 import 没意义。Linter 就可能告诉你：`F401 os imported but unused`

再比如：

```python
def hello():
    x = 123
    return "hello"
```

`x` 创建了，但是没有使用：`F841 Local variable x is assigned to but never used`

### ruff

Ruff 是现在 Python 生态里非常主流的一套代码质量工具，由 Astral 开发。

它最核心有两个功能：

- ruff check: Linter,检查代码问题
- ruff format: Formatter, 自动整理代码格式

所以以前一个 Python 项目可能是：

```
flake8       → lint
isort        → import 排序
black        → format
pyupgrade    → 检查旧 Python 写法
autoflake    → 删除没用的 import
```

现在很多项目可以简化成：

```
Ruff
├── ruff check
└── ruff format
```

#### what is `F401` ?

`F401` 不是错误编号随机生成的，它叫 lint rule

例如：

```
F401
│ │
│ └── 401：具体规则编号
│
└── F：规则类别
```

`F401` 的含义就是：imported-but-unused（import 了一个东西，但是没有使用）

Ruff 内部有大量类似规则。例如你以后会经常看到：

```
F401
F841
E501
B006
UP035
RUF...
```

它们来自不同的 rule family。

暂时不用背。

你只需要理解：

```
ruff check
    ↓
扫描代码
    ↓
拿代码和几百条规则比较
    ↓
发现违反某条规则
    ↓
报告 rule code
```

Ruff 官方目前支持 900+ 条规则，而且很多规则源自 Flake8、isort、pyupgrade 等工具，但 Ruff 自己用 Rust 重新实现。