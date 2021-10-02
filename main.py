from ApiBot import *
from Bot import Bot
# from BotStates import *
from States.MainState import MainState
from States.State import State

from ApiBot import get_text_addons

text_addons = get_text_addons()

api_bot = get_api_bot()
bot = None


@api_bot.message_handler(content_types=['text'])
def on_text_handler(message):
    print(message)
    if message.text == text_addons['return_Button']:
        bot.state.return_back()
    else:
        user = BotUser.objects.get(user_id=message)
        bot.set_state(State.get_cls(message.text))

    bot.on_text_handler(message)


if __name__ == '__main__':
    bot = Bot(MainState)
    api_bot.polling()
