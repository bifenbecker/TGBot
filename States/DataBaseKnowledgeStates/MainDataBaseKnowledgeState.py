from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from ApiBot import get_text_addons

from States.State import State

text_addons = get_text_addons()


class DataBaseKnowledgeState(State):
    """
    Состояние База знаний
    """

    NAME = text_addons['database_knowledge_Button']