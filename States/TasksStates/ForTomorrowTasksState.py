from ApiBot import get_text_addons

from States.State import State

text_addons = get_text_addons()


class ForTomorrowTasksState(State):
    """
    Состояние На завтра Задачи
    """

    NAME = text_addons['tomorrow_tasks_Button']

    def __init__(self, *args, **kwargs):
        super(ForTomorrowTasksState, self).__init__(*args, **kwargs)