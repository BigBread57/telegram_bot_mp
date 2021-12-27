import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType

from src.data_base.base import Base, engine


class BotChoiceType(ChoiceType):
    cache_ok = True


STATUS = [
        (u'created', u'☑ Создана ☑️'),
        (u'denied', u'❌ Отклонена ❌'),
        (u'discussion', u'💬 Обсуждение 💬'),
        (u'accepted', u'✅ Принята ✅'),
    ]


class Task(Base):
    """Задача пользователя."""
    __tablename__ = 'task'

    id = sa.Column('task_id', sa.Integer, primary_key=True)
    index_pm = sa.Column(sa.Integer, nullable=False)
    author = sa.Column(sa.String(200), nullable=False)
    author_id = sa.Column(sa.Integer, nullable=False)
    project = sa.Column(sa.String(200), nullable=False)
    purpose = sa.Column(sa.Text, nullable=False)
    action = sa.Column(sa.Text, nullable=False)
    real = sa.Column(sa.Text, nullable=False)
    consultation = sa.Column(sa.String(200), nullable=True, default='Нет данных')
    responsible = sa.Column(sa.String(200), nullable=True, default='Нет данных')
    fixtures = sa.Column(sa.String(200), nullable=True, default='Нет данных')
    status = sa.Column(
        BotChoiceType(STATUS),
        nullable=False,
        default='created',
    )
    files = relationship(
        'File',
        backref='task',
        cascade='all, delete,'
    )
    notes = relationship(
        'Note',
        uselist=False,
        backref='task',
        cascade='all, delete,'
    )
    jira_urls = relationship(
        'JiraUrl',
        uselist=False,
        backref='task',
        cascade='all, delete,'
    )


Base.metadata.create_all(engine)
