from ApiBot import get_api_bot, get_text_addons
from States.State import State
from Bot import get_bot

text_addons = get_text_addons()
api_bot = get_api_bot()
bot = get_bot()


def reg_handlers():

    @api_bot.message_handler(content_types=['text'])
    def on_text_handler(message):
        if message.text == text_addons['return_Button']:
            bot.state.return_back()
        else:
            bot.set_state(State.get_cls(message.text))

        bot.on_text_handler(message)


