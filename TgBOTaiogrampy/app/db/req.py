from app.db.models import async_session
from app.db.models import User, Password, Object, Absent, Deadline
from sqlalchemy import select
import hashlib


async def add_subject(name_subject: str):
    async with async_session() as session:
        if await session.scalar(select(Object).where(Object.name_object == name_subject)):
            return False
        else:
            session.add(Object(name_object=name_subject))
            await session.commit()
            return True


async def check_password(group: str, password: str):
    async with async_session() as session:
        hash_password = hashlib.md5(password.encode())
        user = await session.scalar(select(Password).where(Password.number_gr == group).
                                    where(Password.password == hash_password.hexdigest()))
        return True if user else False


async def check_status(tg_id: int):
    async with async_session() as session:
        status = await session.scalar(select(User).where(User.tg_id == tg_id).where(User.status))
        return True if status else False


async def check_student(name: str, number_group: str):
    async with async_session() as session:
        student = await session.scalar(select(User).where(User.name == name)
                                       .where(User.number_gr == number_group))
        return True if student else False


async def get_absents(tg_id: int):
    async with async_session() as session:
        number_gr = await get_group(tg_id)
        all_absents = await session.scalars(select(Absent).where(Absent.number_gr == number_gr))
        absents_list = []
        for absent in all_absents:
            absents_list.append(absent.name_user)
        sorted_absents_list = sorted(absents_list)
        return sorted_absents_list


async def get_cnt_gap(name_user: str):
    async with async_session() as session:
        str_user = await session.scalars(select(Absent).where(Absent.name_user == name_user))
        cnt_gap = [i.cnt_gap for i in str_user]
        return cnt_gap[0]


async def get_deadlines(tg_id: int):
    async with async_session() as session:
        number_gr = await get_group(tg_id)
        return await session.scalars(select(Deadline).where(Deadline.number_gr == number_gr))


async def get_group(tg_id: int):
    async with async_session() as session:
        str_user = await session.scalars(select(User).where(User.tg_id == tg_id))
        number_gr = [i.number_gr for i in str_user]
        return number_gr


async def get_subjects():
    async with async_session() as session:
        return await session.scalars(select(Object))


async def get_users(tg_id: int):
    async with async_session() as session:
        number_gr = await get_group(tg_id)
        return await session.scalars(select(User).where(User.number_gr == number_gr))


async def set_absent(name_user: str, number_group: str, name_object: str):
    async with async_session() as session:
        if await session.scalar(select(Absent).where(Absent.name_object == name_object).where(Absent.name_user
                                                                                              == name_user)):
            str_absent = await session.scalars(select(Absent).where(Absent.name_object == name_object)
                                               .where(Absent.name_user == name_user))
            for i in str_absent:
                i.cnt_gap += 1
            await session.commit()
        else:
            session.add(Absent(name_user=name_user, number_gr=number_group, name_object=name_object, cnt_gap=1))
            await session.commit()


async def set_deadline(name_deadline: str, number_gr: str, day_deadline: str, time_deadline: str):
    async with async_session() as session:
        session.add(Deadline(name_deadline=name_deadline, number_gr=number_gr, day_deadline=day_deadline,
                             time_deadline=time_deadline))
        await session.commit()


async def set_user(name: str, tg_id: int, group: str, status: bool):
    async with async_session() as session:
        session.add(User(name=name, tg_id=tg_id, number_gr=group, status=status))
        await session.commit()


async def set_user_id(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        return True if user else False
