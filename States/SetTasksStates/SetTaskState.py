from ApiBot import get_text_addons

from States.State import State

from projects.models import *

text_addons = get_text_addons()


class SetTaskState(State):
    """
    Состояние Поставить задачу
    """

    NAME = text_addons['set_task_Button'] + "задачу"

    def __init__(self, *args, **kwargs):
        super(SetTaskState, self).__init__(*args, **kwargs)
        self.keyboard = State.create_tg_keyboard([
            [text_addons['return_Button']],
        ])
