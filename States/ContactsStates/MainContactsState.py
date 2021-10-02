from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from ApiBot import get_text_addons

from States.State import State

text_addons = get_text_addons()


class ContactsState(State):
    """
    Состояние контакты
    """

    NAME = text_addons['contacts_Button']

    def on_text_handler(self, message):
        contact1 = KeyboardButton('Контакт 1')
        contact2 = KeyboardButton('Контакт 2')

        self.buttons.add(contact1, contact2, row_width=2)
        self.bot.send_message(message.chat.id, self.NAME, reply_markup=self.buttons)
        self.reset_buttons()