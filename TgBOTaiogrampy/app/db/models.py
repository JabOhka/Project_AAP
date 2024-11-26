from sqlalchemy import BigInteger, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='mysql+aiomysql://root:Yarih0812@localhost:3306/ib24')
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Absent(Base):
    __tablename__ = 'absents'
    id: Mapped[int] = mapped_column(primary_key=True)
    name_user: Mapped[str] = mapped_column(String(35))
    number_gr: Mapped[str] = mapped_column(String(6))
    name_object: Mapped[str] = mapped_column(String(120))
    cnt_gap: Mapped[int] = mapped_column()


class Deadline(Base):
    __tablename__ = 'deadlines'
    id: Mapped[int] = mapped_column(primary_key=True)
    name_deadline: Mapped[str] = mapped_column(String(120))
    number_gr: Mapped[str] = mapped_column(String(6))
    day_deadline: Mapped[str] = mapped_column(String(10))
    time_deadline: Mapped[str] = mapped_column(String(5))


class Object(Base):
    __tablename__ = 'objects'
    id: Mapped[int] = mapped_column(primary_key=True)
    name_object: Mapped[str] = mapped_column(String(120))


class Password(Base):
    __tablename__ = 'passwords'
    id: Mapped[int] = mapped_column(primary_key=True)
    number_gr: Mapped[str] = mapped_column(String(6))
    password: Mapped[str] = mapped_column(String(50))


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(35))
    tg_id = mapped_column(BigInteger)
    number_gr: Mapped[str] = mapped_column(String(6))
    status: Mapped[bool] = mapped_column()


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
