from telebot.types import ReplyKeyboardMarkup, KeyboardButton


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
            KeyboardButton('Назад')
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
        self.bot.set_state(MainState)



class MainState(State):
    """
    Главное окно чат бота
    """

    NAME = 'Главная'

    def entry(self):
        pass

    def on_text_handler(self, message):
        tasks = KeyboardButton(TasksState.NAME)
        stat = KeyboardButton('Статистики')
        set_task = KeyboardButton('Поставить')
        idea = KeyboardButton('Идея')
        data_base_knowledge = KeyboardButton('База знаний')
        contacts = KeyboardButton(ContactsState.NAME)
        self.buttons.add(tasks,stat,set_task, idea, data_base_knowledge, contacts, row_width=2)
        self.bot.send_message(message.chat.id, self.NAME, reply_markup=self.buttons)
        self.reset_buttons()


class TasksState(State):
    """
    Состояние Задачи
    """

    NAME = 'Задачи'

    def on_text_handler(self, message):
        my_tasks = KeyboardButton('Мои задачи')
        i_set = KeyboardButton('Я поставил')
        today = KeyboardButton('На сегодня')
        tomorrow = KeyboardButton('На завтра')
        self.buttons.add(my_tasks, i_set, today, tomorrow,
                                                   row_width=2)

        self.bot.send_message(message.chat.id, self.NAME, reply_markup=self.buttons)
        self.reset_buttons()


class ContactsState(State):
    """
    Состояние контакты
    """

    NAME = "Контакты"

    def on_text_handler(self, message):
        contact1 = KeyboardButton('Контакт 1')
        contact2 = KeyboardButton('Контакт 2')

        self.buttons.add(contact1, contact2, row_width=2)
        self.bot.send_message(message.chat.id, self.NAME, reply_markup=self.buttons)
        self.reset_buttons()