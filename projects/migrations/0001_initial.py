# Generated by Django 3.2.7 on 2021-10-02 12:04

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Проект',
                'verbose_name_plural': 'Проекты',
            },
        ),
        migrations.CreateModel(
            name='ProjectRoleInviteLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link_id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('role', models.CharField(choices=[('TP', 'Постановщик'), ('PF', 'Исполнитель'), ('CT', 'Проверка'), ('MG', 'Координатор'), ('DR', 'Руководитель'), ('CR', 'Создатель')], max_length=2, verbose_name='Роль')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активная')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Создана')),
                ('used_date', models.DateTimeField(blank=True, null=True, verbose_name='Использована')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='users.botuser', verbose_name='Создатель')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invite_links', to='projects.project', verbose_name='Проект')),
            ],
            options={
                'verbose_name': 'Ссылка приглашения',
                'verbose_name_plural': 'Ссылки приглашения',
            },
        ),
        migrations.CreateModel(
            name='ProjectRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активная')),
                ('role', models.CharField(choices=[('TP', 'Постановщик'), ('PF', 'Исполнитель'), ('CT', 'Проверка'), ('MG', 'Координатор'), ('DR', 'Руководитель'), ('CR', 'Создатель')], max_length=2, verbose_name='Роль')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('bot_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='users.botuser', verbose_name='Пользователь')),
                ('invite_link', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_role', to='projects.projectroleinvitelink', verbose_name='Ссылка приглашения')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='projects.project', verbose_name='Проект')),
            ],
            options={
                'verbose_name': 'Роль в проекте',
                'verbose_name_plural': 'Роли в проектах',
            },
        ),
    ]