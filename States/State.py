import telebot

from ApiBot import get_text_addons
from users.models import BotUser


text_addons = get_text_addons()


def get_all_child_classes(main_cls):
    def is_subclasses(cls_list):
        for cls in cls_list:
            if cls.__subclasses__():
                return True
        return False

    child_list = main_cls.__subclasses__()
    index = 0
    while is_subclasses(child_list):
        cls = child_list[index]
        if cls.__subclasses__():
            del child_list[index]
            new_list = cls.__subclasses__()
            for new_cls in new_list:
                child_list.append(new_cls)

        index += 1

    return child_list


class State:
    """
    Базовое состояние чат бота
    """

    NAME = None

    def __init__(self, bot):
        self.bot = bot
        self.entry_message = ''
        self.state_data = ''

    def reset_keyboard(self):
        self.keyboard = State.create_tg_keyboard([
            [text_addons['return_Button']]
        ])

    @staticmethod
    def get_cls(name):
        cls_list = get_all_child_classes(State)
        for cls in cls_list:
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

    def entry(self, message):
        """
        Отправка основного сообщения
        :return:
        """
        self.bot.send_message(message.from_user.id, self.entry_message, reply_markup=self.keyboard)

    def on_text_handler(self, message):
        """
        Обработка текста
        :param message:
        :return:
        """
        raise NotImplemented()

