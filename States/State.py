from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from ApiBot import get_text_addons

text_addons = get_text_addons()

class State:
    """
    Базовое состояние чат бота
    """

    NAME = None

    def __init__(self, bot):
        self.bot = bot
        self.reset_buttons()

    def reset_buttons(self):
        self.buttons = ReplyKeyboardMarkup().add(
            KeyboardButton(text_addons['return_Button'])
        )

    @staticmethod
    def get_cls(name=None):
        for cls in State.__subclasses__():
            if cls.NAME == name:
                return cls


    def entry(self):
        """
        Отправка основного сообщения
        :return:
        """
        raise NotImplemented()

    def on_text_handler(self, message):
        """
        Обработка текста
        :param message:
        :return:
        """
        raise NotImplemented()

    def return_back(self):
        """
        Возвращает назад
        :return:
        """
        if self.bot.prev_state:
            self.bot.state = self.bot.prev_state