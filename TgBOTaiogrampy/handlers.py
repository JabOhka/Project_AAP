from aiogram import types, F, Router
from aiogram.enums import ParseMode
from aiogram.filters.command import CommandStart
from aiogram.fsm.state import StatesGroup,State
from aiogram.fsm.context import FSMContext

import keyboards as kb
import app.db.req as rg
import category


router=Router()
c=0

class Reg(StatesGroup):
    group=State()
    status=State()
    password=State()


@router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer('Привет! Я бот-помощник для студентов ИБ.')
    if await rg.set_user_id(message.from_user.id) == False:
        await message.answer('Для начала, давай зарегистрируемся!')
        await state.set_state(Reg.group)
        await message.answer('Выбери свою группу.',
                             reply_markup=kb.reg_gr)
    else:
        await message.answer('Вижу тебя в системе!\nЧем могу помочь?')


@router.message(Reg.group)
async def reg_gr(message: types.Message, state: FSMContext):
    await state.update_data(group=message.text)
    await state.set_state(Reg.password)
    await message.answer('Отлично! Если ты староста или зам. старосты введи пароль, если нет, нажми на кнопку.',
                         reply_markup=kb.skip)
@router.message(Reg.password)
async def check_password(message: types.Message, state: FSMContext):
    global c
    data_intrm_group=await state.get_data()
    if message.text=='Пропустить':
        await state.update_data(password=message.text)
        await state.set_state(Reg.status)
    else:
        check=await rg.check_password(data_intrm_group['group'],message.text)
        if check:
            await state.update_data(password=message.text)
            await state.set_state(Reg.status)
            await message.answer('Статус подтвержден!')
        elif not check and c<3:
            c+=1
            await state.update_data(password=message.text)
            await state.set_state(Reg.password)
            await message.answer(f'Упс, пароль неверен, попробуй еще раз. У тебя еще {3-c} попытки/а')
        elif c==3:
            await state.set_state(Reg.status)
            await message.answer('Статус не подтвержден.')
    await message.answer('Нажми на кнопку что бы продолжить',
                         reply_markup=kb.continue_)


@router.message(Reg.status)
async def reg_st(message: types.Message, state: FSMContext):
    data_intrm_group=await state.get_data()
    check=await rg.check_password(data_intrm_group['group'],data_intrm_group['password'])
    if not(check):
        await state.update_data(status=False)
    else:
        await state.update_data(status=True)
    data_reg=await state.get_data()
    await rg.set_user(data_reg['group'], message.from_user.id, data_reg['status'])
    await message.answer('Регистрация окончена.\nЧем могу помочь?',
                         reply_markup=kb.knl)

@router.message(F.text=='Каналы ВШЭ')
async def canal_hse(message: types.Message):
    await message.reply('Выбери категорию.',
                        reply_markup=kb.knl1)
@router.callback_query(F.data=='al')
async def al(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer(category.hse()+'\n'+category.it(), parse_mode=ParseMode.HTML)
@router.callback_query(F.data=='act')
async def act(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer(category.act(), parse_mode=ParseMode.HTML)
@router.callback_query(F.data=='hse')
async def hse(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer(category.hse(), parse_mode=ParseMode.HTML)
@router.callback_query(F.data=='it')
async def it(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer(category.it(),parse_mode=ParseMode.HTML)
@router.callback_query(F.data=='sp')
async def sp(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer(category.sp(), parse_mode=ParseMode.HTML)

