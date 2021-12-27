from aiogram import types, Dispatcher

from src.buttons.client_buttons import client_buttons
from src.buttons.pm_buttons import pm_buttons
from src.data_base.request_for_db.utils import add_pm, check_client_is_pm_in_db

from src.settings.common import DICT_PM


async def start(message: types.Message):
    """Привественное слово и запуск кнопок."""
    if message.from_user.username in DICT_PM.keys():
        if not await check_client_is_pm_in_db(message.from_user.username):
            await add_pm(message.from_user)
        await message.reply('Добро пожаловать!', reply_markup=pm_buttons)
    else:
        await message.reply('Добро пожаловать!', reply_markup=client_buttons)


async def help_me(message: types.Message):
    """Помощь пользователю."""
    if message.from_user.username in DICT_PM.keys():
        await message.reply(
            'Данный бот является помощником проектного менеджера. ' +
            'Его функционал заключается в аккумулировании задач пользователей ' +
            'и едином подходе к постановке задач. Список команд: \n' +
            '\\start - запуск бота\n' +
            '\\help - получение справки о возможностях бота\n' +
            '\\list_tasks - получение списка всех задач\n' +
            '\\accepted_tasks - получение списка принятых задач\n' +
            '\\created_tasks - получение списка созданных задач\n' +
            '\\denied_tasks - получение списка отмененных задач\n' +
            '\\discussion_tasks - получение списка дискуссионных задач\n' +
            'ПМ может изменять статус каждой задачи, добавлять комментарии к ней ' +
            'и вставлять ссылку на jira'
        )
    else:
        await message.reply(
            'Данный бот является помощником проектного менеджера. ' +
            'Его функционал заключается в аккумулировании задач пользователей ' +
            'и едином подходе к постановке задач. Список команд: \n' +
            '\\start - запуск бота\n' +
            '\\help - получение справки о возможностях бота\n' +
            '\\new_task - создание задачи (не доступно для ПМ)\n' +
            '\\list_tasks - получение списка всех задач\n' +
            '\\accepted_tasks - получение списка принятых задач\n'
            '\\created_tasks - получение списка созданных задач\n'
            '\\denied_tasks - получение списка отмененных задач\n'
            '\\discussion_tasks - получение списка дискуссионных задач\n'
        )


def register_handlers_other(dp: Dispatcher):
    """Регистрация обработчиков."""
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(help_me, commands=['help'])
