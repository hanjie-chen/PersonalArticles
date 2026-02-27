from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy import insert, select, update, delete, bindparam
from sqlalchemy import func, union, union_all, text, literal_column, and_, or_, cast, type_coerce
from sqlalchemy.orm import aliased
from sqlalchemy.sql import exists

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

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

stmt_insert = insert(user_table).values(name="plain")

with engine.connect() as conn:
    result = conn.execute(stmt_insert)
    conn.commit()

# 基本的SELECT查询
# select()函数用于创建SELECT语句，可以指定要查询的列或整个表
# where()方法用于添加WHERE子句，指定查询条件
stmt_select = select(user_table).where(user_table.name == 'plain')

# 使用JOIN
# join()方法用于将两个表连接在一起
# 如果存在外键关系，SQLAlchemy会自动推断连接条件
stmt_select = select(user_table, address_table).join(address_table)

# 使用LEFT OUTER JOIN
# isouter=True参数指定使用左外连接
# 这会包含左表（user_table）中的所有行，即使在右表（address_table）中没有匹配的行
stmt_select = select(user_table, address_table).join(address_table, isouter=True)

# 排序和分组
# order_by()方法用于指定结果的排序方式
# group_by()方法用于对结果进行分组
# func.count()是一个聚合函数，用于计数
# label()方法为计算结果指定一个别名
stmt_select = (
    select(user_table.name, func.count(address_table.id).label('address_count'))
    .join(address_table)
    .group_by(user_table.name)
    .order_by(user_table.name)
)

# 子查询
# subquery()方法将SELECT语句转换为可以在其他查询中使用的子查询
# 子查询可以在主查询的FROM子句或WHERE子句中使用
subq = select(address_table.user_id, func.count(address_table.id).label('address_count')).group_by(address_table.user_id).subquery()
stmt_select = select(user_table, subq.c.address_count).join(subq, user_table.id == subq.c.user_id)

# 公共表表达式（CTE）
# cte()方法创建一个公共表表达式，可以在主查询中多次引用
# CTE通常用于复杂查询，可以提高可读性和性能
cte = select(address_table.user_id, func.count(address_table.id).label('address_count')).group_by(address_table.user_id).cte()
stmt_select = select(user_table, cte.c.address_count).join(cte, user_table.id == cte.c.user_id)

# 使用别名
# aliased()函数用于创建表或ORM实体的别名
# 这在自连接查询或需要多次引用同一个表的情况下非常有用
user_alias = aliased(user_table)
stmt_select = select(user_table, user_alias).join(user_alias, user_table.id < user_alias.id)

# 集合操作（UNION, UNION ALL）
# union()函数用于合并两个或多个查询的结果，并去除重复行
# union_all()函数合并结果但不去除重复行
stmt1 = select(user_table).where(user_table.name == 'plain')
stmt2 = select(user_table).where(user_table.name == 'sandy')
union_stmt = union(stmt1, stmt2)
union_all_stmt = union_all(stmt1, stmt2)

# 使用EXISTS
# exists()用于创建EXISTS子查询，通常用在WHERE子句中
# 它检查是否存在满足特定条件的行
exists_stmt = select(user_table).where(exists().where(address_table.user_id == user_table.id))

# 使用SQL函数
# func对象用于访问各种SQL函数
# 这里使用了lower()函数和count()聚合函数
stmt_select = select(func.lower(user_table.name), func.count(address_table.id)).join(address_table).group_by(user_table.name)

# 窗口函数
# over()方法用于定义窗口函数
# 窗口函数可以在查询结果集的特定"窗口"内执行计算
stmt_select = select(
    user_table.name,
    func.row_number().over(order_by=user_table.name).label('row_num'),
    func.count().over().label('total')
)

# 表值函数
# table_valued()方法用于处理返回表的函数
# 这在处理JSON或数组类型的数据时特别有用
json_each = func.json_each('{"a": 1, "b": 2}').table_valued('key', 'value')
stmt_select = select(json_each.c.key, json_each.c.value)

# 使用文本SQL和字面列
# text()函数用于插入原始SQL文本
# literal_column()函数用于创建文字SQL表达式作为列
stmt_select = select(text("'some text'"), literal_column("'literal column'"))

# 复杂的WHERE子句
# and_()和or_()函数用于组合多个条件
# 这允许构建复杂的WHERE子句
stmt_select = select(user_table).where(and_(or_(user_table.name == 'spongebob', user_table.name == 'sandy'), user_table.id > 5))

# 类型转换
# cast()函数用于显式类型转换
# type_coerce()函数用于在Python级别进行类型转换，不影响生成的SQL
stmt_select = select(cast(user_table.id, String), type_coerce(user_table.name, JSON))

# 使用FILTER
# filter()方法用于在聚合函数中添加条件
# 这允许在聚合之前过滤掉不需要的行
stmt_select = select(func.count(address_table.id).filter(address_table.email.like('%@gmail.com')))

# 使用WITHIN GROUP
# within_group()方法用于某些特定的聚合函数
# 例如，在计算中位数或百分位数时使用
stmt_select = select(func.percentile_cont(0.5).within_group(address_table.id))

# 使用lateral相关
# lateral()方法用于创建LATERAL子查询
# LATERAL允许子查询引用主查询中的列，增加了查询的灵活性
subq = select(address_table).where(address_table.user_id == user_table.id).lateral()
stmt_select = select(user_table, subq).join(subq, full=True)



# 假设已有表结构：
# user_table(id, name, fullname, email)
# address_table(id, user_id, email_address)

# 1. 基本的UPDATE操作
basic_update = (
    update(user_table)
    .where(user_table.c.name == "patrick")    # 指定更新条件
    .values(fullname="Patrick Star")          # 设置要更新的值
)
# 执行: UPDATE user_account SET fullname = :fullname WHERE user_account.name = :name_1

# 2. 批量更新 - 同时更新多行数据
batch_update = (
    update(user_table)
    .where(user_table.c.name == bindparam("oldname"))  # 使用参数绑定
    .values(name=bindparam("newname"))
)
# 执行方式:
# conn.execute(
#     batch_update,
#     [
#         {"oldname": "jack", "newname": "ed"},
#         {"oldname": "wendy", "newname": "mary"}
#     ]
# )

# 3. 使用子查询进行更新
subq_update = (
    update(user_table)
    .values(
        email=(
            select(address_table.c.email_address)
            .where(address_table.c.user_id == user_table.c.id)
            .scalar_subquery()
        )
    )
)

# 4. 基本的DELETE操作
basic_delete = (
    delete(user_table)
    .where(user_table.c.name == "patrick")    # 指定删除条件
)
# 执行: DELETE FROM user_account WHERE user_account.name = :name_1

# 5. 使用RETURNING子句（获取被更新/删除的数据）
update_with_return = (
    update(user_table)
    .where(user_table.c.name == "patrick")
    .values(fullname="Patrick Star")
    .returning(user_table.c.id, user_table.c.name)    # 返回指定字段
)

# 6. 实际执行示例
# with engine.begin() as conn:
#     # 执行更新并获取受影响的行数
#     result = conn.execute(basic_update)
#     print(f"更新影响的行数: {result.rowcount}")
#
#     # 执行带返回值的更新
#     result = conn.execute(update_with_return)
#     for row in result:
#         print(f"更新的行: {row}")


