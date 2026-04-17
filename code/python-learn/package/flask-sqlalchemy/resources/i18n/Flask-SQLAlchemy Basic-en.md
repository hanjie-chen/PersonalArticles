<!-- source_blob: 23bc64313ec789c4a105ca5cd9d7b80b96fc94c7 -->

# Before We Begin

It's best to read [SQLAlchemy Basic](../SQLAlchemy/Basic.md) first, then come back to this section.

# Flask-SQLAlchemy Basic

for flask-sqlalchemy 3.x and sqlalchemy 2.x

# Initialize

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
```

## Detailed Explanation of the Initialization Code

### `flask` VS `Flask`

`flask` (lowercase) is the name of the Python package. This is the standard naming convention for modules/packages.

`Flask` (uppercase) is the class name. In Python, class names usually start with a capital letter (PascalCase).

This is a common Python naming convention, not something confusing:
- Package/module names use lowercase (for example: flask, os, sys)
- Class names start with uppercase letters (for example: Flask, String, Dict)

### `SQLAlchemy` in `flask_sqlalchemy`

The `SQLAlchemy` class is an integration class. Its main purpose is to:

Act as a bridge between Flask and SQLAlchemy, providing a unified interface to manage:

database connections, session management, model definitions, and query construction

## `db = SQLAlchemy(model_class=Base)`

### Native SQLAlchemy Usage
In native SQLAlchemy, we define models like this:
```python
# 1. 定义基类
class Base(DeclarativeBase):
    pass

# 2. 定义模型类
class User(Base):
    __tablename__ = 'users'  # 必须指定表名
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]
```

### Flask-SQLAlchemy Usage
In Flask-SQLAlchemy:
```python
# 1. 创建基类和db实例
class Base(DeclarativeBase):
    pass
db = SQLAlchemy(model_class=Base)

# 2. 定义模型类
class User(db.Model):  # 使用 db.Model 而不是 Base
    # 不需要 __tablename__，会自动生成
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]
```

### Key Points Explained

**What does `db = SQLAlchemy(model_class=Base)` do?**

```python
# Flask-SQLAlchemy 内部大致实现（简化版）
class SQLAlchemy:
    def __init__(self, model_class=None):
        # 将传入的 Base 类扩展，添加 Flask-SQLAlchemy 特定的功能
        self.Model = self.make_declarative_base(model_class)
        
    def make_declarative_base(self, model_class):
        # 如果没有提供 model_class，创建一个新的
        if model_class is None:
            model_class = DeclarativeBase
        
        # 添加 Flask-SQLAlchemy 特定的功能
        class Model(model_class):
            # 自动生成表名的功能
            @declared_attr
            def __tablename__(cls):
                return cls.__name__.lower()
            
            # 添加查询助手
            query = QueryProperty()
            
            # 添加其他 Flask-SQLAlchemy 特定的功能...
        
        return Model
```

**Why use `db.Model`?**

- `db.Model` is a base class enhanced by Flask-SQLAlchemy
- It inherits from the original `Base` class, but adds extra features:
  - Automatic table name generation (no need for `__tablename__`)
  - Integration with Flask's context management
  - A more convenient query interface
  - Added session management features

**The relationship between Flask-SQLAlchemy and SQLAlchemy**

```
Flask-SQLAlchemy
     │
     ├── Provides Flask integration
     ├── Automatically manages database connections
     ├── Handles application context
     └── Simplifies configuration and usage
         │
         ▼
   SQLAlchemy (core)
     │
     ├── Database abstraction layer
     ├── SQL query construction
     └── ORM features
```

# Define and Create Tables

## Define TABLE

```python
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# 文章元数据
class Article_Meta_Data(db.Model):
    # 指定数据模型在数据库中的表名称 如果未指定那么为类名称的小写
    __tablename__ = 'article_meta_date'
    # 主键 但是无需为其赋值 SQLite数据库会自动为其生成一个唯一的值
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # 文章标题 最长不超过100个字 默认nullable=False
    title: Mapped[str] = mapped_column(String(100))

    # 文章发布时间
    rollout_date: Mapped[date] = mapped_column(Date)

    # 表示文章最后更新的日期 只精确到年月日
    ultimate_modified_date: Mapped[date] = mapped_column(Date)

    # 文章作者 最长不超过50个字符
    author: Mapped[str] = mapped_column(String(50))

    # 文章指导者 存在Optional 默认nullable=True
    instructor: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # 文章内容简介
    brief_introduction: Mapped[str] = mapped_column(Text)

    # 文章封面链接
    cover_image_url: Mapped[str] = mapped_column(String(100))

    # 文章分类
    category: Mapped[str] = mapped_column(String(100))
    
    # 文章分类 使用 mptt 待开发和测试
    # category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    # category = db.relationship('Category')

    def __repr__(self):
        return f'<Article {self.title}>'
