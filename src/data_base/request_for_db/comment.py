from src.data_base import current_session
from src.data_base.model.comment import Comment
from src.data_base.request_for_db.utils import get_chat_id_and_status_user


async def add_comment_in_db(state):
    """Функция на добавление заметки к задаче в БД."""
    async with state.proxy() as data:
        new_comment = Comment(
            task_id=data.get('task_id'),
            text=data.get('text'),
        )
        current_session.add(new_comment)
        current_session.commit()

    await get_chat_id_and_status_user(data.get('task_id'))


async def update_comment_in_db(state):
    """Функция на обновление comment в БД."""
    async with state.proxy() as data:
        comment = current_session.query(Comment).filter_by(task_id=data.get('task_id')).first()
        comment.text = data.get('text')
        current_session.commit()

    await get_chat_id_and_status_user(data.get('task_id'))
