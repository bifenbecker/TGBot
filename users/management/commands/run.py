from django.core.management.base import BaseCommand

from ApiBot import get_api_bot
from Bot import Bot
from States.MainState import MainState

api_bot = get_api_bot()
bot = None

class Command(BaseCommand):
    help = "Run bot polling"

    def handle(self, *args, **options):
        global bot
        bot = Bot(MainState)
        api_bot.set_webhook('localhost/fokus-bot/retgefafsfwegbfbvf')
        api_bot.polling()