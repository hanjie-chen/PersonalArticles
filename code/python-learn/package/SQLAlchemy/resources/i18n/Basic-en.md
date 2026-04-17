<!-- source_blob: f8d13a82d6f354641f58effe87254fd1fd95df0f -->

# SQLAlchemy Core Components

# About ORM (Object-Relational Mapping)

ORM is a programming technique used to establish a mapping between object-oriented programming languages and relational databases. Its full name is Object-Relational Mapping.

By using this technique, you can operate on a database directly through a programming language without writing SQL statements by hand. Code written this way can also be migrated more easily across different database systems.

Basic ORM concepts

- Entity: Corresponds to a table in the database.
- Property: Corresponds to a column in a table.
- Relationship: Represents associations between entities (such as one-to-many, many-to-many, and so on).

## Python SQLAlchemy Example

Suppose we have a `User` class and a corresponding `users` table:

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

In this example, we define a `User` class that maps to the `users` table in the database. We can create, query, and manipulate user data in an object-oriented way without writing SQL directly.

Comparison between ORM and traditional database operations:

- Traditional approach:
  ```sql
  INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com');
  SELECT * FROM users WHERE name = 'Alice';
  ```
- ORM approach:
  ```python
  new_user = User(name="Alice", email="alice@example.com")
  session.add(new_user)
  users = session.query(User).filter(User.name == "Alice").all()
  ```

The ORM approach is closer to object-oriented thinking, and the code is more intuitive and easier to maintain.

# Engine

The SQLAlchemy engine uses the `create_engine` function to connect to a database.

For example:

```python
from sqlalchemy import create_engine
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
```

The second line creates a SQLAlchemy `engine` object, which is responsible for managing connections to the database. Let's break down what this line means:

```python
engine = create_engine('sqlite+pysqlite:///:memory:', echo=True)
```

1. **The `create_engine` function**:

   - `create_engine` is a function provided by SQLAlchemy to create an `engine` object. This object is the core of database interaction.

2. **Database URL**:

   - `'sqlite+pysqlite:///:memory:'` is a database URL used to specify the database type and connection method.

     - `sqlite`: Specifies that SQLite is being used.

     - `pysqlite`: Specifies the DBAPI driver being used. In modern Python, `pysqlite` usually corresponds to the standard library `sqlite3`.

     - `/:memory:`: Specifies that the database runs in memory.

       This means the database is temporary. It starts with no tables or data and is not persisted to disk. You need to create tables and insert data manually after connecting in order to perform actual database operations. Each time the program restarts, the database is reset. This approach is ideal for testing and development.

3. **The `echo=True` parameter**:

   - `echo=True` is an optional parameter that tells SQLAlchemy to print all generated SQL statements to standard output. This is very useful for debugging and for learning how SQLAlchemy generates SQL.

# Connection

## Build a connection and execute SQL statements

SQLAlchemy provides a simple yet powerful way to interact with a database. Let's look at the basic connection and SQL execution process through an example.

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

Running this code produces the following output:

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

### Code explanation: `text()` --> `execute()`

`text()` is used to create an executable SQL text object, which can then be passed to a connection object's `execute()` method.

> note:
>
> In early versions of SQLAlchemy, `execute()` could accept raw SQL strings directly. However, starting with SQLAlchemy 1.4, directly passing SQL strings was deprecated to improve security and consistency.

Using `text()` lets us use named parameters like `:parameter`, which helps prevent SQL injection and improves code readability.

For example:

```python
from sqlalchemy import text

# 推荐的方式
result = conn.execute(text("SELECT * FROM users WHERE id = :id"), {"id": 1})

# 不推荐的方式（在新版本中可能会产生警告）
# result = conn.execute("SELECT * FROM users WHERE id = 1")
```

And in our example:

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

### Transaction management: `BEGIN (implicit)`

When SQLAlchemy logs `BEGIN (implicit)`, it means SQLAlchemy has recognized the start of a transaction, but this is based on the behavior of the database driver rather than because SQLAlchemy or the application explicitly sent a `BEGIN` command.

Many database drivers automatically start a transaction when you execute the first operation that requires one. This means you do not need to explicitly call `BEGIN` to start a transaction.

## Return values from `execute` queries

