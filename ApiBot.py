import telebot

token = "1844053170:AAECRMqnUaVNb11VCB2wnaKtodpezXQtR88"
api_bot = telebot.TeleBot(token=token)

def get_api_bot():
    return api_bot