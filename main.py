from ApiBot import get_api_bot
from Bot import Bot
from BotStates import *

api_bot = get_api_bot()

bot = None


@api_bot.message_handler(content_types=['text'])
def on_text_handler(message):
    if message.text == 'Назад':
        bot.state.return_back()
    else:
        bot.set_state(State.get_cls(message.text))

    bot.on_text_handler(message)


if __name__ == '__main__':
    bot = Bot(MainState)
    api_bot.polling()
