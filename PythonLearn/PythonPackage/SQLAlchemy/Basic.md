# SQLAlchemy Basic Knowledge

在基础知识阶段，我们将学习这些概念：

1. 了解ORM（对象关系映射）
2. 学习SQLAlchemy的核心组件：Engine, Connection, MetaData
3. 掌握基本的CRUD操作（创建、读取、更新、删除）
4. 学习如何定义模型（Model）和表（Table）

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
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

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

## `engine.connect()` vs `session(engine)`

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

### 如何选择？

- 如果你的项目使用 ORM，并且需要处理复杂的对象映射和事务逻辑，`session` 是更好的选择。它简化了事务管理，并提供了丰富的功能来处理对象的生命周期。
- 如果你只是需要执行简单的 SQL 语句，或者项目不需要使用 ORM，`engine.connect` 可以提供更直接和高效的方式来与数据库交互。

总之，`session` 提供了更高层次的抽象，适合复杂的应用程序，而 `engine.connect` 则适合简单的、低级别的数据库操作。

