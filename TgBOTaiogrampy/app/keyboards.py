from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from app.db.req import check_status, get_subjects, get_users


async def main(tg_id):
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(types.KeyboardButton(text='Каналы ВШЭ'))
    keyboard.add(types.KeyboardButton(text='Посмотреть дедлайны'))
    if await check_status(tg_id):
        keyboard.add(types.KeyboardButton(text='Отметить отсутствующих'))
        keyboard.add(types.KeyboardButton(text='Пропуски'))
        keyboard.add(types.KeyboardButton(text='Добавить дедланы'))
    return keyboard.adjust(1).as_markup()


async def students(tg_id):
    keyboard = ReplyKeyboardBuilder()
    all_name = await get_users(tg_id)
    keyboard.add(types.KeyboardButton(text='ВСЁ!'))
    names_list = []
    for name in all_name:
        names_list.append(name.name)
    sorted_name_list = sorted(names_list)
    for name in sorted_name_list:
        keyboard.add(types.KeyboardButton(text=name))
    return keyboard.adjust(3).as_markup()


async def subjects():
    keyboard = ReplyKeyboardBuilder()
    all_subjects = await get_subjects()
    subjects_list = []
    for subject in all_subjects:
        subjects_list.append(subject.name_object)
    sorted_subject_list = sorted(subjects_list)
    for subject in sorted_subject_list:
        keyboard.add(types.KeyboardButton(text=subject))
    keyboard.add(types.KeyboardButton(text='Добавить предмет'))
    return keyboard.adjust(2).as_markup()


add_subjects = types.ReplyKeyboardMarkup(keyboard=[
    [types.KeyboardButton(text='Всё!')]
])

reg_gr = types.ReplyKeyboardMarkup(keyboard=[
    [types.KeyboardButton(text='БИБ241'), types.KeyboardButton(text='БИБ242')],
    [types.KeyboardButton(text='БИБ243'), types.KeyboardButton(text='БИБ244')],
    [types.KeyboardButton(text='БИБ245')]
], resize_keyboard=True)

skip = types.ReplyKeyboardMarkup(keyboard=[
    [types.KeyboardButton(text='Пропустить')]
])

knl = types.InlineKeyboardMarkup(inline_keyboard=[
    [types.InlineKeyboardButton(text='Все каналы', callback_data='al')],
    [types.InlineKeyboardButton(text='Официальные каналы ВШЭ', callback_data='hse'),
     types.InlineKeyboardButton(text='IT-каналы', callback_data='it')]
])


