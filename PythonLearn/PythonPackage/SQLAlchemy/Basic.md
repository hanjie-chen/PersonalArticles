# SQLAlchemy Basic Knowledge

在基础知识阶段，我们将学习这些概念：

1. 掌握基本的CRUD操作（创建、读取、更新、删除）
2. 学习如何定义模型（Model）和表（Table）

# 关于ORM(Object-Relational Mapping)

ORM是一种编程技术,用于在面向对象编程语言和关系型数据库之间建立映射关系，全称是Object-Relational Mapping,即对象关系映射。

通过使用这种技术，可以直接通过编程语言来擦欧总数据库，而不需要直接编写SQL语句。而且写得代码可以方便的在不同的数据库系统之间迁移

ORM的基本概念

- 实体(Entity): 对应数据库中的表。
- 属性(Property): 对应表中的列。
- 关系(Relationship): 表示实体之间的关联(如一对多,多对多等)。

常见框架

- Java: Hibernate, MyBatis
- Python: SQLAlchemy, Django ORM
- .NET: Entity Framework

## Python SQLAlchemy示例

假设我们有一个User类和一个对应的users表:

```python
# Python示例,使用SQLAlchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

# 使用ORM创建新用户
new_user = User(name="Alice", email="alice@example.com")
session.add(new_user)
session.commit()

# 使用ORM查询用户
users = session.query(User).filter(User.name == "Alice").all()
```

在这个例子中,我们定义了一个User类,它映射到数据库中的users表。我们可以使用面向对象的方式来创建、查询和操作用户数据,而不需要直接编写SQL语句。

ORM与传统数据库操作的对比:

- 传统方式:
  ```sql
  INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com');
  SELECT * FROM users WHERE name = 'Alice';
  ```
- ORM方式:
  ```python
  new_user = User(name="Alice", email="alice@example.com")
  session.add(new_user)
  users = session.query(User).filter(User.name == "Alice").all()
  ```

ORM方式更接近于面向对象的编程思维,代码更加直观和易于维护。

# Core Components of SQLAlchemy: Engine

Sqlalchemy engine 使用函数`create_engine` 连接数据库

例如：

```python
from sqlalchemy import create_engine
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
```

其中第二行代码用于创建一个SQLAlchemy的`engine`对象，它负责管理与数据库的连接。让我们逐步解释这行代码的含义：

```python
engine = create_engine('sqlite+pysqlite:///:memory:', echo=True)
```

1. **`create_engine`函数**：

   - `create_engine`是SQLAlchemy提供的一个函数，用于创建`engine`对象。这个对象是与数据库交互的核心

2. **数据库URL**：

   - `'sqlite+pysqlite:///:memory:'`是一个数据库URL，用于指定数据库的类型和连接方式。

     - `sqlite`：指定使用SQLite数据库。

     - `pysqlite`：指定使用的DBAPI驱动程序。在现代Python中，`pysqlite`通常对应于`sqlite3`标准库。

     - `/:memory:`：指定数据库在内存中运行。

       这意味着数据库是临时的，并且在创建时没有任何表或数据，而且不会持久化到磁盘。需要在连接后手动创建表并插入数据，以便进行实际的数据库操作。每次重启程序，数据库都会重置。这种方式非常适合测试和开发。

3. **`echo=True`参数**：

   - `echo=True`是一个可选参数，表示SQLAlchemy将会打印所有生成的SQL语句到标准输出。这对于调试和学习SQLAlchemy的SQL生成过程非常有用。

# Core Components of SQLAlchemy: Connection

## Build connect and Execute SQL statement

SQLAlchemy提供了一种简单而强大的方式来与数据库交互。让我们通过一个例子来了解基本的connect和SQL执行过程。

```python
from sqlalchemy import text
from sqlalchemy import create_engine

# 创建一个内存SQLite数据库引擎
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

# 使用with语句来管理连接
with engine.connect() as conn:
    # 创建表
    conn.execute(text("CREATE TABLE some_table (x int, y int)"))
    
    # 插入数据
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
    )
    
    # 提交事务
    conn.commit()
```

