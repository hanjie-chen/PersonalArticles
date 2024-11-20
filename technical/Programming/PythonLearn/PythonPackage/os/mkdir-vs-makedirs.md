# Python目录创建操作：os.mkdir vs os.makedirs 详解

## 1. 基本概念对比

### 1.1 os.mkdir(path, mode=0o777)
- 只能创建一级目录
- 父目录必须存在，否则报错
- 目录已存在时会报错
- 没有parents参数

### 1.2 os.makedirs(path, mode=0o777, exist_ok=False)
- 可以创建多级目录（包括所有必要的父目录）
- 父目录不需要预先存在
- 通过exist_ok参数控制目录已存在时的行为
- 更安全、更灵活

## 2. 使用场景对比

### 2.1 os.mkdir() 适用场景
```python
# 当确定只需要创建一级目录，且父目录已存在时
os.mkdir("downloads")
os.mkdir("temp")
```

### 2.2 os.makedirs() 适用场景
```python
# 创建多级目录结构
os.makedirs("data/raw/2024/01", exist_ok=True)

# 不确定父目录是否存在的情况
os.makedirs("output/logs", exist_ok=True)

# 需要安全地创建目录
os.makedirs("cache", exist_ok=True)
```

## 3. exist_ok 参数详解

### 3.1 exist_ok=False（默认值）
```python
# 目录不存在时：创建成功
# 目录存在时：抛出 FileExistsError
try:
    os.makedirs("existing_folder")
except FileExistsError:
    print("目录已存在！")
```

### 3.2 exist_ok=True
```python
# 目录不存在时：创建成功
# 目录存在时：静默跳过，继续执行
os.makedirs("existing_folder", exist_ok=True)  # 不会报错
```

## 4. 实用代码示例

### 4.1 安全的目录创建函数
```python
def ensure_directory_exists(path):
    """确保目录存在，如果不存在则创建"""
    os.makedirs(path, exist_ok=True)
```

### 4.2 批量处理目录
```python
directories = [
    "output/images",
    "output/logs",
    "output/data",
    "output/temp"
]

for dir_path in directories:
    os.makedirs(dir_path, exist_ok=True)
```

### 4.3 项目结构设置
```python
def setup_project_structure(base_path):
    """设置项目目录结构"""
    directories = [
        "src",
        "tests",
        "docs",
        "data/raw",
        "data/processed",
        "output/logs",
        "output/results"
    ]
    
    for dir_name in directories:
        full_path = os.path.join(base_path, dir_name)
        os.makedirs(full_path, exist_ok=True)
```

## 5. 最佳实践建议

1. **一般情况**：
   - 优先使用 `os.makedirs(path, exist_ok=True)`
   - 这是最安全和通用的方式

2. **特殊情况**：
   - 当确定只需创建单级目录且父目录存在时，可以使用 `os.mkdir()`
   - 需要精确控制目录创建过程时，使用 `os.makedirs(path, exist_ok=False)` 并做好错误处理

3. **错误处理**：
```python
def setup_directory(path):
    """安全地设置目录"""
    os.makedirs(path, exist_ok=True)
    return os.path.exists(path)  # 确认目录确实存在
```

## 6. 补充说明
除了 os.mkdir 和 os.makedirs，还可以使用 pathlib.Path 的 mkdir() 方法，这是最现代的方式：
```python
from pathlib import Path

# 创建单个目录
Path("new_folder").mkdir()

# 创建多级目录
Path("parent/child/grandchild").mkdir(parents=True)
```

这个笔记涵盖了我们讨论的所有重要内容，并按照易于理解和查找的方式组织。您可以根据需要随时参考特定部分。