from aiogram import types

from filters import GroupFilter

from loader import dp, bot


@dp.message_handler(GroupFilter(), content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
async def new_member(msg: types.Message):
    members = ''.join([m.get_mention(as_html=True) for m in msg.new_chat_members])
    await msg.answer(f"Xush kelibsiz {members}!")


@dp.message_handler(GroupFilter(), content_types=types.ContentType.LEFT_CHAT_MEMBER)
async def new_member(msg: types.Message):
    if msg.left_chat_member.id == msg.from_user.id:
        await msg.answer(f"{msg.left_chat_member.get_mention(as_html=True)} guruhni tark etdi!")
    elif msg.left_chat_member.id == (await bot.me).id:
        return
    else:
        await msg.answer(f"{msg.left_chat_member.get_mention(as_html=True)} foydalanuvchi "
                         f"{msg.from_user.get_mention(as_html=True)} admin tomonidan guruhdan chiqarildi!")