执行这段代码会产生以下输出：

```bash
2024-09-07 14:39:14,179 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2024-09-07 14:39:14,179 INFO sqlalchemy.engine.Engine CREATE TABLE some_table (x int, y int)
2024-09-07 14:39:14,179 INFO sqlalchemy.engine.Engine [generated in 0.00041s] ()
<sqlalchemy.engine.cursor.CursorResult object at 0x7f81523dc820>
2024-09-07 14:39:14,181 INFO sqlalchemy.engine.Engine INSERT INTO some_table (x, y) VALUES (?, ?)
2024-09-07 14:39:14,181 INFO sqlalchemy.engine.Engine [generated in 0.00020s] [(1, 1), (2, 4)]
<sqlalchemy.engine.cursor.CursorResult object at 0x7f81523dc880>
2024-09-07 14:39:14,181 INFO sqlalchemy.engine.Engine COMMIT
```

---

### 代码解释 `text()`-->`execute()`

`text()` 用于创建一个可以执行的 SQL 文本对象，这个对象可以传递给连接对象的 `execute()` 来执行。

> note:
>
> 在 SQLAlchemy 的早期版本中，`execute()` 方法可以直接接受原生 SQL 字符串。然而，从 SQLAlchemy 1.4 开始，为了提高安全性和一致性，直接传递 SQL 字符串的做法被弃用了。

使用 `text()` 允许我们使用命名参数 `:parameter`，可以更好地防止 SQL 注入攻击，提高了代码的可读性

例如：

```python
from sqlalchemy import text

# 推荐的方式
result = conn.execute(text("SELECT * FROM users WHERE id = :id"), {"id": 1})

# 不推荐的方式（在新版本中可能会产生警告）
# result = conn.execute("SELECT * FROM users WHERE id = 1")
```

而在我们的例子中

```python
# 插入数据
conn.execute(
	text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
	[
        {"x": 1, "y": 1},
        {"x": 2, "y": 4}
    ],
)
```

### BEGIN (implicit) 事务管理

当 SQLAlchemy 记录“BEGIN (implicit)”时，它表示 SQLAlchemy 识别到一个事务的开始，但这是基于数据库驱动程序的行为，而不是因为 SQLAlchemy 或者应用程序显式地发送了 `BEGIN` 命令。

许多数据库驱动程序会在你执行第一个需要事务的操作时自动开始一个事务。这种行为意味着你不需要显式地调用 `BEGIN` 来开始事务。

## execute 查询返回值

让我们首先看一个基本的查询执行示例：

```bash
>>> with engine.connect() as conn:
...     result = conn.execute(text("SELECT x, y FROM some_table"))
...     print(result.all())
...
2024-09-07 15:04:00,062 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2024-09-07 15:04:00,062 INFO sqlalchemy.engine.Engine SELECT x, y FROM some_table
2024-09-07 15:04:00,062 INFO sqlalchemy.engine.Engine [generated in 0.00038s] ()
[(1, 1), (2, 4)]
2024-09-07 15:04:00,063 INFO sqlalchemy.engine.Engine ROLLBACK
```

result 是一个列表`list` 在这个例子中result包含2个元组`tuple` (1, 1), (2, 4)

### 参数查询

```bash
>>> with engine.connect() as conn:
...     result = conn.execute(text("SELECT x, y FROM some_table WHERE y > :y"), {"y": 2})
...     for row in result:
...             print(f"x: {row.x}  y: {row.y}")
...
2024-09-07 15:51:19,434 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2024-09-07 15:51:19,435 INFO sqlalchemy.engine.Engine SELECT x, y FROM some_table WHERE y > ?
2024-09-07 15:51:19,435 INFO sqlalchemy.engine.Engine [generated in 0.00051s] (2,)
x: 2  y: 4
2024-09-07 15:51:19,435 INFO sqlalchemy.engine.Engine ROLLBACK
```

**执行带参数的查询**：

- `text("SELECT x, y FROM some_table WHERE y > :y")`: 创建一个 SQL 查询文本对象，使用命名参数 `:y`
- `{"y": 2}`: 参数字典，将命名参数 `:y` 绑定到值 `2`

