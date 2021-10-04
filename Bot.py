from ApiBot import get_api_bot, get_text_addons

from States.State import State
from States.MainState import MainState
from States.ProjectStates.ProjectState import ProjectState

from users.models import BotUser
from projects.models import *


api_bot = get_api_bot()
text_addons = get_text_addons()


class Bot:

    def __init__(self):
        self.prev_state = None
        self.state = None

    def load_user_state(self, user_id: int):
        """
        Загрузка состояние для пользователя из БД
        :return:
        """
        user = BotUser.objects.get(user_id=user_id)
        self.state = State.get_cls(user.current_state.state.name)(self)
        self.prev_state = State.get_cls(user.prev_state.state.name)(self)

    def set_state(self, new_state_cls, message):
        """
        Переход на другое состояние. Сохранение в БД и вызов entry()
        :param new_state_cls: Класс нового состояния
        :return:
        """
        if new_state_cls:
            self.prev_state = self.state.__class__
            new_state = new_state_cls(self)
            self.state = new_state
            self.state.entry(message)
            user = BotUser.objects.get(user_id=message.from_user.id)
            user.set_state(self.state.NAME, self.state.state_data)

    def on_text_handler(self, message):
        if message.text == text_addons['return_Button']:
            user = BotUser.objects.get(user_id=message.from_user.id)
            user.current_state.delete()
            self.load_user_state(message.from_user.id)
            self.state.entry(message)
        else:
            if self.state:
                try:
                    self.switch_state(message)
                except IndexError:
                    self.state.on_text_handler(message)
                # except Exception as e:
                #     print(str(e))

    def handle_callback_inline(self, message):
        try:
            project = Project.objects.get(id=message.data)
            self.set_state(ProjectState, message)
        except Exception as e:
            print(str(e))

    def switch_state(self, message):
        """
        Переключение состояния
        Если исключение, то такого состояния нет и скорее всего его не переключают
        :param message:
        :return:
        """

        try:
            self.set_state(State.get_cls(message.text), message)
        except IndexError:
            raise IndexError

    def send_message(self, chat_id, text, **kwargs):
        api_bot.send_message(chat_id, text, **kwargs)

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
