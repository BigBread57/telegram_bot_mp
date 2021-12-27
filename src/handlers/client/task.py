from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from src.buttons.client_buttons import (
    client_buttons,
    pm, client_buttons_without_skip, client_buttons_with_skip,
)
from src.data_base.request_for_db.task import add_new_task_in_db
from src.data_base.request_for_db.utils import get_author


class FSMNewTask(StatesGroup):
    """Класс конечных автоматов для задачи."""
    pm = State()
    project = State()
    action = State()
    purpose = State()
    real = State()
    consultation = State()
    responsible = State()
    fixtures = State()
    file = State()


async def start_add_new_task(message: types.Message):
    """Начинаем создание задачи и даем право выбрать ПМ."""
    await FSMNewTask.pm.set()
    await message.reply(
        'Для создания задачи пройдите небольшой опрос.',
        reply_markup=client_buttons_without_skip,
    )
    await message.answer('Укажите PM.', reply_markup=pm)


async def pm_call(
        callback: types.CallbackQuery,
        state: FSMContext,
):
    """Запоминаем результат выбора ПМ и сохраняем данные об авторе задачи."""
    async with state.proxy() as data:
        data['author'] = await get_author(callback)
        data['author_id'] = callback.from_user.id
        data['index_pm'] = callback.data
    await FSMNewTask.next()
    await callback.message.reply(
        'Введите название проекта для которого ставится задача ' +
        '(пример: nova_band; django_nova_health и т.д.).',
    )


async def load_project(message: types.Message, state: FSMContext):
    """Запоминаем название проекта."""
    async with state.proxy() as data:
        if message.text == '/cancel_client':
            await cancel_add_new_task(message, state)
        else:
            data['project'] = message.text
            await FSMNewTask.next()
            await message.reply(
                'Укажите действия, которые вы совершали и место где были совершены действия ' +
                '(пример: ввод данных по адресу api/health/measure/; ' +
                'просмотр графика на сайте dev.band на странице Обзор->Ключевые показатели и т.д.).)',
            )


async def load_action(message: types.Message, state: FSMContext):
    """Запоминаем действия которые были совершены."""
    async with state.proxy() as data:
        if message.text == '/cancel_client':
            await cancel_add_new_task(message, state)
        else:
            data['action'] = message.text
            await FSMNewTask.next()
            await message.reply(
                'Укажите поведение, которые вы ожидали увиделить или получить ' +
                '(пример: при вводе данных ожидалось создание замера; ' +
                'ожидалось получить столбчатую диаграмму с данными о замерах за месяц и т.д.).)',
            )


async def load_purpose(message: types.Message, state: FSMContext):
    """Запоминаем результат, который ожидали получить."""
    async with state.proxy() as data:
        if message.text == '/cancel_client':
            await cancel_add_new_task(message, state)
        else:
            data['purpose'] = message.text
            await FSMNewTask.next()
            await message.reply(
                'Укажите поведение, которое было реально получено (пример: ' +
                'при вводе данных сервер возвращает 500 ошибку; ' +
                'данные в диаграмме отображюся за месяц, а не неделю и т.д.).)',
            )


async def load_real(message: types.Message, state: FSMContext):
    """Запоминаем результат, который реально был получен."""
    async with state.proxy() as data:
        if message.text == '/cancel_client':
            await cancel_add_new_task(message, state)
        else:
            data['real'] = message.text
            await FSMNewTask.next()
            await message.reply(
                'Укажите контактные данные лица, к которому можно обратиться ' +
                'за помощью или разъяснением (пример: Саша бэк, @bloodandhodor и т.д.).',
                reply_markup=client_buttons_with_skip,
            )


async def load_consultation(message: types.Message, state: FSMContext):
    """Запоминаем данные лица, у которого можно получить консультацию."""
    async with state.proxy() as data:
        if message.text == '/cancel_client':
            await cancel_add_new_task(message, state)
        elif message.text == '/skip_client':
            await FSMNewTask.next()
        else:
            data['consultation'] = message.text
            await FSMNewTask.next()
        await message.reply(
            'При необходимости укажите кому адресана данная задача. ' +
            '(пример: Саша бэк, @bloodandhodor и т.д.).',
        )


async def load_responsible(message: types.Message, state: FSMContext):
    """Запоминаем данные лица, которому ставится задача."""
    async with state.proxy() as data:
        if message.text == '/cancel_client':
            await cancel_add_new_task(message, state)
        elif message.text == '/skip_client':
            await FSMNewTask.next()
        else:
            data['responsible'] = message.text
            await FSMNewTask.next()
        await message.reply(
            'При необходимости укажите версию устройств, на которых была обнаружена ошибка ' +
            'или версию системы (build), в которой обнаружен баг (пример: ios билд 1.4.44, ' +
            'устроства тетирования: Iphone 12 Pro Max, Iphone 7'
        )


async def load_fixtures(message: types.Message, state: FSMContext):
    """Запоминаем данные о приспособлениях, задействованных в ходе обнаружения ошибки."""
    async with state.proxy() as data:
        if message.text == '/cancel_client':
            await cancel_add_new_task(message, state)
        elif message.text == '/skip_client':
            await FSMNewTask.next()
        else:
            data['fixtures'] = message.text
            await FSMNewTask.next()
        await message.reply(
            'При необходимости загрузите фотографию или документ (досупна загрузка одного файла).',
        )


async def load_file(message: types.Message, state: FSMContext):
    """Запоминаем загруженную фотографию или документ и сохраняем все в БД."""
    async with state.proxy() as data:
        if message.__getattribute__('text'):
            if message.text == '/cancel_client':
                await cancel_add_new_task(message, state)
            elif message.text == '/skip_client':
                flag = True
            else:
                await message.reply(
                    'Загрузите фотографию, документ или пропустите этап.',
                )
                flag = False
        elif message.__getattribute__('photo'):
            data['file'] = message.photo[0].file_id
            data['type'] = 'photo'
            flag = True
        elif message.__getattribute__('document'):
            data['file'] = message.document.file_id
            data['type'] = 'document'
            flag = True
    if flag:
        await add_new_task_in_db(state)
        await state.finish()
        if data['index_pm'] != '777':
            await message.reply(
                'Ваша задача поступила на рассмотрение к ПМ. '
                'Ждите результатов рассмотрения.',
                reply_markup=client_buttons,
            )


async def cancel_add_new_task(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Вы отменили действие.', reply_markup=client_buttons)


def register_handlers_client_task(dp: Dispatcher):
    """Регистрация обработчиков"""
    dp.register_message_handler(start_add_new_task, commands='new_task', state=None)
    dp.register_callback_query_handler(pm_call, state=FSMNewTask.pm)
    dp.register_message_handler(load_project, state=FSMNewTask.project)
    dp.register_message_handler(load_action, state=FSMNewTask.action)
    dp.register_message_handler(load_purpose, state=FSMNewTask.purpose)
    dp.register_message_handler(load_real, state=FSMNewTask.real)
    dp.register_message_handler(load_consultation, state=FSMNewTask.consultation)
    dp.register_message_handler(load_responsible, state=FSMNewTask.responsible)
    dp.register_message_handler(load_fixtures, state=FSMNewTask.fixtures)
    dp.register_message_handler(
        load_file,
        content_types=['photo', 'text', 'document'],
        state=FSMNewTask.file,
    )
    dp.register_message_handler(cancel_add_new_task, state="*", commands='cancel')
    dp.register_message_handler(
        cancel_add_new_task,
        Text(equals='cancel', ignore_case=True),
        state="*",
    )
