from src.data_base import current_session
from src.data_base.model.note import Note
from src.data_base.request_for_db.utils import get_chat_id_and_status_user


async def add_note_in_db(state):
    """Функция на добавление заметки к задаче в БД."""
    async with state.proxy() as data:
        new_note = Note(
            task_id=data.get('task_id'),
            text=data.get('text'),
        )
        current_session.add(new_note)
        current_session.commit()

    await get_chat_id_and_status_user(data.get('task_id'))


async def update_note_in_db(state):
    """Функция на обновление note в БД."""
    async with state.proxy() as data:
        note = current_session.query(Note).filter_by(task_id=data.get('task_id')).first()
        note.text = data.get('text')
        current_session.commit()

    await get_chat_id_and_status_user(data.get('task_id'))
