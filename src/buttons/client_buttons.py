from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButton,
    ReplyKeyboardMarkup
)
from src.buttons.with_all_buttons import (
    help_me,
    list_accepted_tasks,
    list_created_tasks,
    list_denied_tasks,
    list_discussion_tasks,
    list_tasks,
)
from src.settings.common import DICT_PM


new_task = KeyboardButton('/new_task')
cancel = KeyboardButton('/cancel_client')
skip = KeyboardButton('/skip_client')


client_buttons = ReplyKeyboardMarkup(resize_keyboard=True)
client_buttons_with_skip = ReplyKeyboardMarkup(resize_keyboard=True)
client_buttons_without_skip = ReplyKeyboardMarkup(resize_keyboard=True)

client_buttons.row(
    new_task, help_me, list_tasks
).row(
    list_created_tasks, list_accepted_tasks,
).row(
    list_denied_tasks, list_discussion_tasks
)

client_buttons_with_skip.row(cancel, skip)
client_buttons_without_skip.add(cancel)

pm = InlineKeyboardMarkup(row_width=1)
for key, value in DICT_PM.items():
    pm.add(InlineKeyboardButton(text=key, callback_data=value))
