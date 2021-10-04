from ApiBot import get_text_addons

from States.State import State

from users.models import BotUser


text_addons = get_text_addons()


class CreateTaskState(State):
    """
    Состояние Создать задачу
    """

    NAME = text_addons['create_task_Button']

    def __init__(self, *args, **kwargs):
        super(CreateTaskState, self).__init__(*args, **kwargs)
        self.entry_message = self.NAME + "\nВ какой проект добавить задачу?"
        self.keyboard = State.create_tg_keyboard([
            [text_addons['return_Button']],
            ['📝Создать новый проект']
        ])

    def entry(self, message):
        buttons = self.get_data_from_db(message.from_user.id)[0]
        values = self.get_data_from_db(message.from_user.id)[1]
        self.keyboard = State.create_tg_keyboard(
            [
                *buttons,
            ],
            [
                *values,
            ]
        )
        # self.bot.send_message(message.from_user.id, '', reply_markup=inline_keyboard)
        super(CreateTaskState, self).entry(message)


    def on_text_handler(self, message):
        print(message.text)

    def get_data_from_db(self, user_id):
        """
        Получение проектов и участников с задачами этих проектов из базы данных пользователя
        :param user_id: User_id пользовател
        :return: список строк - имя_проекта/сколко_учстников/сколько_задач
        """
        numbers = {
            '0': '0️⃣',
            '1': '1️⃣',
            '2': '2️⃣',
            '3': '3️⃣',
            '4': '4️⃣',
            '5': '5️⃣',
            '6': '6️⃣',
            '7': '7️⃣',
            '8': '8️⃣',
            '9': '9️⃣',
        }
        data = []
        values = []
        projects = BotUser.objects.get(user_id=user_id).projects.all()
        num = 1
        for project in projects:
            str_num = ''
            for char in str(num):
                str_num += numbers[char]

            members_of_project = str(len(project.project.members.all()))
            tasks_of_project = str(len(project.project.tasks.all()))
            values.append([str(project.project.id)])
            data.append([f'{str_num}Проект {project.project.name}/👤{members_of_project}/📈{tasks_of_project}'])
            num += 1
        return (data, values)