```

Because of how SQLAlchemy and Flask-SQLAlchemy work:

1. When your model class inherits from `db.Model`, that model is automatically registered in SQLAlchemy metadata.
2. When you call `db.create_all()`, SQLAlchemy checks all registered model classes and creates the tables.

However, there is one important prerequisite here: **your model class must be imported and executed by the Python interpreter before `db.create_all()` is called**.

## Create Table

```python
with app.app_context():
    db.create_all()
```

This code will:

- Create tables that do not exist
- Not modify tables that already exist
- Not delete tables that already exist
- Not overwrite existing data

### `db.create_all()`

Let's look at how `create_all()` works:

```python
# 简化版的内部实现逻辑
def create_all(self):
    # 1. 获取所有表的元数据
    for table in self.metadata.sorted_tables:
        # 2. 检查表是否存在
        if not table.exists():
            # 3. 如果表不存在，创建表
            table.create()
```

A common example scenario:

```python
# 初始模型
class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]

# 执行 db.create_all() -> 创建表

# 后来修改模型，添加新字段
class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    email: Mapped[str]  # 新增字段

# 再次执行 db.create_all() -> 不会添加新字段！
```

> note
>
> `db.create_all()` will automatically create the database file according to `app.config['SQLALCHEMY_DATABASE_URI']`

### How do you handle table schema updates?

**Drop and recreate** (development environment):

```python
with app.app_context():
    db.drop_all()   # 删除所有表
    db.create_all() # 重新创建
```

**Use database migrations** (recommended, production environment):

```python
# 使用 Flask-Migrate
from flask_migrate import Migrate
migrate = Migrate(app, db)

# 初始化迁移
$ flask db init

# 创建迁移脚本
$ flask db migrate -m "Add email column"

# 应用迁移
$ flask db upgrade
```

## `app.app_context()`

### Application Instance and Its Context

First, we need to understand that each `Flask` object represents an independent application instance. When you create a Flask application, you are actually creating an instance of that application:

```python
app = Flask(__name__)
```

This `app` object is a specific application instance. And `app.app_context()` creates an application context, which is an independent execution environment where all operations are associated with a specific application instance.

Flask uses `_app_ctx_stack` to keep track of the currently active application context. When you use `with app.app_context():`:

The application's context is pushed onto `_app_ctx_stack`.

Inside the `with` block, the `current_app` proxy object points to the application context on the top of the stack. When the `with` block exits, the context is popped.

```python
with app.app_context():
    # 这个应用的上下文被推送到栈顶
    ...
# 退出 with 块时，上下文被弹出
```

In a multi-application scenario, each application has its own context. For example:

```python
app1 = Flask('app1')
app2 = Flask('app2')

with app1.app_context():
    # 这里的操作属于 app1
    ...

with app2.app_context():
    # 这里的操作属于 app2
    ...
```

Let's look at a complete example to understand the process:

```python
from flask import Flask, current_app

app1 = Flask('app1')
app2 = Flask('app2')

@app1.route('/')
def index1():
    return f"This is {current_app.name}"

@app2.route('/')
def index2():
    return f"This is {current_app.name}"

# 在脚本中使用
with app1.app_context():
    print(current_app.name)  # 输出: app1
    
with app2.app_context():
    print(current_app.name)  # 输出: app2

# 嵌套使用
with app1.app_context():
    print(current_app.name)  # 输出: app1
    with app2.app_context():
        print(current_app.name)  # 输出: app2
    print(current_app.name)  # 输出: app1
```

> note:
>
> In CLI commands: if you use the `@app.cli.command()` decorator, Flask will also automatically provide the context.
>
> In tests, you can use `app.test_request_context()` to simulate a request context.

### Why does `db.create_all()` require an application context?

There are several reasons why `db.create_all()` needs an application context:

1. **Database configuration**: Database connection information is usually stored in the application configuration (such as `app.config['SQLALCHEMY_DATABASE_URI']`).

2. **Multi-application support**: If your project has multiple Flask applications and each uses a different database, the context ensures that the correct configuration is used.

3. **Lazy initialization**: Flask-SQLAlchemy uses a lazy initialization pattern, and some settings can only be completed within an application context.

### Automatic Handling in View Functions

When handling web requests, Flask automatically creates and manages an application context for each request, so you do not need to explicitly use `with app.app_context()` inside view functions.

```python
@app.route('/')
def index():
    # 这里已经在应用上下文中了
    return f"Current app: {current_app.name}"
