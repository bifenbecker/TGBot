from ApiBot import get_text_addons

from States.State import State

text_addons = get_text_addons()


class IdeaBankState(State):
    """
    Состояние Банк идей
    """

    NAME = text_addons['idea_bank_Button']

    def __init__(self, *args, **kwargs):
        super(IdeaBankState, self).__init__(*args, **kwargs)