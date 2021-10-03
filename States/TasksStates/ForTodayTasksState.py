from ApiBot import get_text_addons

from States.State import State

text_addons = get_text_addons()


class ForTodayTasksState(State):
    """
    Состояние На сегодня Задачи
    """

    NAME = text_addons['today_tasks_Button']

    def __init__(self, *args, **kwargs):
        super(ForTodayTasksState, self).__init__(*args, **kwargs)