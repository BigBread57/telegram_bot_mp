from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton
)
from src.buttons.with_all_buttons import (
    help_me,
    list_accepted_tasks,
    list_created_tasks,
    list_denied_tasks,
    list_discussion_tasks,
    list_tasks,
)

cancel = KeyboardButton('/cancel_pm')
skip = KeyboardButton('/skip_pm')


pm_buttons = ReplyKeyboardMarkup(resize_keyboard=True)
pm_buttons_with_skip = ReplyKeyboardMarkup(resize_keyboard=True)
pm_buttons_without_skip = ReplyKeyboardMarkup(resize_keyboard=True)

pm_buttons.row(
    help_me, list_tasks
).row(
    list_created_tasks, list_accepted_tasks,
).row(
    list_denied_tasks, list_discussion_tasks
)
pm_buttons_with_skip.row(cancel, skip)
pm_buttons_without_skip.add(cancel)

action_pm_buttons = InlineKeyboardMarkup(row_width=1)
delete = InlineKeyboardButton(text='Удалить', callback_data='1')
accepted_status = InlineKeyboardButton(text='Подтвердить', callback_data='2')
denied_status = InlineKeyboardButton(text='Отклонить', callback_data='3')
discussion_status = InlineKeyboardButton(text='Обсудить', callback_data='4')
url_jira = InlineKeyboardButton(text='Добавить ссылку на jira', callback_data='5')
comment = InlineKeyboardButton(text='Добавить комментарий к задаче', callback_data='6')
for_jira = InlineKeyboardButton(text='Скопировать инфомрацию для Jira', callback_data='7')

action_pm_buttons.row(
    delete, accepted_status
).row(
    denied_status, discussion_status
).add(url_jira).add(comment).add(for_jira)

