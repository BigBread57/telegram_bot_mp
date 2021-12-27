import sqlalchemy as sa

from src.data_base.base import Base, engine


class Pm(Base):
    """инфомрация о PM."""
    __tablename__ = 'pm'

    id = sa.Column('pm_id', sa.Integer, primary_key=True)
    username = sa.Column(sa.String(50), nullable=False)
    user_id = sa.Column(sa.Integer, nullable=False)
    index = sa.Column(sa.Integer, nullable=False, unique=True)


Base.metadata.create_all(engine)
