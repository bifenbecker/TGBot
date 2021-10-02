import telebot
import json
from django.conf import settings

token = "1844053170:AAECRMqnUaVNb11VCB2wnaKtodpezXQtR88"
api_bot = telebot.TeleBot(token=settings.BOT_TOKEN)





def get_api_bot():
    return api_bot


def get_text_addons():
    with open('text_addons.json', 'r', encoding='utf-8') as f:
        return json.load(f)

