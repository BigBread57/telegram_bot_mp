import sqlalchemy as sa

from src.data_base.base import Base, engine
from src.data_base.model.task import Task


class JiraUrl(Base):
    """Данные о задаче в Jira"""
    __tablename__ = 'jira'

    id = sa.Column('jira_id', sa.Integer, primary_key=True)
    task_id = sa.Column(sa.Integer, sa.ForeignKey(Task.id), nullable=False)
    url = sa.Column(sa.String(100), nullable=False)
    note = sa.Column(sa.String(200), nullable=True)


Base.metadata.create_all(engine)
