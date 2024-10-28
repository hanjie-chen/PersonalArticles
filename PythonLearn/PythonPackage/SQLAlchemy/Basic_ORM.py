from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy import MetaData
from sqlalchemy import text
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session, selectinload, joinedload

# 1. 基础设置
class Base(DeclarativeBase):
    pass

# 2. 模型定义
class User(Base):
    __tablename__ = "user_account"
    
    # 列定义
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    
    # 关系定义 - 一对多
    addresses: Mapped[List["Address"]] = relationship(
        back_populates="user",
        # cascade="all, delete-orphan"  # 可选：级联删除
        # lazy="select"  # 默认懒加载
        # lazy="joined"  # 总是JOIN加载
        # lazy="selectin"  # 使用 SELECT IN 加载
        # lazy="raise"  # 防止意外的懒加载
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

class Address(Base):
    __tablename__ = "address"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id = mapped_column(ForeignKey("user_account.id"))
    
    # 关系定义 - 多对一
    user: Mapped[User] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"

# 3. 数据库连接与初始化
def init_db():
    # 创建内存数据库，echo=True 显示SQL语句
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

    # 根据模型类定义创建数据库表
    # 这行代码会：
    # 1. 检查所有继承自Base的模型类
    # 2. 生成创建表的SQL语句（CREATE TABLE语句）
    # 3. 在数据库中执行这些SQL语句
    Base.metadata.create_all(engine)

    return Session(engine)

plain = User(name="plain", fullname="Plain Ethan")
krabs = User(name="ehkrabs", fullname="Eugene H. Krabs")
sandy = User(name="sandy", fullname="Sandy Squirrel")

def example_usage():
    session = init_db()
    
    # 4.1 创建和关联对象
    # 方式1：直接创建并关联
    sandy = User(
        name="sandy", 
        fullname="Sandy Cheeks",
        addresses=[
            Address(email_address="sandy@squirrel.com"),
            Address(email_address="sandy@karate.com")
        ]
    )
    
    # 方式2：分步创建和关联
    spongebob = User(name="spongebob", fullname="Spongebob Squarepants")
    address = Address(email_address="spongebob@bikinibottom.com")
    spongebob.addresses.append(address)  # 或 address.user = spongebob
    
    # 4.2 保存对象
    session.add(sandy)
    session.add(spongebob)  # address 会被自动添加
    session.commit()
    
    # 4.3 查询示例
    # 基本查询 not recommend
    user = session.query(User).filter_by(name="sandy").first()
    print(user.addresses)  # 触发懒加载
    
    # 使用 Select IN 加载（推荐用于集合）
    stmt = select(User).options(
        selectinload(User.addresses)
    ).where(User.name == "sandy")
    user = session.execute(stmt).scalar_one()
    print(user.addresses)  # 不会触发新的查询
    
    # 使用 JOIN 加载（适合多对一关系）
    stmt = select(Address).options(
        joinedload(Address.user)
    )
    addresses = session.execute(stmt).scalars().all()
    for addr in addresses:
        print(f"{addr.email_address} -> {addr.user.name}")  # 不会触发新的查询
    
    # 4.4 关系过滤
    # 查找有地址的用户
    stmt = (
        select(User)
        .join(User.addresses)
        .distinct()
    )
    
    # 4.5 删除对象
    session.delete(user)  # 如果设置了 cascade="all, delete-orphan"，关联的地址也会被删除
    session.commit()
    
    session.close()
