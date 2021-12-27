from src.data_base import current_session
from src.data_base.model.file import File
from src.data_base.model.pm import Pm
from src.data_base.model.task import Task
from src.data_base.request_for_db.utils import division_message, qs


async def add_new_task_in_db(state):
    """Функция на добавление задач в БД."""
    async with state.proxy() as data:
        if data.get('index_pm') == '777':
            index_pm = int(data.get('index_pm'))
            pm = int(data.get('author_id'))
        else:
            pm = current_session.query(Pm).filter_by(index=data.get('index_pm')).first()
            index_pm = pm.index
        new_task_client = Task(
            index_pm=index_pm,
            author=data.get('author'),
            author_id=data.get('author_id'),
            project=data.get('project'),
            purpose=data.get('purpose'),
            action=data.get('action'),
            real=data.get('real'),
            consultation=data.get('consultation'),
            responsible=data.get('responsible'),
            fixtures=data.get('fixtures'),
            status='created',
        )
        current_session.add(new_task_client)
        current_session.flush()

        if data.get('file'):
            new_file = File(
                task_id=new_task_client.id,
                file=data.get('file'),
                type=data.get('type'),
            )
            current_session.add(new_file)
        current_session.commit()

    tasks = await qs()
    tasks = tasks.filter(Task.id == new_task_client.id).all()

    await division_message(message=None, tasks=tasks, status=None, pm=pm, client=None)