```

# CRUD

Flask-SQLAlchemy CRUD is very similar to SQLAlchemy ORM CRUD.

## Insert

Instantiate the table class -> add -> commit

```python
# part code of import_articles_scripts
article = Article_Meta_Data(
            title=metadata.get('Title', 'Untitled'),
            author=metadata.get('Author', 'Unknown'),
            instructor=metadata.get('Instructor'),
            cover_image_url=metadata.get('CoverImage'),
            rollout_date=metadata.get('RolloutDate'),
            ultimate_modified_date=metadata.get('UltimateModifiedDate'),
            category=metadata.get('Category', 'Uncategorized'),
            brief_introduction=brief_intro_text
        )
db.session.add(article_metadata)
db.session.commit()
```

## Query

The query statement `stmt` needs to be executed inside `db.session.execute()`. You only need to add `db.` before `select`, because `db.select` is essentially `sqlalchemy.select`.

For example, a complex query might look like this:

```python
result = db.session.execute(
    db.select(User, Address)
    .join(Address)
    .where(User.name == "plain")
    .order_by(User.id)
)
```

### Exploring the Essence of `db.select`

From the source code of [flask-sqlalchemy extension.py](https://github.com/pallets-eco/flask-sqlalchemy/blob/3e3e92ba557649ab5251eda860a67656cc8c10af/src/flask_sqlalchemy/extension.py), we can see that the `SQLAlchemy` class does not directly define a `select` method. Instead, it handles undefined attribute access through the `__getattr__` magic method. This mechanism is quite elegant. Let's look at how it works:

```python
import typing as t
import sqlalchemy as sa
import sqlalchmey.event as sa.event
import sqlalchemy.orm as sa.orm

class SQLALchemy:

    # ... igonre before code

    
    def __getattr__(self, name: str) -> t.Any:
    if name == "relation":
        return self._relation

    if name == "event":
        return sa_event

    if name.startswith("_"):
        raise AttributeError(name)

    # 关键在这里
    for mod in (sa, sa_orm):
        if hasattr(mod, name):
            return getattr(mod, name)

    raise AttributeError(name)
```

The flow of this code is:

1. When we access `db.select`, Python first checks whether the `SQLAlchemy` class has this attribute
2. If it does not find it, it calls the `__getattr__` method
3. Inside `__getattr__`, it looks for the attribute in the `sa` (SQLAlchemy) and `sa_orm` (SQLAlchemy ORM) modules in sequence
4. Since the `select` function exists in the `sqlalchemy` module, `hasattr(sa, 'select')` returns `True`
5. It then returns the original SQLAlchemy `select` function through `getattr(sa, 'select')`

This explains why:

1. `db.select` is actually `sqlalchemy.select`
2. You cannot find a direct definition of `select` in the source code
3. `type(db.select())` shows `<class 'sqlalchemy.sql.selectable.Select'>`, which is SQLAlchemy's `Select` object

This design pattern is called the Proxy Pattern. Flask-SQLAlchemy uses it to proxy most SQLAlchemy functionality through the `db` object, so we can directly access SQLAlchemy features through `db`.

### `sqlalchemy.select` VS `db.select`

Since `db.select` is actually `sqlalchemy.select`, would using `sqlalchemy.select` directly be faster because it avoids loading `__getattr__()`?

In practice, these two styles run at exactly the same speed, with no performance difference at all.

```python
# 方式1
from sqlalchemy import select
select(User)  # 直接调用sqlalchemy.select

# 方式2
db.select(User)  # 通过__getattr__获取后调用sqlalchemy.select
```

Although `db.select` needs to access the function through the `__getattr__` magic method, this process:

- Only happens the first time `db.select` is accessed
- Uses the cached attribute directly on later accesses
- Adds overhead so small that it can be ignored compared with actual query execution time

Still, `db.select` is recommended because:

- All database-related operations go through the `db` object. If Flask-SQLAlchemy ever needs to extend or modify `select`, your code will not need to change.

- From a software engineering perspective, using `db.select` is better practice. It follows the principles of dependency injection and separation of concerns, and it also makes the code easier to maintain and test.

## Delete & Update

First, use a query statement to filter out the specific entry, for example:

```python
article = db.session.execute(
    db.select(Article_Meta_Data)
    .where(Article_Meta_Data.title == "test-article")
)
```

### Delete

```python
db.session.delete(article)
db.session.commit()
```

### Update

```python
article.author = Plain
db.session.commit()
```

# Reference

[Flask-SQLAlchemy — Flask-SQLAlchemy Documentation (3.1.x)](https://flask-sqlalchemy.palletsprojects.com/en/latest/)
