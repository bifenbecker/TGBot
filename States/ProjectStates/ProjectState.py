from ApiBot import get_text_addons

from States.State import State
from States.ProjectStates.BaseProject import BaseProject
from States.ProjectStates.MembersOfProjectState import MembersOfProjectState
from States.SetTasksStates.SetTaskState import SetTaskState

from projects.models import *


text_addons = get_text_addons()


class ProjectState(BaseProject):
    """
    Состояние Проект
    """

    NAME = 'Проект'

    def __init__(self, *args, **kwargs):
        super(ProjectState, self).__init__(*args, **kwargs)
        self.keyboard = State.create_tg_keyboard([
            [text_addons['return_Button']],
            [MembersOfProjectState.NAME],
            [SetTaskState.NAME]
        ])
    
    def entry(self, message):
        self.project_uuid = message.data
        BaseProject.project_uuid = message.data
        project = Project.objects.get(id=self.project_uuid)
        self.entry_message = self.NAME + ' ' + project.name
        super(ProjectState, self).entry(message)


    def on_text_handler(self, message):
        print(message)