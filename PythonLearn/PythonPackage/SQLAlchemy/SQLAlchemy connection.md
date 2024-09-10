# SQLAlchemy connection

首先看如下代码以及运行结果

```bash
>>> from sqlalchemy import text
>>> from sqlalchemy import create_engine
>>> engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
>>> with engine.connect() as conn:
...     conn.execute(text("CREATE TABLE some_table (x int, y int)"))
...     conn.execute(
...             text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
...             [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
...     )
...     conn.commit()
...
2024-09-07 14:39:14,179 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2024-09-07 14:39:14,179 INFO sqlalchemy.engine.Engine CREATE TABLE some_table (x int, y int)
2024-09-07 14:39:14,179 INFO sqlalchemy.engine.Engine [generated in 0.00041s] ()
<sqlalchemy.engine.cursor.CursorResult object at 0x7f81523dc820>
2024-09-07 14:39:14,181 INFO sqlalchemy.engine.Engine INSERT INTO some_table (x, y) VALUES (?, ?)
2024-09-07 14:39:14,181 INFO sqlalchemy.engine.Engine [generated in 0.00020s] [(1, 1), (2, 4)]
<sqlalchemy.engine.cursor.CursorResult object at 0x7f81523dc880>
2024-09-07 14:39:14,181 INFO sqlalchemy.engine.Engine COMMIT
```



## 关于text和execute

SQLAlchemy 可以执行原生的SQL语句，`text()` 函数用于创建一个可以执行的 SQL 文本对象，这个对象可以传递给连接对象的 `execute()` 方法来执行。



## 关于BEGIN(implicit)

在 SQLAlchemy 的上下文中，“BEGIN (implicit)” 的确有一个特定的含义。它指的是 SQLAlchemy 认为一个事务已经开始，但实际上并没有向数据库发送任何显式的 `BEGIN` 语句。这是因为许多数据库和数据库驱动程序（DBAPI）在执行第一个语句时会自动开始一个事务，而不需要显式的 `BEGIN` 命令。

1. **隐式事务开始**：当 SQLAlchemy 记录“BEGIN (implicit)”时，它表示 SQLAlchemy 识别到一个事务的开始，但这是基于数据库驱动程序的行为，而不是因为 SQLAlchemy 或者应用程序显式地发送了 `BEGIN` 命令。

2. **数据库驱动程序的行为**：许多数据库驱动程序会在你执行第一个需要事务的操作时自动开始一个事务。这种行为意味着你不需要显式地调用 `BEGIN` 来开始事务。

3. **事件钩子**：SQLAlchemy 提供了事件系统，你可以注册事件钩子来拦截事务的开始、提交和回滚等事件。通过这些钩子，你可以在事务管理的不同阶段执行自定义逻辑。

4. **日志记录**：日志中记录“BEGIN (implicit)”是为了帮助开发者理解事务的生命周期，即使没有显式地发送 `BEGIN`，SQLAlchemy 仍然会跟踪事务状态。

这种隐式事务管理的机制使得开发者在使用 SQLAlchemy 时不必过于关注事务的开始和结束，简化了代码的复杂性，同时仍然保持了对数据库事务的控制和一致性。



## execute执行结果

首先查看如下内容

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



## execute 参数

首先查看如下代码以及实现结果

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

- `text("SELECT x, y FROM some_table WHERE y > :y")`: 创建一个 SQL 查询文本对象，使用命名参数 `:y`。
- `{"y": 2}`: 参数字典，将命名参数 `:y` 绑定到值 `2`。
- `conn.execute(...)`: 执行 SQL 查询并返回结果集。

运行日志结果解释

- `INFO sqlalchemy.engine.Engine BEGIN (implicit)`: 开始一个隐式事务。
- `INFO sqlalchemy.engine.Engine SELECT x, y FROM some_table WHERE y > ?`: 执行的 SQL 查询语句，其中 `?` 是参数占位符。
- `INFO sqlalchemy.engine.Engine [generated in 0.00051s] (2,)`: 查询参数 `(2,)` 被绑定到占位符 `?`。

- `x: 2 y: 4`: 打印了符合条件 `y > 2` 的一行数据，其中 `x` 为 `2`，`y` 为 `4`。

- `INFO sqlalchemy.engine.Engine ROLLBACK`: 结束事务并回滚。这通常是因为在 `with` 块结束时自动处理事务。

这段代码通过参数化查询来安全地执行 SQL 语句，避免了 SQL 注入风险。通过绑定参数 `{"y": 2}`，查询只返回 `y` 大于 `2` 的行。在这个例子中，结果集中有一行符合条件并被打印出来。使用参数化查询的好处是提高了安全性和可读性。



还可以携带多个参数执行 

for example:

```bash
>>> with engine.connect() as conn:
...     conn.execute(
...             text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
...             [{"x": 11, "y": 12}, {"x": 13, "y": 14}],
...     )
...     conn.commit()
...
2024-09-07 16:00:20,336 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2024-09-07 16:00:20,336 INFO sqlalchemy.engine.Engine INSERT INTO some_table (x, y) VALUES (?, ?)
2024-09-07 16:00:20,337 INFO sqlalchemy.engine.Engine [cached since 4866s ago] [(11, 12), (13, 14)]
<sqlalchemy.engine.cursor.CursorResult object at 0x7f81523dce20>
2024-09-07 16:00:20,337 INFO sqlalchemy.engine.Engine COMMIT
```



## Engine.connect VS Session

可以使用session实现类似的功能

```bash
>>> from sqlalchemy.orm import Session
>>> stmt = text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y")
>>> with Session(engine) as session:
...     result = session.execute(stmt, {"y": 6})
...     for row in result:
...             print(f"x: {row.x}  y: {row.y}")
...
2024-09-07 16:06:34,299 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2024-09-07 16:06:34,299 INFO sqlalchemy.engine.Engine SELECT x, y FROM some_table WHERE y > ? ORDER BY x, y
2024-09-07 16:06:34,300 INFO sqlalchemy.engine.Engine [generated in 0.00036s] (6,)
x: 11  y: 12
x: 13  y: 14
2024-09-07 16:06:34,300 INFO sqlalchemy.engine.Engine ROLLBACK
```

- **使用 `Session`**：
  - `Session(engine)`: 创建一个新的会话对象，用于管理与数据库的交互。
  - `session.execute(stmt, {"y": 6})`: 执行带参数的 SQL 查询。
  - 自动管理事务：在 `with` 块结束时，自动处理事务的提交或回滚。

- **日志信息**：
  - `INFO sqlalchemy.engine.Engine BEGIN (implicit)`: 开始一个隐式事务。
  - `INFO sqlalchemy.engine.Engine SELECT ...`: 执行的 SQL 查询。
  - `INFO sqlalchemy.engine.Engine ROLLBACK`: 在 `with` 块结束时，自动回滚事务。

### 如何选择？

- 如果你的项目使用 ORM，并且需要处理复杂的对象映射和事务逻辑，`session` 是更好的选择。它简化了事务管理，并提供了丰富的功能来处理对象的生命周期。
- 如果你只是需要执行简单的 SQL 语句，或者项目不需要使用 ORM，`engine.connect` 可以提供更直接和高效的方式来与数据库交互。

总之，`session` 提供了更高层次的抽象，适合复杂的应用程序，而 `engine.connect` 则适合简单的、低级别的数据库操作。
