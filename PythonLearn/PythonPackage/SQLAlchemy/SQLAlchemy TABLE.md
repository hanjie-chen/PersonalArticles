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





# SQLAlchemy Declarative Mapped define

```python
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy import MetaData
from sqlalchemy import text
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    addresses: Mapped[List["Address"]] = relationship(back_populates="user")
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id = mapped_column(ForeignKey("user_account.id"))
    user: Mapped[User] = relationship(back_populates="addresses")
    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

Base.metadata.create_all(engine)
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

## Annotated Declarative Mapping (new feature for 2.0)

### Mapped 和 mapped_column

`Mapped` 和 `mapped_column` 是 SQLAlchemy 2.0 中的新概念：

- `Mapped[T]` 是一个类型提示，表示这个属性将被映射到数据库列。
- `mapped_column()` 函数用于定义列的具体属性。

### 代码解析

```python
class User(Base):
    __tablename__ = "user_account"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    addresses: Mapped[List["Address"]] = relationship(back_populates="user")
```

- `id: Mapped[int] = mapped_column(primary_key=True)`: 定义一个整数类型的主键列。
- `name: Mapped[str] = mapped_column(String(30))`: 定义一个最大长度为30的字符串列。
- `fullname: Mapped[Optional[str]]`: 定义一个可为空的字符串列。注意这里没有使用 `mapped_column()`，SQLAlchemy 会使用默认设置。
- `addresses: Mapped[List["Address"]] = relationship(...)`: 定义一个到 `Address` 模型的一对多关系。

```python
class Address(Base):
    __tablename__ = "address"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id = mapped_column(ForeignKey("user_account.id"))
    user: Mapped[User] = relationship(back_populates="addresses")
```

- `email_address: Mapped[str]`: 定义一个非空字符串列。
- `user_id = mapped_column(ForeignKey("user_account.id"))`: 定义一个外键列。注意这里没有使用 `Mapped`，因为它不是直接映射到模型属性的。
- `user: Mapped[User] = relationship(...)`: 定义到 `User` 模型的多对一关系。

### 与旧版本定义方式

在旧版本的 SQLAlchemy 中，您可能会看到这样的代码：

```python
class User(Base):
    __tablename__ = "user_account"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    fullname = Column(String)
    addresses = relationship("Address", back_populates="user")
```

新版本的主要区别在于使用了类型注解和 `Mapped` 类型，使得代码更加明确和类型安全。不过，SQLAlchemy 2.0 仍然支持旧的定义方式，所以您可能会在不同的项目中看到不同的风格。新的方式是推荐的，特别是对于新项目。

## 运行结果

```bash
2024-09-13 10:11:23,848 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2024-09-13 10:11:23,848 INFO sqlalchemy.engine.Engine PRAGMA main.table_info("user_account")
2024-09-13 10:11:23,848 INFO sqlalchemy.engine.Engine [raw sql] ()
2024-09-13 10:11:23,849 INFO sqlalchemy.engine.Engine PRAGMA temp.table_info("user_account")
2024-09-13 10:11:23,849 INFO sqlalchemy.engine.Engine [raw sql] ()
2024-09-13 10:11:23,849 INFO sqlalchemy.engine.Engine PRAGMA main.table_info("address")
2024-09-13 10:11:23,849 INFO sqlalchemy.engine.Engine [raw sql] ()
2024-09-13 10:11:23,850 INFO sqlalchemy.engine.Engine PRAGMA temp.table_info("address")
2024-09-13 10:11:23,850 INFO sqlalchemy.engine.Engine [raw sql] ()
2024-09-13 10:11:23,850 INFO sqlalchemy.engine.Engine 
CREATE TABLE user_account (
        id INTEGER NOT NULL, 
        name VARCHAR(30) NOT NULL, 
        fullname VARCHAR, 
        PRIMARY KEY (id)
)


2024-09-13 10:11:23,850 INFO sqlalchemy.engine.Engine [no key 0.00013s] ()
2024-09-13 10:11:23,852 INFO sqlalchemy.engine.Engine 
CREATE TABLE address (
        id INTEGER NOT NULL, 
        email_address VARCHAR NOT NULL, 
        user_id INTEGER, 
        PRIMARY KEY (id), 
        FOREIGN KEY(user_id) REFERENCES user_account (id)
)


2024-09-13 10:11:23,852 INFO sqlalchemy.engine.Engine [no key 0.00033s] ()
2024-09-13 10:11:23,853 INFO sqlalchemy.engine.Engine COMMIT
```

### 为什么出现两次 user_account 和 address？

这是因为 SQLAlchemy 在创建表之前，会先检查这些表是否已经存在。这些输出实际上是 SQLAlchemy 执行的 PRAGMA 语句，用于获取表的信息：

```
PRAGMA main.table_info("user_account")
PRAGMA temp.table_info("user_account")
PRAGMA main.table_info("address")
PRAGMA temp.table_info("address")
```

每个表名出现两次是因为 SQLAlchemy 分别检查了主数据库（main）和临时数据库（temp）中的表信息。这是一种安全检查，确保不会重复创建已存在的表。

### 为什么使用 Base.metadata 就可以创建数据库表？

这里的 `Base` 虽然看起来是空的，但实际上它继承自 `DeclarativeBase`，这个类提供了很多元数据和功能：

```python
class Base(DeclarativeBase):
    pass
```

`DeclarativeBase` 是 SQLAlchemy 的一个基类，它包含了 `metadata` 属性，这个属性是一个 `MetaData` 对象，用于存储所有与之相关的表的信息。

当您定义 `User` 和 `Address` 类时，它们都继承自 `Base`：

```python
class User(Base):
    ...

class Address(Base):
    ...
```

这意味着 `User` 和 `Address` 的表信息会自动添加到 `Base.metadata` 中。

### 为什么没有定义 base 这个变量也能用？

您确实定义了 `Base`，只不过它是一个类，不是一个普通的变量。在 Python 中，类也是对象，可以像变量一样使用。当您调用 `Base.metadata.create_all(engine)` 时，您是在使用 `Base` 类的 `metadata` 属性。

当您调用 `Base.metadata.create_all(engine)` 时，SQLAlchemy 会：

1. 检查每个表是否已存在（这就是为什么您看到了 PRAGMA 语句）
2. 如果表不存在，则创建表（这就是为什么您看到了 CREATE TABLE 语句）

这段代码使用收集到的元数据来创建所有定义的表。

# Flask-SQLAlchemy Table define VS SQLAlchemy Table define

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