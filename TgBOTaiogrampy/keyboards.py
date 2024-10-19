from aiogram import types

knl=types.ReplyKeyboardMarkup(keyboard=[
    [types.KeyboardButton(text='Каналы ВШЭ')]
],
    resize_keyboard=True,
    input_field_placeholder='Круто')

knl1=types.InlineKeyboardMarkup(inline_keyboard=[
    [types.InlineKeyboardButton(text='Все каналы',callback_data='al')],
    [types.InlineKeyboardButton(text='Официальные каналы ВШЭ', callback_data='hse'),types.InlineKeyboardButton(text='IT-каналы',callback_data='it')]
])

reg_gr=types.ReplyKeyboardMarkup(keyboard=[
    [types.KeyboardButton(text='БИБ241'),types.KeyboardButton(text='БИБ242')],
    [types.KeyboardButton(text='БИБ243'),types.KeyboardButton(text='БИБ244')],
    [types.KeyboardButton(text='БИБ245')]
],
    resize_keyboard=True)

skip=types.ReplyKeyboardMarkup(keyboard=[
    [types.KeyboardButton(text='Пропустить')]
])

continue_=types.ReplyKeyboardMarkup(keyboard=[
    [types.KeyboardButton(text='Продолжить')]
])