# `date` VS `time` VS `datetime`

1. `date` - 仅表示日期
```python
from datetime import date

# Python 示例
today = date(2024, 1, 1)  # 年，月，日
# 输出：2024-01-01
# 只能存储：年-月-日

# SQLAlchemy 中对应 Date 类型
from sqlalchemy import Date
birthday: Mapped[date] = mapped_column(Date)
```

2. `time` - 仅表示时间
```python
from datetime import time

# Python 示例
now = time(13, 30, 5)  # 时，分，秒
# 输出：13:30:05
# 只能存储：时:分:秒.微秒

# SQLAlchemy 中对应 Time 类型
from sqlalchemy import Time
meeting_time: Mapped[time] = mapped_column(Time)
```

3. `datetime` - 同时表示日期和时间
```python
from datetime import datetime

# Python 示例
now = datetime(2024, 1, 1, 13, 30, 5)  # 年，月，日，时，分，秒
# 输出：2024-01-01 13:30:05
# 存储：年-月-日 时:分:秒.微秒

# SQLAlchemy 中对应 DateTime 类型
from sqlalchemy import DateTime
created_at: Mapped[datetime] = mapped_column(DateTime)
```

为什么需要这三种类型？这是因为不同的业务场景需要不同的时间精度：

1. `date` 使用场景：
   - 生日
   - 节假日
   - 预约日期
   - 任何只需要知道"哪一天"的场景

2. `time` 使用场景：
   - 营业时间
   - 日常固定时间点
   - 任何只需要知道"几点几分"的场景

3. `datetime` 使用场景：
   - 创建时间
   - 修改时间
   - 日志时间戳
   - 任何需要精确到具体时间点的场景

实际使用示例：
```python
from datetime import date, time, datetime
from sqlalchemy import Date, Time, DateTime

class Event(Base):
    __tablename__ = "events"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # 活动日期（只需要知道哪一天）
    event_date: Mapped[date] = mapped_column(Date)
    
    # 每天的开始时间（固定时间点）
    start_time: Mapped[time] = mapped_column(Time)
    
    # 创建时间（需要完整的日期时间信息）
    created_at: Mapped[datetime] = mapped_column(DateTime)

# 使用示例
event = Event(
    event_date=date(2024, 1, 1),        # 2024-01-01
    start_time=time(9, 30),             # 09:30:00
    created_at=datetime.now()           # 2024-01-01 13:30:05.123456
)
```

补充说明：
1. datetime 还可以包含时区信息（如果使用 datetime.datetime.now(tz=timezone.utc)）
2. SQLAlchemy 的 DateTime 类型可以通过 timezone=True 参数支持时区
3. 在处理时间时，建议总是考虑时区问题，特别是在跨地区的应用中

选择哪种类型的建议：
1. 如果只需要日期，用 date
2. 如果只需要时间，用 time
3. 如果需要完整的时间戳，用 datetime
4. 当不确定时，使用 datetime 会更灵活，但会占用更多存储空间

## 非内置类型

`date`, `time`, `datetime` 实际上不是 Python 的内置类型（built-in types），它们是 Python 标准库中 `datetime` 模块提供的类型。这与 `int`, `str`, `float`, `bool` 等真正的内置类型是不同的。

所以：

1. 真正的 Python 内置类型（不需要导入）：
```python
int
str
float
bool
list
dict
tuple
set
# 等等
```

2. datetime 模块中的类型（需要导入）：
```python
from datetime import date, time, datetime

# 或者
import datetime
# 然后使用 datetime.date, datetime.time, datetime.datetime
```

使用示例：
```python
# 内置类型可以直接使用
x: int = 1
name: str = "hello"

# datetime相关类型需要先导入
from datetime import date, time, datetime

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    birthday: Mapped[date] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(DateTime)
```

另一种写法（使用完整模块名）：
```python
import datetime

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    birthday: Mapped[datetime.date] = mapped_column(Date)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime)
```

所以你的理解需要稍微调整：
- `int`, `str`, `float`, `bool` 等是真正的 Python 内置类型，不需要导入
- `date`, `time`, `datetime` 是 Python 标准库中的类型，需要从 `datetime` 模块导入

这种设计是因为：
1. 内置类型是最基础的，几乎所有 Python 程序都会用到
2. 而时间相关的类型是相对特殊的功能，不是所有程序都需要，所以放在标准库中

# 字符串转换为时间类型

从 Python 3.7 开始，`date` 类（`datetime.date`）增加了一个类方法 `fromisoformat()`，用于直接从 ISO 格式的日期字符串创建 `date` 对象。

- ISO 格式的日期字符串格式为 `'YYYY-MM-DD'`，与您的日期字符串格式一致。
- 因此，您可以直接使用 `date.fromisoformat('2024-09-19')` 将字符串转换为 `date` 对象。

对于低于 Python 3.7 的版本，由于没有 `date.fromisoformat()` 方法，需要通过 `datetime.strptime()` 来实现。

如下所示：

```python
>>> from datetime import datetime, date
>>> today_test = "2024-11-04"
>>> rollout = date.fromisoformat(today_test)
>>> rollout
datetime.date(2024, 11, 4)
>>> rollout_test = datetime.strptime(today_test, '%Y-%m-%d').date()
>>> rollout_test
datetime.date(2024, 11, 4)
```

# 获取文件最后修改时间

#### 使用 `date.fromtimestamp()` 获取文件的最后修改日期

`date.fromtimestamp(timestamp)` 方法用于从时间戳创建一个 `date` 对象。

时间戳是一个浮点数，表示自 1970 年 1 月 1 日（UTC）以来的秒数。

**示例：**

```
pythonCopytimestamp = os.stat(md_path).st_mtime
ultimate_modified_date = date.fromtimestamp(timestamp)
```

这将直接获得文件最后修改的日期（不包含时间部分）。

使用 `os.stat` 获取文件的最后修改时间，得到的是一个时间戳。

如下所示：
```python
>>> import os
>>> timestamp = os.stat("/home/Plain/Personal_Project/Test-Website/Readme.md").st_mtime
>>> timestamp
1724061924.119663
>>> modfiled_date = date.fromtimestamp(timestamp)
>>> modfiled_date
datetime.date(2024, 8, 19)
```

