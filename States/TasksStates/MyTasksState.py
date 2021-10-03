from ApiBot import get_text_addons

from States.State import State

text_addons = get_text_addons()


class MyTasksState(State):
    """
    Состояние Мои задачи
    """

    NAME = text_addons['my_tasks_Button']

    def __init__(self, *args, **kwargs):
        super(MyTasksState, self).__init__(*args, **kwargs)
        self.keyboard = State.create_tg_keyboard([
            [text_addons['return_Button']],
            ['За период'],
            ['Все активные задачи'],
            ['Все выполненые задачи'],
            ['Все отмененные задачи'],
            ['Задачи в Банке идей']
        ])