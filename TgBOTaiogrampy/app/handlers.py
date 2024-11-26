from aiogram import types, F, Router
from aiogram.enums import ParseMode
from aiogram.filters.command import CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from app import keyboards as kb
import app.db.req as rq
import app.sup_func
import category


router = Router()
itr_password = 0


class Absent(StatesGroup):
    back_home = State()
    name_subject = State()
    name_user = State()


class Deadline(StatesGroup):
    name_deadline = State()
    day_deadline = State()
    time_deadline = State()


class Reg(StatesGroup):
    group = State()
    status = State()
    password = State()
    name = State()


class Subjects(StatesGroup):
    subject = State()
    subject_skip = State()


@router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer('Привет! Я бот-помощник для студентов ИБ.')
    if not await rq.set_user_id(message.from_user.id):
        await message.answer('Для начала, давай зарегистрируемся!')
        await state.set_state(Reg.group)
        await message.answer('Выбери свою группу.',
                             reply_markup=kb.reg_gr)
    else:
        await message.answer('Вижу тебя в системе!\nЧем могу помочь?',
                             reply_markup=await kb.main(message.from_user.id))


@router.message(Reg.group)
async def reg_gr(message: types.Message, state: FSMContext):
    await state.update_data(group=message.text)
    await state.set_state(Reg.password)
    await message.answer('Отлично! Если ты староста или зам. старосты введи пароль, если нет, нажми на кнопку.',
                         reply_markup=kb.skip)


@router.message(Reg.password)
async def check_password(message: types.Message, state: FSMContext):
    global itr_password
    intermediate_data = await state.get_data()
    if message.text == 'Пропустить':
        await state.update_data(password=message.text)
        await state.set_state(Reg.status)
    else:
        check = await rq.check_password(intermediate_data['group'], message.text)
        if check:
            await state.update_data(password=message.text)
            await state.set_state(Reg.status)
            await message.answer('Статус подтвержден!')
        elif not check and itr_password < 3:
            itr_password += 1
            await state.update_data(password=message.text)
            await state.set_state(Reg.password)
            await message.answer(f'Упс, пароль неверен, попробуй еще раз. У тебя еще {3-itr_password} попытки/а')
        elif itr_password == 2:
            await state.set_state(Reg.status)
            await message.answer('Статус не подтвержден.')
    await message.answer('Продолжим! Введи свое Имя и Фамилию')


@router.message(Reg.status)
async def reg_st(message: types.Message, state: FSMContext):
    intermediate_data = await state.get_data()
    check = await rq.check_password(intermediate_data['group'], intermediate_data['password'])
    if not check:
        await state.update_data(status=False)
    else:
        await state.update_data(status=True)
    await state.set_state(Reg.name)
    await state.update_data(name=message.text)
    data_reg = await state.get_data()
    await rq.set_user(data_reg['name'], message.from_user.id, data_reg['group'], data_reg['status'])
    await state.clear()
    await message.answer('Регистрация окончена.\nЧем могу помочь?',
                         reply_markup=await kb.main(message.from_user.id))


@router.message(Absent.back_home)
@router.message(F.text == 'Отметить отсутствующих')
async def pick_subject(message: types.Message, state: FSMContext):
    await message.answer('Выбери предмет',
                         reply_markup=await kb.subjects())
    await state.set_state(Absent.name_subject)


@router.message(Absent.name_subject)
async def pick_subject2(message: types.Message, state: FSMContext):
    if message.text == 'Добавить предмет':
        await state.clear()
        await state.set_state(Subjects.subject)
        await message.answer('Напиши название предмета, если хочешь добавить несколько, вводи в разных сообщения',
                             reply_markup=kb.add_subjects)
    else:
        await state.update_data(name_subject=message.text)
        await message.answer('Выбери студентов',
                             reply_markup=await kb.students(message.from_user.id))
        await state.set_state(Absent.name_user)


