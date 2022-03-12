from src.data_base import current_session
from src.data_base.model.task_in_jira import JiraUrl
from src.data_base.request_for_db.utils import get_chat_id_and_status_user


async def add_url_jira_in_db(state):
    """Функция на добавление url в Jira в БД."""
    async with state.proxy() as data:
        new_url_jira = JiraUrl(
            task_id=data.get('task_id'),
            url=data.get('url'),
            comment=data.get('comment'),
        )
        current_session.add(new_url_jira)
        current_session.commit()

    await get_chat_id_and_status_user(data.get('task_id'))


async def update_url_jira_in_db(state):
    """Функция на обновление url в Jira в БД."""
    async with state.proxy() as data:
        jira_url = current_session.query(JiraUrl).filter_by(task_id=data.get('task_id')).first()
        jira_url.url = data.get('url')
        jira_url.comment = data.get('comment')
        current_session.commit()

    await get_chat_id_and_status_user(data.get('task_id'))