运行日志结果解释

- `BEGIN (implicit)`: 开始一个隐式事务
- `SELECT x, y FROM some_table WHERE y > ?`: 实际执行的SQL，`?` 是参数占位符
- `[generated in 0.00051s] (2,)`: 显示查询生成时间和绑定的参数值

- `x: 2 y: 4`: 打印了符合条件 `y > 2` 的一行数据，其中 `x` 为 `2`，`y` 为 `4`

- `OLLBACK`: 结束事务并回滚。这通常是因为在 `with` 块结束时自动处理事务

## ORM

`Session` 是 SQLAlchemy ORM (对象关系映射) 的核心概念，它提供了一个更高级的抽象层来管理数据库交互。

example code

```python
from sqlalchemy.orm import Session
from sqlalchemy import text

stmt = text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y")

with Session(engine) as session:
    result = session.execute(stmt, {"y": 6})
    for row in result:
        print(f"x: {row.x}  y: {row.y}")
```

result

```bash
2024-09-07 16:06:34,299 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2024-09-07 16:06:34,299 INFO sqlalchemy.engine.Engine SELECT x, y FROM some_table WHERE y > ? ORDER BY x, y
2024-09-07 16:06:34,300 INFO sqlalchemy.engine.Engine [generated in 0.00036s] (6,)
x: 11  y: 12
x: 13  y: 14
2024-09-07 16:06:34,300 INFO sqlalchemy.engine.Engine ROLLBACK
```

# Core Components of SQLAlchemy: Metadata

想象一下你在设计一座房子：

- 你需要一张蓝图，上面标注了每个房间的位置、大小、用途
- 你还需要施工说明，告诉工人如何建造这座房子

在 SQLAlchemy 中，Metadata 就像这张蓝图：

- 它记录了所有表的"设计图"（表名、列名、数据类型等）
- 它还带有"施工说明书"（create_all、drop_all 等方法）来指导数据库按照设计图建表

## Core define

使用 Table 对象直接定义表结构，例如

```python
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

# 创建一个空白的"设计图"
metadata_obj = MetaData()

# 在设计图上画出表的结构
user_table = Table(
	"user_account",
	metadata_obj,	# 把表的设计添加到这张图纸上
	Column("id", Integer, primary_key=True),
	Column("name", String(30)),
  	# ... 其他字段
)
address_table = Table(
	"address",
	metadata_obj,
	Column("id", Integer, primary_key=True),
	Column("user_id", ForeignKey("user_account.id"), nullable=False),
	Column("email_address", String, nullable=False),
	)

# 根据设计图建造真实的数据库表
metadata_obj.create_all(engine)
```

~~正常人都不会用的~~

## ORM Declarative Forms define

先看完整的代码

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

# Base.metadata 自动收集了所有模型类的表结构信息
Base.metadata.create_all(engine)
```

### 关于空的Base类

通过定义空的 `Base` 类，可以在将来添加自定义方法或属性，而这些将被所有模型类继承，无需修改每个单独的模型类。

例如，为所有表添加一个 `created_at` 列：

   ```python
   from sqlalchemy.orm import DeclarativeBase
   from sqlalchemy import Column, DateTime
   from datetime import datetime

   class Base(DeclarativeBase):
       created_at = Column(DateTime, default=datetime.utcnow)
   ```

在大型项目中，可以将 `Base` 类定义在一个单独的文件中以提高代码的组织性。

> 新旧版本变化：
>
> 值得注意的是，SQLAlchemy 在不同版本中对声明式基类的处理有所变化，在旧版本中，使用 `declarative_base()` 函数来创建基类。在 SQLAlchemy 2.0 中，引入了 `DeclarativeBase` 类。

---

### Mapped 和 mapped_column

`Mapped` 和 `mapped_column` 是 SQLAlchemy 2.0 中的新概念：类型注解 (type annotations)

- `Mapped[]` 用于类型提示，指定ORM映射属性的类型
- `mapped_column()` 定义列的具体属性，创建 Column 对象

结合User & Address Class 解读

```python
class User(Base):
    __tablename__ = "user_account"
    
    # 定义一个整数类型的主键列
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # 定义一个最大长度为30的字符串列
    name: Mapped[str] = mapped_column(String(30))
    
    # 定义一个可为空的字符串列 Optional[] 默认为null 
    fullname: Mapped[Optional[str]]
    
    # 定义一个到 Address 模型的一对多关系。
    addresses: Mapped[List["Address"]] = relationship(back_populates="user")


