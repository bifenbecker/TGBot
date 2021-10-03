from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from ApiBot import get_text_addons

from States.State import State
from States.TasksStates.MainTasksState import TasksState
from States.StatisticStates.MainStatisticState import StatisticState
from States.SetTasksStates.MainSetTasksState import SetState
from States.IdeaStates.MainIdeaState import IdeaState
from States.DataBaseKnowledgeStates.MainDataBaseKnowledgeState import DataBaseKnowledgeState
from States.ContactsStates.MainContactsState import ContactsState

text_addons = get_text_addons()

class MainState(State):
    """
    Главное окно чат бота
    """

    NAME = 'Главная'

    def __init__(self, *args, **kwargs):
        self.keyboard = State.create_tg_keyboard(
            [
                [TasksState.NAME, StatisticState.NAME],
                [SetState.NAME, IdeaState.NAME],
                [DataBaseKnowledgeState.NAME, ContactsState.NAME]
            ]
        )
        super(MainState, self).__init__(*args, **kwargs)

    def entry(self, user_id):
        self.bot.send_message(user_id, self.NAME + "\nДля создание проекта введите '/newproject'", reply_markup=self.keyboard)


    def on_text_handler(self, message):
        try:
            self.bot.set_state(State.get_cls(message.text), message.chat.id)
        except IndexError as e:
            print(str(e))
        # except Exception as e:
        #     print(str(e))

        # self.bot.send_message(message.chat.id, self.NAME, reply_markup=self.keyboard)


