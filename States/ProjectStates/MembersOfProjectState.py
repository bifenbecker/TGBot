from ApiBot import get_text_addons

from States.State import State
from States.ProjectStates.BaseProject import BaseProject

from projects.models import *

text_addons = get_text_addons()
NAME = text_addons['members_of_project_Button']

class MembersOfProjectState(BaseProject):
    """
    Состояние Участников проекта
    """

    NAME = text_addons['members_of_project_Button']

    def __init__(self, *args, **kwargs):
        super(MembersOfProjectState, self).__init__(*args, **kwargs)
        self.keyboard = State.create_tg_keyboard([
            [text_addons['return_Button']],
        ])

    def entry(self, message):
        if self.project_uuid:
            project = Project.objects.get(id=self.project_uuid)
            members = project.members.all()
            for member in members:
                self.entry_message += member.bot_user.username

            State.entry(message)

    # def on_text_handler(self, message):
    #     print(message)


