from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy import MetaData
from sqlalchemy import text
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

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

session = Session(engine)

plain = User(name="plain", fullname="Plain Ethan")
krabs = User(name="ehkrabs", fullname="Eugene H. Krabs")
sandy = User(name="sandy", fullname="Sandy Squirrel")

session.add(plain)
session.add(krabs)

session.commit()

session.close()