from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from ApiBot import get_text_addons

from States.State import State

text_addons = get_text_addons()

class SetState(State):
    """
    Состояние Поставить
    """

    NAME = text_addons['set_task_Button']