from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from keyboards.keyboards import menu_kb
from states.states import Form


command_rout = Router()


@command_rout.message(CommandStart())
async def command_start(message: Message, state: FSMContext):
    await state.set_state(Form.password)
    await message.answer(f"{message.from_user.full_name}! Введите пароль: ")


@command_rout.message(Command("menu"))
async def command_new(message: Message):
    await message.answer("Меню", reply_markup=menu_kb.as_markup(one_time_keyboard=True))


@command_rout.message(Command("new"))
async def command_new(message: Message, state: FSMContext):
    password = await state.get_data()
    try:
        print(password["password"])
        await state.set_state(Form.date)
        await message.answer("Введите дату и время: ")
    except KeyError:
        await message.answer("Сначало введите пароль, написав - /start")


@command_rout.message(Command("cancel"))
async def command_new(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Все действия отменены.")
