# Python Type Annotations

在 Python 中，冒号(`:`)有多种用途，其中最常见的包括类型注解、代码块定义和字典/切片操作。

## 1. 类型注解 (Type Annotations)

类型注解是 Python 3.5+ 引入的特性，用于指定变量、函数参数和返回值的预期类型。

### 基本语法：

```python
variable: type
```

### 示例：

```python
# 变量注解
x: int = 5
name: str = "Alice"

# 函数参数和返回值注解
def greet(name: str) -> str:
    return f"Hello, {name}"

# 复杂类型注解
from typing import List, Dict
numbers: List[int] = [1, 2, 3]
user_scores: Dict[str, int] = {"Alice": 95, "Bob": 87}
```

### 在 SQLAlchemy 中的应用：

```python
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
```

### 注意事项：
- 类型注解不影响运行时行为
- 主要用于静态类型检查、代码可读性和 IDE 支持
- 可以使用 mypy 等工具进行静态类型检查

## 2. 代码块定义

冒号用于定义代码块，如函数、类、循环和条件语句。

### 示例：

```python
# 函数定义
def say_hello():
    print("Hello")

# 类定义
class Person:
    def __init__(self, name):
        self.name = name

# 条件语句
if x > 0:
    print("Positive")

# 循环
for i in range(5):
    print(i)
```

## 3. 字典和切片操作

### 字典定义：

```python
person = {"name": "Alice", "age": 30}
```

### 列表切片：

```python
numbers = [0, 1, 2, 3, 4, 5]
subset = numbers[1:4]  # [1, 2, 3]
```

## 总结

- 类型注解（`:type`）：指定变量或参数的预期类型
- 代码块定义：用于函数、类、循环和条件语句
- 字典和切片：用于创建字典和进行列表切片操作

记住，类型注解在语法上类似于 C 语言的类型声明，但在 Python 中是可选的，不会强制执行类型检查。它们主要用于提高代码可读性、支持静态类型检查工具和增强 IDE 功能。