Let's first look at a basic example of executing a query:

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

`result` is a `list`. In this example, `result` contains two `tuple` values: `(1, 1)` and `(2, 4)`.

### Parameterized queries

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

**Executing a query with parameters**:

- `text("SELECT x, y FROM some_table WHERE y > :y")`: Creates a SQL query text object using the named parameter `:y`
- `{"y": 2}`: A parameter dictionary that binds the named parameter `:y` to the value `2`

Explanation of the log output:

- `BEGIN (implicit)`: Starts an implicit transaction
- `SELECT x, y FROM some_table WHERE y > ?`: The actual SQL executed, where `?` is the parameter placeholder
- `[generated in 0.00051s] (2,)`: Shows the query generation time and the bound parameter value

- `x: 2 y: 4`: Prints the row that matches the condition `y > 2`, where `x` is `2` and `y` is `4`

- `ROLLBACK`: Ends the transaction and rolls it back. This usually happens because transaction handling is done automatically when the `with` block ends

## ORM

`Session` is a core concept in SQLAlchemy ORM (Object-Relational Mapping). It provides a higher-level abstraction for managing database interactions.

Example code

```python
from sqlalchemy.orm import Session
from sqlalchemy import text

stmt = text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y")

with Session(engine) as session:
    result = session.execute(stmt, {"y": 6})
    for row in result:
        print(f"x: {row.x}  y: {row.y}")
```

Result

```bash
2024-09-07 16:06:34,299 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2024-09-07 16:06:34,299 INFO sqlalchemy.engine.Engine SELECT x, y FROM some_table WHERE y > ? ORDER BY x, y
2024-09-07 16:06:34,300 INFO sqlalchemy.engine.Engine [generated in 0.00036s] (6,)
x: 11  y: 12
x: 13  y: 14
2024-09-07 16:06:34,300 INFO sqlalchemy.engine.Engine ROLLBACK
```

# Metadata

Imagine you are designing a house:

- You need a blueprint showing the position, size, and purpose of each room
- You also need construction instructions telling the workers how to build the house

In SQLAlchemy, Metadata is like that blueprint:

- It records the "design drawings" of all tables (table names, column names, data types, and so on)
- It also comes with a "construction manual" (`create_all`, `drop_all`, and other methods) to guide the database in creating tables from the design

## Core define

Use the `Table` object to define table structures directly, for example:

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

~~Nobody normally uses this~~

## ORM Declarative Forms define

First, look at the complete code:

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

### About the empty `Base` class

By defining an empty `Base` class, you can add custom methods or attributes in the future that will be inherited by all model classes, without modifying each individual model.

For example, adding a `created_at` column to all tables:

   ```python
   from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
   from sqlalchemy import DateTime
   from datetime import datetime

   class Base(DeclarativeBase):
       created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
   ```

In large projects, you can define the `Base` class in a separate file to improve code organization.

> Changes between old and new versions:
>
> It is worth noting that SQLAlchemy handles declarative base classes differently across versions. In older versions, the `declarative_base()` function was used to create the base class. In SQLAlchemy 2.0, the `DeclarativeBase` class was introduced.

---

### `Mapped` and `mapped_column`

`Mapped` and `mapped_column` are new concepts in SQLAlchemy 2.0: type annotations.

- `Mapped[]` is used for type hints to specify the type of an ORM-mapped attribute
- `mapped_column()` defines the concrete attributes of a column and creates a `Column` object

Interpreting them together with the `User` and `Address` classes:

```python
class User(Base):
    __tablename__ = "user_account"
    
    # 定义一个整数类型的主键列
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # 定义一个最大长度为30的字符串列 默认nullable=False
    name: Mapped[str] = mapped_column(String(30))
    
    # 定义一个可为空的字符串列 Optional[] 
    # 如果不适用Optional[] 默认 not null
    fullname: Mapped[Optional[str]]

# 	same as following
#	存在Optional 默认nullable=True
#   fullname: Mapped[Optional[str]] = mapped_column(String, nullable=True)
#	fullname: Mapped[Optional[str]] = mapped_column(String)

    # 定义一个到 Address 模型的一对多关系。
    addresses: Mapped[List["Address"]] = relationship(back_populates="user")


class Address(Base):
    __tablename__ = "address"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    # 不指定String长度 使用数据库默认值
    email_address: Mapped[str]
    
    # 定义一个外键列。注意这里没有使用 `Mapped`，因为它不是直接映射到模型属性的。
    user_id = mapped_column(ForeignKey("user_account.id"))
    
    # 定义到 User 模型的多对一关系。
    user: Mapped[User] = relationship(back_populates="addresses")
```

