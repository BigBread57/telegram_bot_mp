from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from src.buttons.pm_buttons import pm_buttons, pm_buttons_with_skip, pm_buttons_without_skip
from src.data_base.request_for_db.url_jira import add_url_jira_in_db, update_url_jira_in_db
from src.data_base.request_for_db.utils import definition_task_id, change_url_jira_for_task


class FSMNewUrl(StatesGroup):
    """Класс конечных автоматов для jira."""
    url = State()
    note = State()


async def start_add_new_url_jira(callback: types.CallbackQuery):
    """Начинаем создание ссылки на jira, и даем право ввести url."""
    task = await definition_task_id(callback)

    await FSMNewUrl.url.set()
    state = Dispatcher.get_current().current_state()
    await state.update_data(task_id=task.id)

    if await change_url_jira_for_task(task.id):
        await callback.message.reply(
            'Вставьте ссылку на задачу в Jira.',
            reply_markup=pm_buttons_without_skip,
        )
        await state.update_data(flag='new')
    else:
        await callback.message.reply(
            'Данная задача уже зафиксирована, вы не можете добавить еще один url, ' +
            'но можете его отредактировть',
            reply_markup=pm_buttons_without_skip,
        )
        await state.update_data(flag='update')


async def load_url(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == '/cancel_pm':
            await cancel_add_new_url_jira(message, state)
        else:
            data['url'] = message.text
            await FSMNewUrl.next()
            await message.reply(
                'Укажите комментарий или заметку для пользователя ' +
                'При пропуске будет стоять следующий текст: ' +
                'Не забудьте оценить время работы над задачей, следите за статусом ее исполения, ' +
                'оставляйте комментарии в случае возникших трудностей или пишите своему ПМ',
                reply_markup=pm_buttons_with_skip,
            )


async def load_note(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == '/cancel_pm':
            await cancel_add_new_url_jira(message, state)
        elif message.text == '/skip_pm':
            data['note'] = (
                    'Не забудьте оценить время работы над задачей, ' +
                    'следите за статусом ее исполения, ' +
                    'оставляйте комментарии в случае возникших ' +
                    'трудностей или пишите своему ПМ'
            )
        else:
            data['note'] = message.text

    if data['flag'] == 'new':
        await add_url_jira_in_db(state)
    else:
        await update_url_jira_in_db(state)
    await state.finish()
    await message.reply(
        'Вы добавили ссылку на Jira. Отправитель задачи уведомлен об этом.',
        reply_markup=pm_buttons,
    )


async def cancel_add_new_url_jira(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Вы отменили действие.', reply_markup=pm_buttons)


def register_handlers_jira(dp: Dispatcher):
    """Регистрация обработчиков"""
    dp.register_callback_query_handler(start_add_new_url_jira, state=None)
    dp.register_message_handler(load_url, state=FSMNewUrl.url)
    dp.register_message_handler(load_note, state=FSMNewUrl.note)
    dp.register_message_handler(cancel_add_new_url_jira, state="*", commands='cancel_pm')
    dp.register_message_handler(
        cancel_add_new_url_jira,
        Text(equals='cancel', ignore_case=True),
        state="*",
    )

