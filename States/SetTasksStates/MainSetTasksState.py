from ApiBot import get_text_addons

from States.State import State
from States.SetTasksStates.VoiceToManagerState import VoiceToManagerState
from States.SetTasksStates.CreateTaskState import CreateTaskState


text_addons = get_text_addons()

class SetTasksState(State):
    """
    Состояние Поставить
    """

    NAME = text_addons['set_task_Button']

    def __init__(self, *args, **kwargs):
        super(SetTasksState, self).__init__(*args, **kwargs)
        self.keyboard = State.create_tg_keyboard([
            [text_addons['return_Button']],
            [VoiceToManagerState.NAME],
            [CreateTaskState.NAME],
        ])

        self.entry_message = self.NAME

    def on_text_handler(self, message):
        pass