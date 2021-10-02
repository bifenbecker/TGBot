from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from ApiBot import get_text_addons

from States.State import State

text_addons = get_text_addons()


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