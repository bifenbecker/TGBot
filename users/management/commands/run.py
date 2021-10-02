from django.core.management.base import BaseCommand

from ApiBot import get_api_bot
from Bot import get_bot
from States.MainState import MainState
from handlers import reg_handlers

api_bot = get_api_bot()

class Command(BaseCommand):
    help = "Run bot polling"

    def handle(self, *args, **options):
        bot = get_bot()
        reg_handlers()
        api_bot.polling()
