from django.db import models
import logging

# Create your models here.


logger = logging.getLogger('fokusbot')


class BotUser(models.Model):
    user_id = models.IntegerField(unique=True, verbose_name="Telegram ID")
    first_name = models.CharField(max_length=64, verbose_name="Имя")
    last_name = models.CharField(max_length=64, blank=True, null=True, verbose_name="Фамилия")
    username = models.CharField(max_length=32, blank=True, null=True, verbose_name="Никнейм")
    state = models.CharField(max_length=32, blank=True, null=True, verbose_name="Статус чата")
    prev_state = models.CharField(max_length=32, blank=True, null=True, verbose_name="Предыдущий статус чата")
    last_active_date = models.DateTimeField(auto_now=True, verbose_name="Последняя активность")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"{self.first_name}{('' if self.last_name is None else ' ' + self.last_name)}{('' if self.username is None else ' @' + self.username)}"

    class Meta:
        verbose_name = 'Пользователь бота'
        verbose_name_plural = 'Пользователи бота'