> In older versions of SQLAlchemy, you might see code like this:
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
> The main difference in the new version is the use of `something: Mapped[int]` and `mapped_cloumn`, which makes the code more explicit and type-safe. However, SQLAlchemy 2.0 still supports the old declaration style.

For more details, please read [Table Configuration with Declarative — SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-declarative-table)

***

Common built-in Python types (especially in a database context):

```python
int        # 整数
float      # 浮点数
str        # 字符串
bool       # 布尔值
bytes      # 字节串
datetime   # 日期时间（来自 datetime 模块）
date       # 日期（来自 datetime 模块）
time       # 时间（来自 datetime 模块）
```

Common SQLAlchemy database column types:

```python
from sqlalchemy import (
    String,          # VARCHAR
    Integer,         # INTEGER
    Float,           # FLOAT
    Numeric,         # DECIMAL
    Boolean,         # BOOLEAN
    Date,            # DATE
    DateTime,        # DATETIME
    Time,            # TIME
    Text,            # TEXT
    LargeBinary,     # BLOB
    JSON,            # JSON
    BigInteger,      # BIGINT
    SmallInteger,    # SMALLINT
)
```

[Complete SQLAlchemy type list](https://docs.sqlalchemy.org/en/20/core/types.html)

If the Python type inside `Mapped[]` is incompatible with the database column type in `mapped_column()`, SQLAlchemy will raise an error at runtime. For example:

```python
# 这会导致错误，因为类型不兼容
id: Mapped[int] = mapped_column(String)  # 错误！

# 这些是正确的类型匹配
id: Mapped[int] = mapped_column(Integer)
name: Mapped[str] = mapped_column(String)
is_active: Mapped[bool] = mapped_column(Boolean)
```

SQLAlchemy's type system checks whether these types are compatible. Here are some common type correspondences:

```python
Python 类型    SQLAlchemy 类型
int           Integer, BigInteger, SmallInteger
float         Float, Numeric
str           String, Text
bool          Boolean
datetime      DateTime
date          Date
time          Time
bytes         LargeBinary
dict          JSON
```

***

In SQLAlchemy 2.0+, if you write only `Mapped[str]` without using `mapped_column()`, SQLAlchemy will apply some default configuration:

For a simple `Mapped[str]`:

```python
# 这两种写法是等价的
email_address: Mapped[str]
email_address: Mapped[str] = mapped_column(String())  # String() 没有指定长度
```

In this case, SQLAlchemy uses the database's default `VARCHAR` length:
- MySQL/MariaDB: defaults to `VARCHAR(255)`
- PostgreSQL: no specific limit, but explicitly specifying a length is still recommended
- SQLite: no enforced length limit

Best practice:
```python
class Address(Base):
    __tablename__ = "address"
    
    # 不推荐：依赖默认值
    email_address1: Mapped[str]
    
    # 推荐：明确指定长度
    email_address2: Mapped[str] = mapped_column(String(255))
```

### Metadata features

All table information for model classes that inherit from `Base` is automatically registered in `Base.metadata`.

You can access all registered tables through `metadata.tables`.

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

Before creating tables, SQLAlchemy first executes these `PRAGMA` statements to check whether the tables already exist in the main database (`main`) and the temporary database (`temp`), ensuring that it does not recreate existing tables.

```
PRAGMA main.table_info("user_account")
PRAGMA temp.table_info("user_account")
PRAGMA main.table_info("address")
PRAGMA temp.table_info("address")
```

# CUDR Operation

Likewise, there are Core-style CUDR operations and ORM-style CUDR operations. We will introduce both, with the main focus on ORM.

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

### Select()

```python
from sqlalchemy import select
stmt = select(user_table).where(user_table.c.name == "spongebob")

>>> print(stmt)
SELECT user_account.id, user_account.name
FROM user_account
WHERE user_account.name = :name_1
```

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

More details are in [Basic.py file](./Basic.py)

## ORM CUDR

### Session.new() & session.add()

`session.new` is a property of the SQLAlchemy `Session` object. It represents the collection of all new objects that have been added to the session but have not yet been committed to the database.

Let's understand it through code:

```python
# User类的实例代表数据库表中的一行数据
plain = User(name="plain", fullname="Plain Ethan")
krabs = User(name="ehkrabs", fullname="Eugene H. Krabs")

# 此时这些对象还不在 session.new 中
print(session.new)  # 输出：IdentitySet([])

# 添加到 session
session.add(plain)
session.add(krabs)

# 现在这些对象出现在 session.new 中
print(session.new)  # 输出：IdentitySet([User(...), User(...)])

# 当执行 flush 或 commit 后，这些对象就不再在 session.new 中了
session.flush()
print(session.new)  # 输出：IdentitySet([])

```

Other related `Session` state collections:

- `session.dirty`: contains modified objects that have not yet been committed
- `session.deleted`: contains objects marked for deletion but not yet committed
- `session.identity_map`: contains all objects tracked by the session

Together, these collections form SQLAlchemy's object state management system, helping implement efficient database operations and transaction management.

### Session.get()

`session.get(entity, primary_key)` takes two main arguments:
1. The first argument is the entity class (in this example, the `User` class)
2. The second argument is the primary key value (in this example, `4`)

If the record already exists in the session's identity map, it returns the existing object directly.

If it does not exist, SQL is sent to the database to fetch the data.

Some usage examples:
```python
# 通过 id 获取单个用户
user = session.get(User, 1)  # 获取 id=1 的用户

# 如果记录不存在,返回 None
non_exist_user = session.get(User, 999)  # 返回 None

# 如果表使用复合主键,可以传入元组
# 假设 Order 表使用 (order_id, user_id) 作为复合主键
order = session.get(Order, (order_id, user_id))
```



### Session.flush() & Session.commit()

`flush` only synchronizes the current changes in the session to the database, but those changes are still inside the transaction and have not actually been committed.

`commit` truly commits the transaction, permanently saving the changes to the database. In practice, `commit()` performs a `flush` first, then commits the current transaction, and then starts a new one.

Usually, you do not need to call `flush()` manually; let SQLAlchemy handle it automatically.

Remember: `flush()` is like writing changes into a draft, while `commit()` is the actual save.

> Use case:
>
> If you need the primary key `id` before calling `commit()`, you can explicitly call `flush()`.
>
> ```python
> from sqlalchemy.ext.declarative import declarative_base
> 
> Base = declarative_base()
> 
> class User(Base):
>     __tablename__ = 'users'
>     id = Column(Integer, primary_key=True)
>     name = Column(String)
> 
> # 创建用户
> user = User(name="Alice")
> session.add(user)
> print(user.id)  # 输出: None
> 
> # flush 之后
> session.flush()
> print(user.id)  # 输出: 1 (已经有 ID 了)
> 
> # 这时其他事务还看不到这条数据
> # commit 之后其他事务才能看到
> session.commit()
> ```





### Session.delete()

```python
1. 标记删除
session.delete(user)  
# 此时：
# - 对象被标记为 'marked for deletion'
# - 对象仍然存在于 session 中
# - 数据库中的数据还未被删除

2. flush 同步
# 自动触发 flush 或手动 flush 时：
session.flush()  
# - 生成 DELETE SQL 语句
# - 在当前事务中执行删除操作
# - 数据在当前事务中已不可见

3. 最终提交
session.commit()
# - 删除操作被永久化到数据库
# - 事务被提交
# - 删除无法撤销
```

A concrete example:

```python
# 假设有一个用户对象
user = session.get(User, 1)

# 1. 标记删除
session.delete(user)
# 此时可以通过 session.rollback() 取消删除

# 2. 执行 flush (通常自动触发)
session.flush()
# 此时数据库中执行了 DELETE 语句，但在事务中
# 仍然可以通过 rollback() 撤销

# 3. 提交事务
session.commit()
# 删除永久生效，无法撤销
```

Key points:
- `session.delete()` does not operate only on uncommitted data; it really deletes records from the database
- But the deletion becomes permanently effective only after `commit()`
- Before `commit()`, you can cancel the deletion with `session.rollback()`

So the behavior of `session.delete()` is consistent with `add()` and `update()`:
- First mark the change in the session
- Then synchronize it to the database via `flush`
- Finally make it permanent with `commit`



### Rollback

`session.rollback()` undoes all uncommitted changes. Let me explain in detail:

```python
### session.rollback() 的作用

1. 撤销范围
- 所有未 commit 的操作都会被撤销，包括：
  * add() - 添加的新对象
  * delete() - 标记删除的对象
  * update - 对象属性的修改
  * flush() - 已经 flush 但未 commit 的改动

2. 工作原理
- 回滚当前事务中的所有数据库操作
- 重置 session 中对象的状态
- 使对象回到最后一次 commit 时的状态

3. 示例代码
session = Session(engine)

# 假设有一个用户对象
user = User(name="test")
session.add(user)                # 新增
user.name = "new_name"          # 修改
session.delete(other_user)       # 删除

# 即使执行了 flush，只要还没 commit，都可以回滚
session.flush()

session.rollback()  
# 此时：
# - add 的对象被移除
# - 修改被撤销
# - 删除标记被清除
# - 所有对象恢复到上次 commit 的状态
```

A complete example:

```python
# 开始新事务
session = Session(engine)

try:
    # 进行一系列操作
    user1 = User(name="user1")
    session.add(user1)          # 添加新用户
    
    user2.name = "new_name"     # 修改现有用户
    
    session.delete(user3)       # 删除用户
    
    # 如果出现错误
    if something_wrong:
        session.rollback()      # 撤销所有改动
    else:
        session.commit()        # 提交所有改动
except Exception as e:
    session.rollback()          # 发生异常时回滚
    raise
finally:
    session.close()             # 最后关闭 session
```

So you can think of SQLAlchemy transaction operations this way:
- `commit()` saves all changes
- `rollback()` undoes all unsaved changes
- `flush()` previews the effect of changes, but they can still be undone with `rollback()`

### Session.close()

```python
### session.close() 详解

1. 主要作用
- 释放数据库连接，返回到连接池
- 清空当前 session 中的所有对象
- 结束当前事务（未提交的事务会回滚）

2. 自动关闭的情况
- 使用 with 语句时会自动关闭：
    with Session() as session:
        # 代码块结束时自动调用 close()
        pass

- 使用 scoped_session 时会在请求结束时自动关闭：
    # Flask-SQLAlchemy 就是这样处理的
    db.session.remove()  # 内部会调用 close()

3. 常见问题
# 问题1：使用已关闭的 session
session.close()
user = session.query(User).first()  # 错误：Session已关闭

# 问题2：忘记关闭导致连接泄露
session = Session()
try:
    # 一些操作
    return result  # 忘记关闭！
except Exception:
    raise  # 异常时也忘记关闭！

# 正确做法
session = Session()
try:
    # 一些操作
    session.commit()
    return result
except Exception:
    session.rollback()
    raise
finally:
    session.close()  # 确保总是关闭
```

Best practices:

1. Use a context manager (recommended)
```python
# 方式1：使用 with 语句
with Session() as session:
    user = session.query(User).first()
    session.commit()
    # 自动关闭

# 方式2：在 Flask 等框架中使用 scoped_session
# 无需手动关闭，框架会处理
```

2. Complete pattern for manual management
```python
session = Session()
try:
    # 1. 执行数据库操作
    user = User(name="test")
    session.add(user)
    
    # 2. 提交或回滚
    session.commit()
    
except Exception as e:
    # 3. 异常处理
    session.rollback()
    raise
    
finally:
    # 4. 确保关闭
    session.close()
```

### Querying: `query` & `select`

Query object type

```python
# 使用模型类名(User)而不是表名(user_account)
# 因为SQLAlchemy ORM操作的是Python对象，而不是直接操作数据库表
session.query(User)  # 正确
# session.query('user_account')  # 错误
```

Methods for getting query results

```python
# 假设我们查询name="sandy"的用户
query = session.query(User).filter_by(name="sandy")

# 1. first() - 返回第一个结果，如果没有返回None
user = query.first()

# 2. one() - 期望且仅返回一个结果
# - 如果没有结果或有多个结果，会抛出异常
user = query.one()  # 可能抛出 NoResultFound 或 MultipleResultsFound

# 3. one_or_none() - 期望零个或一个结果
# - 如果有多个结果会抛出异常
user = query.one_or_none()  # 返回结果或None

# 4. all() - 返回所有结果的列表
users = query.all()  # 返回列表，可能为空

# 5. scalar() - 返回第一个结果的第一个字段
# - 通常用于查询单个值
count = session.query(func.count(User.id)).scalar()

# 6. get() - 通过主键获取
# - 这是query对象的特殊方法
user = session.query(User).get(1)  # 获取id=1的用户
# 新版本推荐使用:
user = session.get(User, 1)
```

Modern querying style (2.0 style) ==recommended==

```python
from sqlalchemy import select

# 新的查询语法使用select()函数
stmt = select(User).where(User.name == "sandy")

# 执行查询的方法：
# 1. scalar() - 返回单个标量结果
user = session.scalar(stmt)

# 2. scalar_one() - 返回一个结果，如果没有或有多个则抛出异常
user = session.scalar_one(stmt)

# 3. scalar_one_or_none() - 返回一个结果或None
user = session.scalar_one_or_none(stmt)

# 4. execute()后跟scalars().all() - 返回所有结果
users = session.execute(stmt).scalars().all()
```

Examples of complex queries

```python
# 多条件查询
stmt = (
    select(User)
    .where(User.name == "sandy")
    .where(User.fullname.isnot(None))
)

# 排序
stmt = (
    select(User)
    .order_by(User.name.desc())  # 降序
    .limit(5)  # 限制返回数量
)

# 聚合查询
from sqlalchemy import func
stmt = (
    select(func.count(User.id))
    .select_from(User)
    .where(User.name.like('s%'))
)

# JOIN查询
stmt = (
    select(User, Address)
    .join(Address)
    .where(Address.email_address.like('%@gmail.com'))
)

# 分组查询
stmt = (
    select(User.name, func.count(Address.id))
    .join(Address)
    .group_by(User.name)
    .having(func.count(Address.id) > 1)
)
```

5. **Suggestions for choosing query methods**
- When you expect only one result:
  - If a result must exist: use `one()`
  - If there may be no result: use `one_or_none()`
  - If you only need the first result: use `first()`

- When you need multiple results:
  - Use `all()` to get a list
  - Use `scalars().all()` (2.0 style)

- When querying by primary key:
  - Use `session.get(User, id)`

- When pagination is needed:
```python
# 分页查询
page = 2
per_page = 10
stmt = (
    select(User)
    .order_by(User.id)
    .offset((page - 1) * per_page)
    .limit(per_page)
)
```

Remember, newer versions of SQLAlchemy recommend the 2.0-style query syntax (using `select()`), which provides better type hints and consistency. However, the older `query()` syntax is still available and remains widely used in existing codebases.

### Session.execute

In SQLAlchemy 2.x, there are indeed two main ways to execute queries: using the `scalar()` family directly, or using `execute()`. Each has its own use cases. Let's look at them:

1. Use the `scalar()` family directly:
   - `scalar()`
   - `scalar_one()`
   - `scalar_one_or_none()`

2. Use `execute()`, and then call other methods such as `scalars().all()` as needed

Which approach is recommended mainly depends on your specific needs:

1. When you expect a query to return a single result, using the `scalar()` family directly is cleaner and more straightforward:

   - If you are sure the query will return exactly one result or `None`, use `scalar_one_or_none()`
   - If you are sure the query must return exactly one result, use `scalar_one()`
   - If you want the first result, if any, use `scalar()`

   These methods return ORM objects directly, without further processing.

2. When you need more flexible result handling, or expect multiple results, `execute()` is more suitable:

   - `execute()` returns a `Result` object, which offers more flexibility and control
   - You can then call `scalars()`, `all()`, `first()`, and so on as needed
   - This is appropriate for multi-row results or when additional result processing is required

Overall, the recommended approach in SQLAlchemy 2.x is:

- For queries returning a single result, prefer the `scalar()` family because it is more concise and returns ORM objects directly.
- For queries that may return multiple results, or when you need more result-processing options, use `execute()`.

For example:

```python
# 查询单个用户
user = session.scalar_one_or_none(select(User).where(User.id == 1))

# 查询多个用户
users = session.execute(select(User).where(User.age > 18)).scalars().all()
```

This approach keeps the code concise while still providing enough flexibility for different query scenarios.

### Further explanation about `select`

Once we import and use `select`, we do not need to import other keywords such as `where`, `order_by`, and so on, because `select` already comes with them:

[SELECT and Related Constructs — SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select)

There, you can see the methods available on `select`:
```python
__init__(), add_columns(), add_cte(), alias(), as_scalar(), c, column(), column_descriptions, columns_clause_froms, correlate(), correlate_except(), corresponding_column(), cte(), distinct(), except_(), except_all(), execution_options(), exists(), exported_columns, fetch(), filter(), filter_by(), from_statement(), froms, get_children(), get_execution_options(), get_final_froms(), get_label_style(), group_by(), having(), inherit_cache, inner_columns, intersect(), intersect_all(), is_derived_from(), join(), join_from(), label(), lateral(), limit(), offset(), options(), order_by(), outerjoin(), outerjoin_from(), prefix_with(), reduce_columns(), replace_selectable(), scalar_subquery(), select(), select_from(), selected_columns, self_group(), set_label_style(), slice(), subquery(), suffix_with(), union(), union_all(), where(), whereclause, with_for_update(), with_hint(), with_only_columns(), with_statement_hint()
```

## ORM CUDR <u>***SELECT***</u>

source: [Using SELECT Statements — SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html)



### `.where` usage

In SQLAlchemy 2.0, you can use multiple `.where()` clauses, and they will be combined with `AND`.

```python
exist_check = db.session.execute(
    db.select(Article_Meta_Data)
    .where(Article_Meta_Data.title == article_metadata.title)
    .where(Article_Meta_Data.category == article_metadata.category)
).scalar()
```

There are also several equivalent alternatives:

Separate multiple conditions with commas inside `where` (they are automatically combined with `AND`):

```python
exist_check = db.session.execute(
    db.select(Article_Meta_Data).where(
        Article_Meta_Data.title == article_metadata.title,
        Article_Meta_Data.category == article_metadata.category
    )
).scalar()
```

Use the `and_` function:

```python
from sqlalchemy import and_

exist_check = db.session.execute(
    db.select(Article_Meta_Data).where(
        and_(
            Article_Meta_Data.title == article_metadata.title,
            Article_Meta_Data.category == article_metadata.category
        )
    )
).scalar()
```

> [!note]
>
> For how to use `and_()` and `or_()`, refer to the example below:
>
> ```python
> from sqlalchemy import and_, or_
> print(
>     select(Address.email_address).where(
>         and_(
>             or_(User.name == "squidward", User.name == "sandy"),
>             Address.user_id == User.id,
>         )
>     )
> )
> ```
>
> equal to
>
> ```sql
> SELECT address.email_address
> FROM address, user_account
> WHERE (user_account.name = :name_1 OR user_account.name = :name_2)
> AND address.user_id = user_account.id
> ```

All of these methods are equivalent and generate the same SQL query.

# ORM relationship

Some characteristics of ORM relationships

## Relationship loading strategies

We can understand four different relationship loading strategies through a concrete example. Suppose we have this data:

- 10 users
- Each user has 3 addresses

Let's compare the query behavior of different loading strategies:

### Select in load()

```python
# 使用 selectinload
stmt = select(User).options(selectinload(User.addresses))
users = session.execute(stmt).scalars().all()

# 实际执行的SQL：
# Query 1: SELECT * FROM user_account;  # 获取10个用户
# Query 2: SELECT * FROM address WHERE user_id IN (1,2,3,4,5,6,7,8,9,10);  # 一次获取所有地址
```

### Lazy Load (default) - the N+1 problem

```python
# 不使用 selectinload
stmt = select(User)
users = session.execute(stmt).scalars().all()  # 1次查询获取用户
for user in users:
    print(user.addresses)  # 每个用户都会触发一次新查询！

# 实际执行的SQL：
# Query 1: SELECT * FROM user_account;  # 获取10个用户
# Query 2: SELECT * FROM address WHERE user_id = 1;  # 获取用户1的地址
# Query 3: SELECT * FROM address WHERE user_id = 2;  # 获取用户2的地址
# ... （总共执行11次查询！）
```

### Joined Load

```python
# 使用 joinedload
stmt = select(User).options(joinedload(User.addresses))
users = session.execute(stmt).scalars().all()

# 实际执行的SQL：
# SELECT user_account.*, address.* 
# FROM user_account 
# LEFT OUTER JOIN address ON user_account.id = address.user_id
# 
# 问题：
# 1. 如果每个用户有3个地址，结果集会有30行（10用户 × 3地址）
# 2. 数据有重复，用户信息会重复3次
# 3. 数据量大时，传输和处理的数据量会急剧增加
```

Network overhead analysis:

```python
# 假设每次数据库连接有20ms的网络延迟：

# 懒加载：
# 11次查询 × 20ms = 220ms 的网络延迟

# JOIN加载：
# 1次查询 × 20ms = 20ms 的网络延迟
# 但是传输的数据量更大（因为数据重复）

# Select IN：
# 2次查询 × 20ms = 40ms 的网络延迟
# 传输的数据量最优（没有重复）
```

Best practice recommendations:
- Small datasets, one-to-one relationships: `joinedload` can be used
- Large datasets, one-to-many relationships: use `selectinload`
- If you are not sure whether related data is needed: use the default lazy loading



## Session execution methods

```python
# 1. session.scalar(stmt)
user = session.scalar(stmt)  # 简洁写法

# 2. session.execute(stmt).scalar()
user = session.execute(stmt).scalar()  # 完整写法
```

These two approaches are essentially the same. `session.scalar()` is actually shorthand for `session.execute().scalar()`.

**Recommendations:**

1. When querying a single result, use `session.scalar()`:
```python
# 获取单个用户
user = session.scalar(select(User).where(User.id == 1))
```

2. When querying multiple results, use `session.execute().scalars().all()`:
```python
# 获取多个用户
users = session.execute(select(User)).scalars().all()
```

3. When you need to do more processing on the result, use `execute()`:
```python
# 需要进一步处理结果
result = session.execute(select(User))
for user in result.scalars():
    # 处理每个用户
    pass
```

Short version:

`session.scalar()` queries a single result

`session.execute()` returns a `Result` object, providing more control and flexibility, and is suitable for multi-row results

## Stmt functions

Common functions

```python
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import joinedload

# 1. 基础查询
# 查询单个
stmt = select(User).where(User.id == 1)
user = session.scalar(stmt)

# 查询多个
stmt = select(User)
users = session.execute(stmt).scalars().all()

# 2. 条件查询
stmt = (
    select(User).where(
        and_(
            User.age >= 18,
            User.name.like('A%')  # 名字以A开头
        )
    )
)

# 3. 排序
stmt = (
    select(User)
    .order_by(User.age.desc())  # 降序
    .order_by(User.name)        # 升序
)

# 4. 限制结果数量
stmt = (
    select(User)
    .limit(10)        # 最多10条
    .offset(20)       # 跳过前20条
)

# 5. 关联查询
# 内连接（只返回有地址的用户）
stmt = (
    select(User)
    .join(User.addresses)
    .distinct()
)

# 左连接（包含没有地址的用户）
stmt = (
    select(User)
    .outerjoin(User.addresses)
)

# 6. 预加载关联数据
stmt = (
    select(User)
    .options(joinedload(User.addresses))  # 一次性加载地址信息
)

# 7. 聚合函数
from sqlalchemy import func
stmt = (
    select(func.count(User.id))
    .where(User.age > 18)
)
count = session.scalar(stmt)
```

Common modifiers:
- `.where()`: add conditions
- `.join()`: inner join
- `.outerjoin()`: left join
- `.distinct()`: remove duplicates
- `.order_by()`: sort
- `.limit()`: limit the number of results
- `.offset()`: skip records
- `.options()`: configure loading options

Common filter conditions:
- `==`: equal to
- `!=`: not equal to
- `.in_()`: in a list
- `.like()`: fuzzy match
- `.ilike()`: case-insensitive fuzzy match
- `>`, `<`, `>=`, `<=`: comparisons
- `and_()`: and
- `or_()`: or
- `.is_(None)`: is null
- `.is_not(None)`: is not null
