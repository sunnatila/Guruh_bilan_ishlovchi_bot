from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from filters import PrivateFilter
from loader import dp


@dp.message_handler(PrivateFilter(), CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Salom, {message.from_user.full_name}!")
