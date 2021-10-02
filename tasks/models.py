from django.db import models
from django.conf import settings
import logging
from datetime import datetime
import pytz
from users.models import BotUser
from projects.models import Project, ProjectRole

# Create your models here.


logger = logging.getLogger('fokusbot')
TIME_ZONE = pytz.timezone(settings.TIME_ZONE)


class Task(models.Model):
    project = models.ForeignKey(
        Project,
        models.CASCADE,
        related_name="tasks",
        verbose_name="Проект"
    )
    members = models.ManyToManyField(
        ProjectRole,
        related_name="tasks",
        verbose_name="Участники"
    )

    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.CharField(max_length=5000, verbose_name="Описание")
    start_date = models.DateTimeField(verbose_name="Время начала")
    end_date = models.DateTimeField(verbose_name="Время окончания")
    is_overdue = models.BooleanField(default=False, verbose_name='Задача просрочена')
    is_finished = models.BooleanField(default=False, verbose_name='Задача завершена')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"{self.title}"

    def is_creation_finished(self):
        return all([x is not None for x in (self.title, self.description, self.start_date, self.end_date)])

    def get_unfilled_roles(self):
        return list(filter(lambda r: self.project.members.filter(is_active=True, role=r), ('TP', 'PF', 'CT', 'MG', 'DR')))

    def get_state(self, as_obj=False):
        states = self.states.filter(end_date__isnull=True).order_by('start_date').all()
        if len(states) == 1:
            state = states[0]
        elif len(states) == 0:
            logger.warning(f"Task with id {self.id} dont have active state")
            state = TaskState(
                task=self,
                state='UP',
            )
            state.save()
        else:
            logger.warning(f"Task with id {self.id} have multiple active states")
            state = states[-1]
        return state if as_obj else state.state

    def set_state(self, state: str):
        curr_state = self.get_state(as_obj=True)
        curr_state.end_date = TIME_ZONE.localize(datetime.now())
        curr_state.save()
        TaskState.objects.create(task=self, state=state)
        if state in ('DN', 'CL'):
            self.is_finished = True
            self.save()

    def get_members_by_role(self, role: str):
        return list(self.members.filter(is_active=True, role=role))

    def get_roles_by_user(self, bot_user: BotUser, as_obj=False):
        return [(pr if as_obj else pr.role) for pr in self.members.filter(bot_user=bot_user, is_active=True)]

    def get_bot_user_role(self, bot_user: BotUser, role: str):
        return self.members.filter(bot_user=bot_user, is_active=True, role=role).first()

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


class TaskState(models.Model):
    TASK_STATE_CHOCIES = (
        ('UP', 'Запланирована'),  # upcoming
        ('IP', 'В работе'),  # in progress
        ('DN', 'Выполнена'),  # done
        ('CL', 'Отменена'),  # canceled
    )

    task = models.ForeignKey(
        Task,
        models.CASCADE,
        related_name="states",
        verbose_name="Задача"
    )
    state = models.CharField(max_length=2, choices=TASK_STATE_CHOCIES, verbose_name="Статус")
    start_date = models.DateTimeField(auto_now_add=True, verbose_name="Время начала")
    end_date = models.DateTimeField(blank=True, null=True, verbose_name="Время конца")

    def __str__(self):
        return str(self.task) + " - " + str(self.state)

    class Meta:
        verbose_name = 'Статус задачи к задаче'
        verbose_name_plural = 'Статусы задачи к задачам'


class TaskConfirm(models.Model):
    task = models.ForeignKey(
        Task,
        models.CASCADE,
        related_name="confirms",
        verbose_name="Задача"
    )
    confirmed_by = models.ForeignKey(
        ProjectRole,
        models.PROTECT,
        related_name="confirms_created",
        verbose_name="Исполнитель"
    )
    is_checked = models.BooleanField(blank=True, null=True, verbose_name='Проверена')
    comment = models.CharField(max_length=5000, blank=True, null=True, verbose_name="Комментарий")
    checked_by = models.ForeignKey(
        ProjectRole,
        models.PROTECT,
        blank=True,
        null=True,
        related_name="confirms_checked",
        verbose_name="Проверяющий"
    )
    checked_date = models.DateTimeField(blank=True, null=True, verbose_name='Проверена')

    def __str__(self):
        return str(self.task)

    class Meta:
        verbose_name = 'Подтверждение задачи'
        verbose_name_plural = 'Подтверждения задач'


def task_confirm_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/task_<id>/<filename>
    return 'task_{0}/{1}'.format(instance.task_confirm.task.id, filename)


class TaskConfirmFile(models.Model):
    task_confirm = models.ForeignKey(
        TaskConfirm,
        models.CASCADE,
        related_name='files',
        verbose_name="К подтверждению задачи"
    )
    file_id = models.CharField(max_length=50, verbose_name='ID файла телеграм')
    file_type = models.CharField(max_length=10, verbose_name='Тип файла')

    def __str__(self):
        return self.file_id

    class Meta:
        verbose_name = 'Файл к подтверждению задачи'
        verbose_name_plural = 'Файлы к подтверждению задач'


def task_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/task_<id>/<filename>
    if instance.task:
        return 'task_{0}/{1}'.format(instance.task.id, filename)
    else:
        return 'temp/{0}'.format(filename)


class TaskFile(models.Model):
    task = models.ForeignKey(
        Task,
        models.CASCADE,
        blank=True,
        null=True,
        related_name='files',
        verbose_name="К задаче"
    )
    file = models.FileField(upload_to=task_directory_path)

    def __str__(self):
        return self.file.name

    class Meta:
        verbose_name = 'Файл к задаче'
        verbose_name_plural = 'Файлы к задачам'


class Refinement(models.Model):
    task = models.ForeignKey(
        Task,
        models.CASCADE,
        related_name='refinements',
        verbose_name="К задаче"
    )
    description = models.CharField(max_length=3000, verbose_name="Описание")
    new_end_date = models.DateTimeField(verbose_name="Время окончания")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return str(self.task) + " >> " + str(self.new_end_date)

    class Meta:
        verbose_name = 'Доработка'
        verbose_name_plural = 'Доработки'


class Postponement(models.Model):
    task = models.ForeignKey(
        Task,
        models.CASCADE,
        related_name='postponements',
        verbose_name="К задаче"
    )
    new_start_date = models.DateTimeField(blank=True, null=True, verbose_name="Время начала")
    new_end_date = models.DateTimeField(verbose_name="Время окончания")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return str(self.task) + " >> (" + str(self.new_start_date) + "-" + str(self.new_end_date) + ")"

    class Meta:
        verbose_name = 'Отсрочка'
        verbose_name_plural = 'Отсрочки'
