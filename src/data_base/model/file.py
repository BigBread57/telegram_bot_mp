import sqlalchemy as sa

from src.data_base.q import Base


class File(Base):
    """Файлы, прикрепленные к задаче."""
    __tablename__ = 'file'

    id = sa.Column(sa.Integer, primary_key=True)
    task_id = sa.Column(sa.Integer, sa.ForeignKey('task.id'), nullable=False)
    file = sa.Column(sa.String(200), nullable=False)
    type = sa.Column(sa.String(20), nullable=False)