@router.message(Absent.name_user)
async def mark_absent(message: types.Message, state: FSMContext):
    if message.text == 'ВСЁ!':
        await state.clear()
        await message.answer('Чем могу помочь?',
                             reply_markup=await kb.main(message.from_user.id))
    else:
        number_group = await rq.get_group(message.from_user.id)
        if not await rq.check_student(message.text, *number_group):
            await message.answer('Ошибка, студент не найден.')
        else:
            await state.update_data(name_user=message.text)
            data_mark = await state.get_data()
            await rq.set_absent(name_user=data_mark['name_user'], number_group=number_group[0],
                                name_object=data_mark['name_subject'])
        await state.set_state(Absent.name_user)


@router.message(Subjects.subject)
async def add_subject(message: types.Message, state: FSMContext):
    if message.text == 'Всё!':
        await message.answer('Выбери предмет',
                             reply_markup=await kb.subjects())
        await state.clear()
        await state.set_state(Absent.back_home)
    elif not await rq.add_subject(message.text):
        await message.answer('Ошибка, предмет уже существует!')
        await state.set_state(Subjects.subject)


@router.message(F.text == 'Пропуски')
async def pick_subject_skip(message: types.Message, state: FSMContext):
    await message.answer('Выберите предмет',
                         reply_markup=await kb.subjects())
    await state.set_state(Subjects.subject_skip)


@router.message(Subjects.subject_skip)
async def print_table_skips(message: types.Message):
    sorted_absents_list = await rq.get_absents(message.from_user.id)
    ending_str = f'Пропуски предмета {message.text}\n'
    for absent in sorted_absents_list:
        cnt_gap = await rq.get_cnt_gap(absent)
        ending_str += f'{absent} - {cnt_gap} пропуска\n'
    await message.answer(ending_str)


@router.message(F.text == 'Просмотреть дедлайны')
async def begin_deadlines(message: types.Message):
    pass


@router.message(F.text == 'Добавить дедлайн')
async def add_deadlines(message: types.Message, state: FSMContext):
    await state.set_state(Deadline.name_deadline)
    await message.answer('Давай начнем с названия дедлайна')


@router.message(Deadline.name_deadline)
async def dl_nm(message: types.Message, state: FSMContext):
    await state.update_data(name_deadline=message.text)
    await state.set_state(Deadline.day_deadline)
    await message.answer('Теперь введи дату и время дедлайна в формате день.месяц.год(два последних числа) час:минуты')


@router.message(Deadline.day_deadline)
async def dl_d(message: types.Message, state: FSMContext):
    day = message.text
    if not app.sup_func.check_data(day):
        await message.answer('Ошибка! Неверный формат или время дедлайна уже истекло')
        await message.answer('Введите дату дедлайна в формате день.месяц.год')
        await state.set_state(Deadline.day_deadline)
    else:
        day_list = day.split(' ')
        await state.update_data(day_deadline=day_list[0])
        await state.update_data(time_deadline=day_list[1])
        data_deadline = await state.get_data()
        number_gr = await rq.get_group(message.from_user.id)
        await rq.set_deadline(name_deadline=data_deadline['name_deadline'], number_gr=number_gr,
                              day_deadline=data_deadline['day_deadline'], time_deadline=data_deadline['time_deadline'])
        await state.clear()
        await message.answer('Дедлайн добавлен!')
        await message.answer('Чем могу помочь?',
                             reply_markup=await kb.main(message.from_user.id))


@router.message(F.text == 'Каналы ВШЭ')
async def canal_hse(message: types.Message):
    await message.reply('Выбери категорию.',
                        reply_markup=kb.knl)


@router.callback_query(F.data == 'al')
async def al(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer(category.hse()+'\n'+category.it(), parse_mode=ParseMode.HTML)


@router.callback_query(F.data == 'act')
async def act(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer(category.act(), parse_mode=ParseMode.HTML)


@router.callback_query(F.data == 'hse')
async def hse(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer(category.hse(), parse_mode=ParseMode.HTML)


@router.callback_query(F.data == 'it')
async def it(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer(category.it(), parse_mode=ParseMode.HTML)


@router.callback_query(F.data == 'sp')
async def sp(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer(category.sp(), parse_mode=ParseMode.HTML)