class Address(Base):
    __tablename__ = "address"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    
    # 定义一个外键列。注意这里没有使用 `Mapped`，因为它不是直接映射到模型属性的。
    user_id = mapped_column(ForeignKey("user_account.id"))
    
    # 定义到 User 模型的多对一关系。
    user: Mapped[User] = relationship(back_populates="addresses")
```

> 在旧版本的 SQLAlchemy 中，可能会看到这样的代码：
>
> ```python
> class User(Base):
>     __tablename__ = "user_account"
>     
>     id = Column(Integer, primary_key=True)
>     name = Column(String(30))
>     fullname = Column(String)
>     addresses = relationship("Address", back_populates="user")
> ```
>
> 新版本的主要区别在于使用了`something: Mapped[int]`和`mapped_cloumn`，使得代码更加明确和类型安全。不过，SQLAlchemy 2.0 仍然支持旧的定义方式。

more details please read [Table Configuration with Declarative — SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-declarative-table)

### Metadata特性

所有继承自 Base 的模型类的表信息都会自动注册到 Base.metadata

可以通过 metadata.tables 访问所有已注册的表

```python
# 创建所有表
Base.metadata.create_all(engine)

# 删除所有表
Base.metadata.drop_all(engine)

# 检查表是否存在
Base.metadata.reflect(engine)
```



## Run ORM Declarative code

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

SQLAlchemy 在创建表之前，会先执行的 PRAGMA 语句，检查主数据库（main）和临时数据库（temp）中这些表是否已经存在，确保不会重复创建已存在的表。

```
PRAGMA main.table_info("user_account")
PRAGMA temp.table_info("user_account")
PRAGMA main.table_info("address")
PRAGMA temp.table_info("address")
```

# CUDR Operation

同样的，存在Core方式的CUDR和ORM方式的CUDR，我们会分别介绍这2种，当然着重于ORM

## Core CUDR

### Insert()

```python
from sqlalchemy import insert
stmt = insert(user_table).values(name="plain")

# 通过print可以看到
>>> print(stmt)
INSERT INTO user_account (name) VALUES (:name)
# 转换为特定数据库的SQL语句
>>> compiled = stmt.compile()
>>> compiled.params
{'name': 'plain'}
```

关于`compile()` 

`compiled.params` 可以提供了对绑定参数的访问，如果指定了特定的数据库引擎，`compile()` 可能会生成针对该数据库优化的 SQL。

示例：

```python
# 假设我们有一个 PostgreSQL 引擎
from sqlalchemy import create_engine
engine = create_engine('postgresql://user:pass@localhost/dbname')

# 现在编译时指定引擎
compiled = stmt.compile(engine)

# 这可能会生成 PostgreSQL 特定的 SQL
print(compiled)  # 可能会有细微的 PostgreSQL 特定差异

# 获取实际执行时需要的参数字典
execution_params = compiled.params
```

### Select()

```python
from sqlalchemy import select
stmt = select(user_table).where(user_table.c.name == "spongebob")

>>> print(stmt)
SELECT user_account.id, user_account.name
FROM user_account
WHERE user_account.name = :name_1
```

more details in [Basic.py file](./Basic.py)

### Update() and Delete()

```python
# 1. 基本的UPDATE操作
basic_update = (
    update(user_table)
    .where(user_table.c.name == "patrick")    # 指定更新条件
    .values(fullname="Patrick Star")          # 设置要更新的值
)
# 4. 基本的DELETE操作
basic_delete = (
    delete(user_table)
    .where(user_table.c.name == "patrick")    # 指定删除条件
)
```

more details in [Basic.py file](./Basic.py)

## ORM CUDR
