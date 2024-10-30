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

## 初始化代码详解

### `flask` VS `Flask`

`flask` (小写) 是Python包的名称，这是一个模块/包的标准命名方式

`Flask` (大写) 是类名，在Python中类名通常使用大写字母开头（PascalCase命名法）

这是Python的常见命名规范，不是混淆：
- 包名/模块名用小写（如：flask, os, sys）
- 类名用大写开头（如：Flask, String, Dict）

### `SQLAlchemy` in the flask_sqlalchemy

`SQLAlchemy` 这个类是一个集成类，它的主要作用是：

作为Flask和SQLAlchemy之间的桥梁，提供了一个统一的接口来管理：

数据库连接，会话管理，模型定义，查询构建

### `db = SQLAlchemy(model_class=Base)`

这行代码**不是**创建数据库表，而是创建了一个SQLAlchemy实例

这个实例（db）提供了很多功能：
```python
# 例如后续可以这样使用：
db.session  # 用于数据库会话管理
db.Model    # 用于定义数据库模型
db.create_all()  # 用于创建所有定义的表
```

`model_class=Base` 是告诉 Flask-SQLAlchemy 使用我们自定义的 Base 类作为模型的基类

完整的初始化流程是：
```python
# 1. 创建基类
class Base(DeclarativeBase):
    pass

# 2. 创建SQLAlchemy实例
db = SQLAlchemy(model_class=Base)

# 3. 创建Flask应用
app = Flask(__name__)

# 4. 配置数据库URI
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

# 5. 初始化应用
db.init_app(app)

# 6. 定义模型
class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))

# 7. 创建表（在应用上下文中）
with app.app_context():
    db.create_all()
```

这种设计模式的优点是：
1. 分离关注点：Flask处理Web部分，SQLAlchemy处理数据库部分
2. 统一接口：通过db实例提供一致的接口
3. 自动管理：自动处理数据库连接、会话等复杂操作
