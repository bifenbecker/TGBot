from ApiBot import get_text_addons

from users.models import *
from projects.models import *

from States.State import State
from States.MainState import MainState

text_addons = get_text_addons()


class CreateProjectState(State):
    """
    Состояние создание проекта
    """

    NAME = "Создать проект"

    def __init__(self, *args, **kwargs):
        super(CreateProjectState, self).__init__(*args, **kwargs)
        self.reset_keyboard()

    def entry(self, user_id):
        self.bot.send_message(user_id, "Введите название проекта", reply_markup=self.keyboard)

    def on_text_handler(self, message):
        user = BotUser.objects.filter(user_id=message.from_user.id).first()
        try:
            new_project = Project.objects.create(
                name=message.text,
            )

            new_project_role = ProjectRole.objects.create(
                bot_user=user,
                project=new_project,
                role='CR'
            )
            self.bot.send_message(message.chat.id, f"Проект с названием {message.text} создан")
            self.bot.set_state(MainState, message.from_user.id)
        except:
            self.bot.send_message(message.chat.id, "Не удалось создать проект")