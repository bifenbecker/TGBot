from ApiBot import get_text_addons

from States.State import State

from States.TasksStates.MyTasksState import MyTasksState
from States.TasksStates.ISetTasksState import ISetTasksState
from States.TasksStates.ForTomorrowTasksState import ForTomorrowTasksState
from States.TasksStates.ForTodayTasksState import ForTodayTasksState
from States.TasksStates.IdeaBankState import IdeaBankState
from States.TasksStates.InDevelopTasksState import InDevelopTasksState

text_addons = get_text_addons()


class TasksState(State):
    """
    Состояние Задачи
    """

    NAME = text_addons['tasks_Button']

    def __init__(self, *args, **kwargs):
        super(TasksState, self).__init__(*args, **kwargs)
        self.keyboard = State.create_tg_keyboard([
            [text_addons['return_Button']],
            [MyTasksState.NAME, ISetTasksState.NAME],
            [ForTodayTasksState.NAME, ForTomorrowTasksState.NAME],
            [IdeaBankState.NAME, InDevelopTasksState.NAME]
        ])

    def entry(self, user_id):
        self.bot.send_message(user_id, self.NAME + "(entry)",
                              reply_markup=self.keyboard)

    def on_text_handler(self, message):
        self.bot.send_message(message.chat.id, self.NAME + "(хендлер)", reply_markup=self.keyboard)
