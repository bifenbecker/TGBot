import telebot
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from users.management.commands.run import api_bot


class UpdateBot(APIView):

    def post(self, request):
        json_str = request.body.decode('UTF-8')
        update = telebot.types.Update.de_json(json_str)
        api_bot.process_new_updates([update])
        return Response({'code': 200})


