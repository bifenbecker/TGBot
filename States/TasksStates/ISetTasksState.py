from ApiBot import get_text_addons

from States.State import State

text_addons = get_text_addons()


class ISetTasksState(State):
    """
    Сотояние Я поставил
    """

    NAME = text_addons['i_set_Button']

    def __init__(self, *args, **kwargs):
        super(ISetTasksState, self).__init__(*args, **kwargs)
