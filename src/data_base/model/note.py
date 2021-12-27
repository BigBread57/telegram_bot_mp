import sqlalchemy as sa

from src.data_base.base import Base, engine
from src.data_base.model.task import Task


class Note(Base):
    """Комментарий, заметка к задаче"""
    __tablename__ = 'note'

    id = sa.Column('note_id', sa.Integer, primary_key=True)
    task_id = sa.Column(sa.Integer, sa.ForeignKey(Task.id), nullable=False)
    text = sa.Column(sa.String(200), nullable=False)


Base.metadata.create_all(engine)
