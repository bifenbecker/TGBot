from ApiBot import get_text_addons

from States.State import State

text_addons = get_text_addons()


class VoiceToManagerState(State):
    """
    Состояние Голосом координатору
    """

    NAME = text_addons['voice_to_manager_Button']

    def __init__(self, *args, **kwargs):
        super(VoiceToManagerState, self).__init__(*args, **kwargs)
        # todo: Get all managers from DB
        self.keyboard = State.create_tg_keyboard([
            [text_addons['return_Button']],
            ['1️⃣Координатор'],
            ['2️⃣Координатор'],
        ])

        self.entry_message = self.NAME + "\nКакому координатору добавить?"

    def on_text_handler(self, message):
        pass