from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from ApiBot import get_text_addons

from States.State import State

text_addons = get_text_addons()


class StatisticState(State):
    """
    Состояние Статистики
    """

    NAME = text_addons['statistic_Button']