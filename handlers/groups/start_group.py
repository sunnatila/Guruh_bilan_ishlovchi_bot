from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from filters import GroupFilter, AdminFilter
from loader import dp


@dp.message_handler(GroupFilter(), CommandStart(), AdminFilter())
async def bot_start(msg: types.Message):
    await msg.answer(f"Salom, {msg.from_user.full_name}\n"
                     f"Savollar oyinini boshlash uchun /start_questions")



