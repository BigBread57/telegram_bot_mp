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


async def send_answer(task, comment, jira, chat_id, reply_markup):
    """Функция для отправки сообщения."""
    comment_text = await chek_comment(comment)
    jira_url = await chek_jira(jira, 'url')
    jira_comment = await chek_jira(jira, 'comment')
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
            comment_text,
            jira_url,
            jira_comment,
        ),
        reply_markup=reply_markup,
    )


async def send_photo(task, comment, jira, chat_id, photo, reply_markup):
    """Функция для отправки фотографии и сообщения."""
    comment_text = await chek_comment(comment)
    jira_url = await chek_jira(jira, 'url')
    jira_comment = await chek_jira(jira, 'comment')
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
            comment_text,
            jira_url,
            jira_comment,
        ),
        reply_markup=reply_markup,
    )


async def send_document(task, comment, jira, chat_id, document, reply_markup):
    """Функция для отправки документа и сообщения."""
    comment_text = await chek_comment(comment)
    jira_url = await chek_jira(jira, 'url')
    jira_comment = await chek_jira(jira, 'comment')
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
            comment_text,
            jira_url,
            jira_comment,
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


async def chek_comment(comment):
    """Проверка существования comment для отправки сообщения."""
    if comment:
        return comment.text
    else:
        return ''


async def chek_jira(jira, field):
    """Проверка существования JiraUrl для отправки сообщения."""
    if jira:
        if field == 'url':
            return jira.url
        else:
            return jira.comment
    return ''
