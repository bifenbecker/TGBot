from datetime import datetime

from django.db import models
import logging

# Create your models here.


logger = logging.getLogger('fokusbot')


class BotUser(models.Model):
    user_id = models.IntegerField(unique=True, verbose_name="Telegram ID")
    first_name = models.CharField(max_length=64, verbose_name="Имя")
    last_name = models.CharField(max_length=64, blank=True, null=True, verbose_name="Фамилия")
    username = models.CharField(max_length=32, blank=True, null=True, verbose_name="Никнейм")
    last_active_date = models.DateTimeField(auto_now=True, verbose_name="Последняя активность")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    @property
    def current_state(self):
        return self.states.all().last()

    def set_state(self, state_name: str, state_data: dict):
        state = State.objects.filter(name=state_name).first()
        if not state:
            state = State.objects.create(
                name=state_name
            )

        state_to_bot_user = StateToBotUser.objects.create(
            bot_user=self,
            state=state,
            state_data=str(state_data)
        )
        self.save()

    @property
    def prev_state(self):
        return self.states.exclude(state=self.current_state.state).last()
        # return list(self.states.all())[-2]

    def __str__(self):
        return f"{self.first_name}{('' if self.last_name is None else ' ' + self.last_name)}{('' if self.username is None else ' @' + self.username)}"

    class Meta:
        verbose_name = 'Пользователь бота'
        verbose_name_plural = 'Пользователи бота'


class State(models.Model):
    name = models.CharField(max_length=64, verbose_name="Имя состояния")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статус состояния'
        verbose_name_plural = 'Статусы состояния'


class StateToBotUser(models.Model):
    bot_user = models.ForeignKey('BotUser', on_delete=models.CASCADE, related_name='states', verbose_name='Пользователь')
    state = models.ForeignKey('State', related_name='+', on_delete=models.PROTECT, null=True, blank=True, verbose_name="Статус сотсояния")
    state_data = models.CharField(max_length=64, verbose_name="Информация о состоянии")

    # started_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    # finished_at = models.DateTimeField(null=True, default=None, verbose_name="Дата окончания")

    def __str__(self):
        return self.state.name

    class Meta:
        verbose_name = 'Статус состояние к состоянию'
        verbose_name_plural = 'Статус состояния к состояниям'