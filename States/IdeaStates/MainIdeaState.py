from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from ApiBot import get_text_addons

from States.State import State

text_addons = get_text_addons()

class IdeaState(State):
    """
    Состояние Идея
    """

    NAME = text_addons['idea_Button']