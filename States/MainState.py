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

    def entry(self):
        pass

    def on_text_handler(self, message):
        tasks = KeyboardButton(TasksState.NAME)
        stat = KeyboardButton(StatisticState.NAME)
        set_task = KeyboardButton(SetState.NAME)
        idea = KeyboardButton(IdeaState.NAME)
        data_base_knowledge = KeyboardButton(DataBaseKnowledgeState.NAME)
        contacts = KeyboardButton(ContactsState.NAME)
        self.buttons.add(tasks,stat,set_task, idea, data_base_knowledge, contacts, row_width=2)
        self.bot.send_message(message.chat.id, self.NAME, reply_markup=self.buttons)
        self.reset_buttons()