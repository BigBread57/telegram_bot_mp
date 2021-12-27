from aiogram import types, Dispatcher
from src.data_base.request_for_db.change_db_pm import (
    delete_task_in_db,
    change_status_in_db,
)
from src.data_base.request_for_db.view_answer import send_answer_for_jira
from src.handlers.pm.jira import start_add_new_url_jira
from src.handlers.pm.note import start_add_new_note


async def action_pm(callback: types.CallbackQuery):
    """Главная функция по распределению действи ПМ."""
    if callback.data == '1':  # удаление задачи
        await delete_task_in_db(callback)
        await callback.message.reply(
            'Выбранная задача удалена. ' +
            'Для получения обновленного списка вызовите одну из оманд фильтрации.',
        )
    elif callback.data == '2':  # изменение статуса на accepted
        await change_status_in_db(callback, 'accepted')
        await callback.message.reply(
            'Статус задачи изменен на Принято ' +
            'Для получения обновленного списка вызовите одну из оманд фильтрации.',
        )
    elif callback.data == '3':  # изменение статуса на denied
        await change_status_in_db(callback, 'denied')
        await callback.message.reply(
            'Статус задачи изменен на Отклонена ' +
            'Для получения обновленного списка вызовите одну из оманд фильтрации.',
        )
    elif callback.data == '4':  # изменение статуса на discussion
        await change_status_in_db(callback, 'discussion')
        await callback.message.reply(
            'Статус задачи изменен на Обсуждение ' +
            'Для получения обновленного списка вызовите одну из оманд фильтрации.',
        )
    elif callback.data == '5':  # добавление ссылки на Jira
        await start_add_new_url_jira(callback)
    elif callback.data == '6':  # добавление заметки к задаче
        await start_add_new_note(callback)
    elif callback.data == '7':  # Выдача информации для копирования в Jira
        await send_answer_for_jira(callback)


def register_handlers_action_pm(dp: Dispatcher):
    """Регистрация обработчиков"""
    dp.register_callback_query_handler(action_pm)
