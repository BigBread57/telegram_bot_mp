from src.data_base import current_session
from src.data_base.request_for_db.utils import definition_task_id


async def delete_task_in_db(callback):
    """Удаление объекта из БД."""
    task = await definition_task_id(callback)

    current_session.delete(task)
    current_session.commit()


async def change_status_in_db(callback, status):
    """Изменение статуса задачи."""
    task = await definition_task_id(callback)

    task.status = status
    current_session.commit()
