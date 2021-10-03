from ApiBot import get_text_addons

from States.State import State

text_addons = get_text_addons()


class InDevelopTasksState(State):
    """
    Состояние В разработке
    """

    NAME = text_addons['in_develop_Button']

    def __init__(self, *args, **kwargs):
        super(InDevelopTasksState, self).__init__(*args, **kwargs)