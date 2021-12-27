from aiogram.utils import executor


from settings.common import dp


async def on_startup(_):
    print('Работает')


from handlers.client import task
from handlers.with_all import list_task, other
from handlers.pm import action_pm, jira, note

other.register_handlers_other(dp)
list_task.register_handlers_list_task(dp)
task.register_handlers_client_task(dp)
action_pm.register_handlers_action_pm(dp)
jira.register_handlers_jira(dp)
note.register_handlers_note(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
