from aiogram import types, Dispatcher

from src.data_base.request_for_db.filter import filter_task


async def list_tasks(message: types.Message):
    """Выводим список всех задач."""
    await filter_task(message, 'all')


async def list_accepted_tasks(message: types.Message):
    """Выводим список задача со статусом accepted."""
    await filter_task(message, 'accepted')


async def list_created_tasks(message: types.Message):
    """Выводим список задача со статусом created."""
    await filter_task(message, 'created')


async def list_denied_tasks(message: types.Message):
    """Выводим список задача со статусом denied."""
    await filter_task(message, 'denied')


async def list_discussion_tasks(message: types.Message):
    """Выводим список задача со статусом discussion."""
    await filter_task(message, 'discussion')


def register_handlers_list_task(dp: Dispatcher):
    """Регистрация обработчиков"""
    dp.register_message_handler(list_tasks, commands=['list_tasks'])
    dp.register_message_handler(list_accepted_tasks, commands=['accepted_tasks'])
    dp.register_message_handler(list_created_tasks, commands=['created_tasks'])
    dp.register_message_handler(list_denied_tasks, commands=['denied_tasks'])
    dp.register_message_handler(list_discussion_tasks, commands=['discussion_tasks'])
