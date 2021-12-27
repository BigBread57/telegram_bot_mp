from src.data_base.model.task import Task
from src.data_base.request_for_db.utils import division_message, qs, is_pm


async def filter_task(message, status):
    """Функция на фильтрацию задач."""
    status_user = await is_pm(message)
    tasks = await qs()
    if status == 'all' and status_user == 'pm':
        tasks = tasks.order_by(Task.id.desc()).limit(10).all()
    elif status == 'all' and status_user != 'pm':
        tasks = tasks.filter(Task.author_id == message.from_user.id)
        tasks = tasks.order_by(Task.id.desc()).limit(10).all()
    elif status != 'all' and status_user == 'pm':
        tasks = tasks.order_by(Task.id.desc()).filter(Task.status == status).limit(10).all()
    elif status != 'all' and status_user != 'pm':
        tasks = tasks.filter(Task.author_id == message.from_user.id)
        tasks = tasks.order_by(Task.id.desc()).filter(Task.status == status).limit(10).all()

    await division_message(message=message, tasks=tasks, status=status, pm=None, client=None)
