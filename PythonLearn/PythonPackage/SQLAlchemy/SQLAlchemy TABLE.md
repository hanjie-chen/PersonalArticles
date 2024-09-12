# SQLAlchemy TABLE



# SQLAlchemy Core define

使用 Table 对象直接定义表结构，例如

```python
from sqlalchemy import Table, Column, Integer, String, MetaData

metadata_obj = MetaData()
user_table = Table(
  "user_account",
  metadata_obj,
  Column("id", Integer, primary_key=True),
  Column("name", String(30)),
  # ... 其他字段
)
```





# SQLAlchemy Declarative define

```python
from sqlalchemy.orm import DeclarativeBase
class Base(DeclarativeBase):
    pass
```

## 关于空的Base类

通过定义自己的 `Base` 类，可以在将来添加自定义方法或属性，这些将被所有模型类继承，提供了更多的灵活性和可扩展性。这种方法允许您在将来轻松地向所有模型添加共同的功能，而不需要修改每个单独的模型类。例如，为所有表添加一个 `created_at` 列：

   ```python
   from sqlalchemy.orm import DeclarativeBase
   from sqlalchemy import Column, DateTime
   from datetime import datetime

   class Base(DeclarativeBase):
       created_at = Column(DateTime, default=datetime.utcnow)
   ```

在大型项目中，可以将 `Base` 类定义在一个单独的文件中（如 `database.py`）可以提高代码的组织性。这样，您可以在其他文件中导入 `Base`，而不是每次都导入 `DeclarativeBase`。

还可以在 `Base` 类中添加元数据配置或其他 SQLAlchemy 相关的设置。

### 旧版本SQLAlchemy：

值得注意的是，SQLAlchemy 在不同版本中对声明式基类的处理有所变化：

- 在旧版本中，使用 `declarative_base()` 函数来创建基类。
- 在 SQLAlchemy 2.0 中，引入了 `DeclarativeBase` 类。

定义自己的 `Base` 类的做法部分源于早期版本的习惯，并且在新版本中仍然保留了这种灵活性。

# Flask-SQLAlchemy Table define VS SQLAlchemy Table define

## 1. Flask-SQLAlchemy 定义方式

- 使用 Python 类来定义数据库表（声明式基类方法）
- 继承自 `db.Model`
- 示例：

```python
class Article_Meta_Data(db.Model):
  __tablename__ = 'article_meta_date'
  id = db.Column(db.Integer, primary_key = True)
  title = db.Column(db.String(100), nullable = False)
  # ... 其他字段
```



## 3. SQLAlchemy ORM 定义方式

- 类似于 Flask-SQLAlchemy，但不依赖 Flask
- 使用 DeclarativeBase
- 示例：

```python
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String

class Base(DeclarativeBase):
  pass

class User(Base):
  __tablename__ = 'user_account'
  id = Column(Integer, primary_key=True)
  name = Column(String(30))
  # ... 其他字段
```

## 4. 关键点

- Flask-SQLAlchemy 是 SQLAlchemy 的扩展，简化了在 Flask 中的使用
- Flask-SQLAlchemy 和 SQLAlchemy ORM 都使用声明式模型定义
- SQLAlchemy Core 提供更底层的表定义方式
- 声明式模型（Flask-SQLAlchemy/SQLAlchemy ORM）提供更 Pythonic 和面向对象的方式
- 选择取决于具体需求和偏好，Flask 应用中通常选择 Flask-SQLAlchemy

## 5. 优势比较

| 方式             | 优势                                   |
| ---------------- | -------------------------------------- |
| Flask-SQLAlchemy | 简化 Flask 集成，更高级的抽象          |
| SQLAlchemy ORM   | 独立于 Flask，适用于各种 Python 应用   |
| SQLAlchemy Core  | 更细粒度的控制，适合复杂查询和性能优化 |



# Flask-SQLAlchemy Table define VS SQLAlchemy Table define

## 1. Flask-SQLAlchemy 定义方式

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
```

## 2. SQLAlchemy ORM (Declarative) 定义方式

```python
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String

class Base(DeclarativeBase):
  pass

class User(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True)
  username = Column(String(80), unique=True, nullable=False)
  email = Column(String(120), unique=True, nullable=False)
```

## 3. 相似性和差异

### 相似点：
1. 都使用 Python 类来定义数据库表
2. 类属性用于定义表的列
3. 使用特殊的 `__tablename__` 属性来指定表名
4. 列的定义方式非常相似（如 `Column(Integer, primary_key=True)`）

### 主要差异：
1. **基类不同**：
 - Flask-SQLAlchemy: 继承自 `db.Model`
 - SQLAlchemy ORM: 继承自自定义的 `Base` 类（通常是 `DeclarativeBase` 的子类）

2. **导入和设置**：
 - Flask-SQLAlchemy: 需要先创建 `SQLAlchemy` 实例（`db = SQLAlchemy()`）
 - SQLAlchemy ORM: 直接使用 SQLAlchemy 的类和函数

3. **列定义的简写**：
 - Flask-SQLAlchemy: 可以使用 `db.Column`，`db.Integer` 等简写形式
 - SQLAlchemy ORM: 通常使用完整导入，如 `Column`，`Integer` 等

4. **与 Flask 的集成**：
 - Flask-SQLAlchemy: 提供了与 Flask 应用更紧密的集成
 - SQLAlchemy ORM: 需要额外的设置来与 Flask 集成

## 4. 为什么如此相似？

1. **Flask-SQLAlchemy 是 SQLAlchemy 的扩展**：
 Flask-SQLAlchemy 构建在 SQLAlchemy 之上，保留了大部分 SQLAlchemy 的语法和功能。

2. **简化的目标**：
 Flask-SQLAlchemy 旨在简化 SQLAlchemy 在 Flask 应用中的使用，但不改变其核心概念和语法。

3. **一致性考虑**：
 保持与原生 SQLAlchemy 相似的语法可以降低学习曲线，使开发者更容易在不同项目间切换。

## 5. 选择建议

- 如果你正在开发一个 Flask 应用，使用 Flask-SQLAlchemy 通常是更好的选择，因为它提供了更好的 Flask 集成。
- 如果你的项目不依赖于 Flask，或者你需要在不同类型的项目中重用数据库模型，使用原生 SQLAlchemy 可能更合适。
- 两者的核心概念和使用方式非常相似，学会一个后很容易转换到另一个。