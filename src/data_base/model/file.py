import sqlalchemy as sa

from src.data_base.base import Base, engine
from src.data_base.model.task import Task


class File(Base):
    """Файлы, прикрепелнные к задаче."""
    __tablename__ = 'file'

    id = sa.Column('file_id', sa.Integer, primary_key=True)
    task_id = sa.Column(sa.Integer, sa.ForeignKey(Task.id), nullable=False)
    file = sa.Column(sa.String(200), nullable=False)
    type = sa.Column(sa.String(20), nullable=False)


Base.metadata.create_all(engine)
