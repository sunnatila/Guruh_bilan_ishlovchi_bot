from aiogram import types

from filters import PrivateFilter
from loader import dp


# Echo bot
@dp.message_handler(PrivateFilter(), state=None)
async def bot_echo(message: types.Message):
    info = "Janob meni guruhga qoshing va adminlar qatoriga qoshing.\n" \
           "Men esa guruhda savol javop oyinida ball hisoblovchiman"
    await message.answer(text=info)
