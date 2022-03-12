"""Схема БД отвечает за процессы, связанные с задачами для Jira."""
import sqlalchemy as sa
from sqlalchemy.orm import relationship

from src.data_base.q import Base
from src.data_base.model.enums import BotChoiceType, STATUS


class Task(Base):
    """Задача пользователя."""
    __tablename__ = 'task'

    id = sa.Column(sa.Integer, primary_key=True)
    user = sa.Column(sa.Integer, sa.ForeignKey('user.id'), nullable=False)  # ссылка на контролирующее лицо
    author_username = sa.Column(sa.String(200), nullable=False)
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
        cascade='all, delete,',
    )
    comments = relationship(
        'Comment',
        backref='task',
        cascade='all, delete',
    )
    jira_urls = relationship(
        'JiraUrl',
        uselist=False,
        backref='task',
        cascade='all, delete',
    )


class Comment(Base):
    """Комментарий, заметка к задаче."""
    __tablename__ = 'comment'

    id = sa.Column(sa.Integer, primary_key=True)
    task_id = sa.Column(sa.Integer, sa.ForeignKey('task.id'), nullable=False)
    text = sa.Column(sa.String(200), nullable=False)


class JiraSettings(Base):
    """Данные для входа в Jira."""
    __tablename__ = 'jira_settings'

    id = sa.Column(sa.Integer, primary_key=True)
    author_id = sa.Column(sa.Integer, nullable=False)
    username_jira = sa.Column(sa.String(100), nullable=False)
    password_jira = sa.Column(sa.String(100), nullable=False)


class JiraUrl(Base):
    """Данные о задаче в Jira."""
    __tablename__ = 'jira_url'

    id = sa.Column(sa.Integer, primary_key=True)
    task_id = sa.Column(sa.Integer, sa.ForeignKey('task.id'), nullable=False)
    url = sa.Column(sa.String(100), nullable=False)
    comment = sa.Column(sa.String(200), nullable=True)
