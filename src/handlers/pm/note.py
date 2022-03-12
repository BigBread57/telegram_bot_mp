from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from src.buttons.pm_buttons import pm_buttons, pm_buttons_without_skip
from src.data_base.request_for_db.comment import add_comment_in_db, update_comment_in_db
from src.data_base.request_for_db.utils import definition_task_id, change_comment_for_task


class FSMNewcomment(StatesGroup):
    """Класс конечных автоматов для comment."""
    text = State()


async def start_add_new_comment(callback: types.CallbackQuery):
    """Начинаем создание заметки для задачи, и даем право ввести текст."""
    task = await definition_task_id(callback)
    await FSMNewcomment.text.set()
    state = Dispatcher.get_current().current_state()
    await state.update_data(task_id=task.id)

    if await change_comment_for_task(task.id):
        await callback.message.reply(
            'Укажите текст заметки для задачи.',
            reply_markup=pm_buttons_without_skip,
        )
        await state.update_data(flag='new')
    else:
        await callback.message.reply(
            'У данной задачи уже есть замметка, вы не можете добавить еще одну, ' +
            'но можете её отредактировть',
            reply_markup=pm_buttons_without_skip,
        )
        await state.update_data(flag='update')


async def load_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == '/cancel_pm':
            await cancel_add_new_comment(message, state)
        else:
            data['text'] = message.text

    if data['flag'] == 'new':
        await add_comment_in_db(state)
    else:
        await update_comment_in_db(state)
    await state.finish()
    await message.reply(
        'Вы добавили заметку в задаче. Отправитель задачи уведомлен об этом.',
        reply_markup=pm_buttons,
    )


async def cancel_add_new_comment(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Вы отменили действие.', reply_markup=pm_buttons)


def register_handlers_comment(dp: Dispatcher):
    """Регистрация обработчиков"""
    dp.register_callback_query_handler(start_add_new_comment, state=None)
    dp.register_message_handler(load_text, state=FSMNewcomment.text)
    dp.register_message_handler(cancel_add_new_comment, state="*", commands='cancel_pm')
    dp.register_message_handler(
        cancel_add_new_comment,
        Text(equals='cancel', ignore_case=True),
        state="*",
    )

