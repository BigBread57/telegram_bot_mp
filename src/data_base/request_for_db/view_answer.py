from src.buttons.pm_buttons import action_pm_buttons
from src.data_base.request_for_db import utils
from src.settings.common import bot


answer = (
    '-------------------------------------\n' +
    '🔢 ID задачи: {}\n\n' +
    '🖋 Автор: {}\n\n' +
    '🗂 Проект: {}\n' +
    '-------------------------------------\n' +
    '⏱ Действия: {}\n\n' +
    '❓ Ожидания: {}\n\n' +
    '❗️ Реальность: {}\n\n' +
    '⌚️️ Приспособления: {}\n' +
    '-------------------------------------\n' +
    '📞 Консультация: {}\n\n' +
    '🛠 Ответсвенный: {}\n' +
    '-------------------------------------\n' +
    'Статус: {}\n\n' +
    '📌 Заметка к задаче: {}\n' +
    '-------------------------------------\n' +
    '🌐 Url в Jira: {}\n\n' +
    '📌 Заметка к url: {}\n'
)


answer_for_jira = (
    '*Проект:* {}\n\n' +
    '*Действия для воспроизведения ошибки:* {}\n\n' +
    '*Ожидания (что и как должно работать в действительности):* {}\n\n' +
    '*Реальность (что и как работает сейчас):* {}\n\n' +
    '*Приспособления:* {}\n\n' +
    '*Консультация:* {}\n\n'
)


async def send_answer(task, note, jira, chat_id, reply_markup):
    """Функция для отправки сообщения."""
    note_text = await chek_note(note)
    jira_url = await chek_jira(jira, 'url')
    jira_note = await chek_jira(jira, 'note')
    await bot.send_message(
        chat_id=chat_id,
        text=answer.format(
            task.id,
            task.author,
            task.project,
            task.action,
            task.purpose,
            task.real,
            task.fixtures,
            task.consultation,
            task.responsible,
            task.status,
            note_text,
            jira_url,
            jira_note,
        ),
        reply_markup=reply_markup,
    )


async def send_photo(task, note, jira, chat_id, photo, reply_markup):
    """Функция для отправки фотографии и сообщения."""
    note_text = await chek_note(note)
    jira_url = await chek_jira(jira, 'url')
    jira_note = await chek_jira(jira, 'note')
    await bot.send_photo(
        chat_id=chat_id,
        photo=photo,
        caption=answer.format(
            task.id,
            task.author,
            task.project,
            task.action,
            task.purpose,
            task.real,
            task.fixtures,
            task.consultation,
            task.responsible,
            task.status,
            note_text,
            jira_url,
            jira_note,
        ),
        reply_markup=reply_markup,
    )


async def send_document(task, note, jira, chat_id, document, reply_markup):
    """Функция для отправки документа и сообщения."""
    note_text = await chek_note(note)
    jira_url = await chek_jira(jira, 'url')
    jira_note = await chek_jira(jira, 'note')
    await bot.send_document(
        chat_id=chat_id,
        document=document,
        caption=answer.format(
            task.id,
            task.author,
            task.project,
            task.action,
            task.purpose,
            task.real,
            task.fixtures,
            task.consultation,
            task.responsible,
            task.status,
            note_text,
            jira_url,
            jira_note,
        ),
        reply_markup=reply_markup,
    )


async def send_answer_for_jira(callback):
    task = await utils.definition_task_id(callback)

    await bot.send_message(
        chat_id=callback.from_user.id,
        text=answer_for_jira.format(
            task.project,
            task.action,
            task.purpose,
            task.real,
            task.fixtures,
            task.consultation,
        ),
        parse_mode='Markdown',
    )


async def chek_note(note):
    """Проверка существования Note для отправки сообщения."""
    if note:
        return note.text
    else:
        return ''


async def chek_jira(jira, field):
    """Проверка существования JiraUrl для отправки сообщения."""
    if jira:
        if field == 'url':
            return jira.url
        else:
            return jira.note
    return ''
