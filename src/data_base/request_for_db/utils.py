import re

from src.buttons.pm_buttons import action_pm_buttons
from src.data_base import current_session
from src.data_base.model.file import File
from src.data_base.model.jira import JiraUrl
from src.data_base.model.note import Note
from src.data_base.model.pm import Pm
from src.data_base.model.task import Task
from src.data_base.request_for_db.view_answer import (
    send_answer,
    send_document,
    send_photo,
)
from src.settings.common import bot, DICT_PM


async def get_chat_id_and_status_user(task_id):
    """Получаем все Задачу со всеми файлами, ссылками и заметками."""

    tasks = await qs()
    tasks = tasks.filter(Task.id == task_id).all()
    client = current_session.query(Task).get(task_id)

    await division_message(message=None, tasks=tasks, status=None, pm=None, client=client.author_id)


async def division_message(message, tasks, status, pm, client):
    """Определение каким методом будет осуществлена отправка данных пользователям."""
    # Проверка на то, что у нас есть какие-то данные в БД
    if tasks:
        # Условие для пересылки только-что созданной записи ПМ или пользователю
        if message is None and isinstance(pm, Pm):
            chat_id = pm.user_id
            status_user = 'pm'
        elif message is None and isinstance(pm, int):
            chat_id = pm
            status_user = 'client'
        elif message is not None and pm is None:
            chat_id = message.chat['id']
            status_user = await is_pm(message)
        elif client:
            chat_id = client
            status_user = 'client'

        for task, file, note, jira in tasks:
            if not file:
                if status_user == 'pm':
                    await send_answer(task, note, jira, chat_id, action_pm_buttons)
                else:
                    await send_answer(task, note, jira, chat_id, None)

            elif file.type == 'photo':
                if status_user == 'pm':
                    await send_photo(task, note, jira, chat_id, file.file, action_pm_buttons)
                else:
                    await send_photo(task, note, jira, chat_id, file.file, None)

            elif file.type == 'document':
                if status_user == 'pm':
                    await send_document(task, note, jira, chat_id, file.file, action_pm_buttons)
                else:
                    await send_document(task, note, jira, chat_id, file.file, None)

    else:
        await bot.send_message(chat_id=message.chat['id'], text=f'Нет задач со статусом {status}.')


async def is_pm(message):
    """Функция для определения пользователь ПМ или нет."""
    if message.from_user.username in DICT_PM.keys():
        return 'pm'
    else:
        return 'client'


async def add_pm(user):
    """Добавление информации о ПМ."""
    mew_pm = Pm(
        username=user.username,
        user_id=user.id,
        index=DICT_PM.get(user.username),
    )

    current_session.add(mew_pm)
    current_session.commit()


async def check_client_is_pm_in_db(username):
    """Проверка есть пользователь (который является ПМ) в БД ."""
    pm = current_session.query(Pm).filter_by(username=username).all()
    return True if pm else False


async def get_author(callback):
    """Получаем данные о создателе задачи."""
    if callback.from_user.__getattribute__('first_name'):
        first_name = callback.from_user.first_name
    else:
        first_name = ''
    if callback.from_user.__getattribute__('last_name'):
        last_name = callback.from_user.last_name
    else:
        last_name = ''
    if callback.from_user.__getattribute__('username'):
        username = callback.from_user.username
    else:
        username = ''

    result = '{} {} {}'.format(first_name, last_name, username)
    return result.strip()


async def definition_task_id(callback):
    """Определение id задачи из текста сообщения."""
    if callback.message.__getattribute__('text'):
        text = callback.message.text
    if callback.message.__getattribute__('caption'):
        text = callback.message.caption

    task_id = int(re.findall(r'ID задачи: (\d*)', text)[0])
    task = current_session.query(Task).get(task_id)

    return task


async def change_url_jira_for_task(task_id):
    """Проверка на наличие ссылки в Jira у задачи."""
    count_task = current_session.query(JiraUrl).filter_by(task_id=task_id).one_or_none()
    if count_task:
        return False
    else:
        return True


async def change_note_for_task(task_id):
    """Проверка на наличие заметки для задачи."""
    count_task = current_session.query(Note).filter_by(task_id=task_id).one_or_none()
    if count_task:
        return False
    else:
        return True


async def qs():
    """ПОлучение всех свзяных объектов с task."""
    tasks = current_session.query(Task, File, Note, JiraUrl)
    tasks = tasks.outerjoin(File, File.task_id == Task.id)
    tasks = tasks.outerjoin(Note, Note.task_id == Task.id)
    tasks = tasks.outerjoin(JiraUrl, JiraUrl.task_id == Task.id)
    return tasks
