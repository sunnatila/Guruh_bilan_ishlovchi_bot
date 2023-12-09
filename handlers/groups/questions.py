from aiogram.dispatcher.filters import Command
from aiogram import types
from aiogram.dispatcher import FSMContext
from filters import GroupFilter, AdminFilter
from handlers.groups.sorted_result import result_sort
from handlers.groups.write_data import get_user, clear_data, write_data, get_users
from loader import dp
from states.state_group import GameStates


@dp.message_handler(GroupFilter(), Command("start_questions"), AdminFilter())
async def start_game(msg: types.Message, state: FSMContext):
    id_group = msg.chat.id
    file_path = f"data/groups/group{id_group}.json".replace('-', '_')
    clear_data(file_path)
    await msg.answer("Oyin boshlandi. Hamaga omad!\n"
                     "Oyini tohtatish uchun: /stop_questions")
    await state.set_state(GameStates.start)


@dp.message_handler(GroupFilter(), Command("start_questions"), AdminFilter(), state=GameStates.start)
async def error_start_questions(msg: types.Message, state: FSMContext):
    await msg.answer("Oyini yengidan boshlash uchun yakunlang.\n"
                     "Yakunlash uchun: /stop_questions")


@dp.message_handler(GroupFilter(), Command("stop_questions"), AdminFilter(), state=GameStates.start)
async def error_start_questions(msg: types.Message, state: FSMContext):
    await msg.answer("Oyin yakulandi.\nNatijani bilish uchun: /result\n")
    await GameStates.next()


@dp.message_handler(GroupFilter(), AdminFilter(), state=GameStates.start)
async def error_start_questions(msg: types.Message, state: FSMContext):
    id_group = msg.chat.id
    file_path = f"data/groups/group{id_group}.json".replace('-', '_')
    try:
        user = msg.reply_to_message.from_user
        ball = msg.text
        if ball.isdigit():
            ball = int(ball)
        else:
            await msg.reply(f"{user.get_mention(as_html=True)} bu qatnashuvchiga notog'ri ball berdingiz!")
            return
        user_data = get_user(user.id, file_path)
        if user_data:
            data = user_data[0]
            data['score'] += ball
        else:
            data = {
                'id': user.id,
                'username': user.username,
                'fullname': user.full_name,
                'score': ball,
                'mention': user.get_mention(as_html=True)
            }

        write_data(data, file_path)
        await msg.answer(f"{user.get_mention(as_html=True)} ga {ball} berildi!")
    except AttributeError:
        return


@dp.message_handler(GroupFilter(), Command("result"), AdminFilter(), state=GameStates.stop)
async def result_questions(msg: types.Message, state: FSMContext):
    id_group = msg.chat.id
    file_path = f"data/groups/group{id_group}.json".replace('-', '_')
    result = get_users(file_path)
    info = "Reyting: \n"
    response = result_sort(result)
    if response:
        info += '\n'.join(map(lambda user, i: f"{i}. {user['mention']} - {user['score']} ball", response, range(1, len(response) + 1)))
    await msg.answer(text=info)
    await state.finish()


@dp.message_handler(GroupFilter(), AdminFilter(), state=GameStates.stop)
async def error_stop(msg: types.Message, state: FSMContext):
    await msg.answer("O'yin yakunlangan. Natijalarni elon qiling: /result")
