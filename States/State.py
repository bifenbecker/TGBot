import telebot

from ApiBot import get_text_addons
from users.models import BotUser


text_addons = get_text_addons()


class State:
    """
    Базовое состояние чат бота
    """

    NAME = None

    def __init__(self, bot):
        self.bot = bot

    def reset_keyboard(self):
        self.keyboard = State.create_tg_keyboard([
            [text_addons['return_Button']]
        ])

    @staticmethod
    def get_cls(name):
        for cls in State.__subclasses__():
            if cls.NAME == name:
                return cls

        raise IndexError(f"Not exists such class: {name}")

    @staticmethod
    def create_tg_keyboard(texts, datas=None, one_time_keyboard=None):
        if one_time_keyboard is False:
            one_time_keyboard = None
        if datas:
            keyboard = telebot.types.InlineKeyboardMarkup()
            for i in range(len(texts)):
                keyboard.add(*[telebot.types.InlineKeyboardButton(texts[i][j], callback_data=datas[i][j]) for j in
                               range(len(texts[i]))])
        else:
            keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=one_time_keyboard)
            for text in texts:
                keyboard.row(*text)
        return keyboard

    def entry(self, user_id):
        """
        Отправка основного сообщения
        :return:
        """
        self.keyboard = State.create_tg_keyboard([
            [text_addons['return_Button']]
        ])
        self.bot.send_message(user_id, self.NAME, reply_markup=self.keyboard)

    def on_text_handler(self, message):
        """
        Обработка текста
        :param message:
        :return:
        """
        raise NotImplemented()
