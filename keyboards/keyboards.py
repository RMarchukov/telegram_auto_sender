from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


menu_kb = ReplyKeyboardBuilder()
menu_kb.add(KeyboardButton(text="/start"))
menu_kb.add(KeyboardButton(text="/new"))
menu_kb.add(KeyboardButton(text="/cancel"))

agreement_kb = ReplyKeyboardBuilder()
agreement_kb.add(KeyboardButton(text="👍"))
agreement_kb.add(KeyboardButton(text="👎"))
