import asyncio
import json
import re
from datetime import datetime
from aiogram import Router, Bot, F
from aiogram.exceptions import AiogramError
from aiogram.filters import ChatMemberUpdatedFilter, JOIN_TRANSITION
from aiogram.fsm.context import FSMContext
from aiogram.types import ChatMemberUpdated, Message
from keyboards.keyboards import agreement_kb
from states.states import Form
from jsons.work_with_json import chats_id, pas


send_rout = Router()


@send_rout.message(Form.password, F.text.casefold() == pas)
async def true_password(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    await state.set_state(Form.date)
    await message.answer(f"Пароль верний, введите дату и время(Формат - yyyy-mm-dd hh:mm): ")


@send_rout.message(Form.password, F.text.casefold() != pas)
async def false_password(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f"Пароль не верный. Напишите - /start")


@send_rout.message(Form.date)
async def set_date(message: Message, state: FSMContext):
    try:
        specified_time = datetime.strptime(message.text, "%Y-%m-%d %H:%M")
        delta = (specified_time - datetime.now()).total_seconds()
        if re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$", message.text) and delta > 0:
            await state.update_data(date=message.text)
            await state.set_state(Form.message_text)
            await message.answer("Введите текст сообщения: ")
        else:
            await message.answer("Неверный формат даты. Повторите ввод: ")
    except ValueError:
        await message.answer("Неверный формат даты. Повторите ввод: ")


@send_rout.message(Form.message_text)
async def set_message(message: Message, state: FSMContext):
    await state.update_data(message_text=message.text)
    date = await state.get_data()
    await state.set_state(Form.agreement)
    await message.answer(f"Подтвердите отправку сообщения в - {date['date']}", reply_markup=agreement_kb.as_markup(one_time_keyboard=True))


@send_rout.message(Form.agreement, F.text.casefold() == "👍")
async def send_message(message: Message, bot: Bot, state: FSMContext):
    info = await state.get_data()
    await message.answer(f"Сообщение запланировано на отправку - {info['date']}. Что б запланировать новую рассылку напишите - /new")

    async def sender(chats, text, time_str):
        specified_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M")
        delta = (specified_time - datetime.now()).total_seconds()
        if not chats:
            await message.answer("Отсутствуют чаты для отправки.")
        else:
            if delta > 0:
                await asyncio.sleep(delta)
                for chat in chats:
                    try:
                        await bot.send_message(chat_id=chat, text=text)
                    except AiogramError as err:
                        print(err)

    await sender(chats_id, info["message_text"], info["date"])


@send_rout.message(Form.agreement, F.text.casefold() == "👎")
async def send_message(message: Message):
    await message.answer("Вы не подтвердили отправку. Для подтверждения напишите - 👍. Для перенастройки напишите - /new")


@send_rout.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION))
async def bot_added(event: ChatMemberUpdated):
    new_data = {
        "chat_title": event.chat.title,
        "chat_id": event.chat.id
    }

    try:
        with open("../jsons/chats.json", "r", encoding='utf-8') as file:
            existing_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []
    if new_data not in existing_data:
        existing_data.append(new_data)

    with open("../jsons/chats.json", "w", encoding='utf-8') as file:
        json.dump(existing_data, file, ensure_ascii=False)
        print("Add!")