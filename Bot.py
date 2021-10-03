from ApiBot import get_api_bot, get_text_addons
from States.State import State
from States.MainState import MainState
from users.models import BotUser


api_bot = get_api_bot()
text_addons = get_text_addons()


class Bot:

    def __init__(self):
        self.prev_state = None
        self.state = None
        # self.set_state(state, message.from_user.id)

    def load_user_state(self, user_id: int):
        """
        Загрузка состояние для пользователя из БД
        :return:
        """
        user = BotUser.objects.get(user_id=user_id)
        self.state = State.get_cls(user.state)(self)
        self.prev_state = State.get_cls(user.prev_state)(self)

    def set_state(self, new_state_cls, user_id: int):
        """
        Переход на другое состояние. Сохранение в БД и вызов entry()
        :param new_state_cls: Класс нового состояния
        :return:
        """
        if new_state_cls:
            self.prev_state = self.state
            new_state = new_state_cls(self)
            self.state = new_state
            self.state.entry(user_id)
            user = BotUser.objects.get(user_id=user_id)
            user.state = new_state.NAME
            user.prev_state = MainState.NAME
            user.save()

    def send_message(self, chat_id, text, **kwargs):
        api_bot.send_message(chat_id, text, **kwargs)

    def on_text_handler(self, message):
        if message.text == text_addons['return_Button']:
            self.set_state(State.get_cls(BotUser.objects.get(user_id=message.from_user.id).prev_state), message.from_user.id)
        else:
            if self.state:
                self.state.on_text_handler(message)


# bot = Bot(MainState)
bot = Bot()


def init_bot(message):
    global bot
    try:
        bot = Bot()
        bot.load_user_state(message.from_user.id)
    except:
        bot = Bot()
        bot.set_state(MainState, message.from_user.id)


def get_bot():
    return bot
