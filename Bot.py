from ApiBot import get_api_bot

api_bot = get_api_bot()

class Bot:

    def __init__(self, state=None):
        self.set_state(state)

    def set_state(self, new_state_cls):
        if new_state_cls:
            new_state = new_state_cls(self)
            self.state = new_state  # Брать из базы у юзера

    def send_message(self, chat_id, text, **kwargs):
        api_bot.send_message(chat_id, text, **kwargs)

    def on_text_handler(self, message):
        if self.state:
            self.state.on_text_handler(message)

