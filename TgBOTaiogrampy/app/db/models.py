from sqlalchemy import BigInteger, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='mysql+aiomysql://root:Yarih0812@localhost:3306/ib24')
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    number_gr: Mapped[str]=mapped_column(String(6))
    status: Mapped[bool]=mapped_column()


class Password(Base):
    __tablename__ = 'passwords'
    id: Mapped[int] = mapped_column(primary_key=True)
    number_gr: Mapped[str]=mapped_column(String(6))
    password: Mapped[str]=mapped_column(String(50))



async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)