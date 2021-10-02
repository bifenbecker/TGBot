from django.db import models
import logging
import uuid
from users.models import BotUser

# Create your models here.


logger = logging.getLogger('fokusbot')


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, verbose_name="Название")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.name

    def get_bot_user_roles(self, bot_user: BotUser):
        return [pr.role for pr in ProjectRole.objects.filter(bot_user=bot_user, project=self, is_active=True).order_by('created_date')]

    def get_bot_user_role(self, bot_user: BotUser, role: str):
        return ProjectRole.objects.filter(bot_user=bot_user, project=self, is_active=True, role=role).first()

    def get_active_members(self):
        return ProjectRole.objects.filter(project=self, is_active=True).order_by('created_date').all()

    def get_active_tasks(self):
        return list(filter(lambda t: t.get_state() not in ('DN', 'CL'), self.tasks.order_by('created_date')))

    def get_members_by_role(self, role: str):
        return list(ProjectRole.objects.filter(project=self, is_active=True, role=role).order_by('created_date'))

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'


class ProjectRole(models.Model):
    ROLE_CHOICES = (
        ("TP", "Постановщик"),  # task producer
        ("PF", "Исполнитель"),  # performer
        ("CT", "Проверка"),  # control
        ("MG", "Координатор"),  # manager
        ("DR", "Руководитель"),  # director
        ("CR", "Создатель"),  # creator
    )

    bot_user = models.ForeignKey(
        BotUser,
        models.CASCADE,
        related_name="projects",
        verbose_name="Пользователь"
    )
    project = models.ForeignKey(
        Project,
        models.CASCADE,
        related_name='members',
        verbose_name="Проект"
    )
    invite_link = models.OneToOneField(
        'ProjectRoleInviteLink',
        models.CASCADE,
        blank=True,
        null=True,
        related_name='project_role',
        verbose_name="Ссылка приглашения"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активная")
    role = models.CharField(max_length=2, choices=ROLE_CHOICES, verbose_name="Роль")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Создано")

    def __str__(self):
        return str(self.bot_user) + " - " + str(self.get_role_display())

    class Meta:
        verbose_name = 'Роль в проекте'
        verbose_name_plural = 'Роли в проектах'


class ProjectRoleInviteLink(models.Model):
    created_by = models.ForeignKey(
        BotUser,
        models.CASCADE,
        related_name="+",
        verbose_name="Создатель"
    )
    project = models.ForeignKey(
        Project,
        models.CASCADE,
        related_name='invite_links',
        verbose_name="Проект"
    )
    link_id = models.UUIDField(default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=2, choices=ProjectRole.ROLE_CHOICES, verbose_name="Роль")
    is_active = models.BooleanField(default=True, verbose_name="Активная")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Создана")
    used_date = models.DateTimeField(blank=True, null=True, verbose_name="Использована")

    def __str__(self):
        return str(self.project) + " - " + str(self.get_role_display())

    class Meta:
        verbose_name = 'Ссылка приглашения'
        verbose_name_plural = 'Ссылки приглашения'
