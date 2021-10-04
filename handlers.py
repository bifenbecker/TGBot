from ApiBot import get_api_bot, get_text_addons
from States.State import State
from Bot import get_bot, init_bot
from users.models import *


from States.ProjectStates.CreateProjectState import CreateProjectState
from States.MainState import MainState

from datetime import datetime

text_addons = get_text_addons()
api_bot = get_api_bot()
bot = get_bot()


def check_is_user_or_create(message):
    """
    Проверка сущестует ли пользователь и создать, если не существует
    :param user_id: ID Пользователя
    :return:
    """
    user = BotUser.objects.filter(user_id=message.from_user.id).first()
    if not user:

        user = BotUser.objects.create(
            user_id=message.from_user.id,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            username=message.from_user.username,
        )

    if not user.states.all():
        state = State.objects.create(
            name=MainState.NAME
        )
        state_to_bot_user = StateToBotUser.objects.create(
            bot_user=user,
            state=state,
            state_data=''
        )
        state_to_bot_user_default_prev = StateToBotUser.objects.create(
            bot_user=user,
            state=state,
            state_data=''
        )

    bot.load_user_state(message.from_user.id)

def reg_handlers():

    @api_bot.message_handler(commands=['newproject'])
    def new_project_handler(message):
        check_is_user_or_create(message)
        bot.set_state(CreateProjectState, message.from_user.id)


    @api_bot.message_handler(commands=['start'])
    def new_program_handler(message):
        check_is_user_or_create(message)
        init_bot(message)

    @api_bot.message_handler(content_types=['text'])
    def on_text_handler(message):
        if bot:
            check_is_user_or_create(message)
            bot.on_text_handler(message)
        else:
            api_bot.send_message(message.chat.id, "Введите '/start'")

    @api_bot.callback_query_handler(func=lambda call: True)
    def handle_callback_inline(call):
        check_is_user_or_create(call)
        if call.data == '/newproject':
            new_project_handler(call)
        else:
            bot.handle_callback_inline(call)






