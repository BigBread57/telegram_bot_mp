"""Схема БД отвечает за информацию о пользователе и окружении."""
import sqlalchemy as sa
from sqlalchemy.orm import relationship


from src.data_base.model.enums import BotChoiceType, ROLE
from src.data_base.q import Base

association_table = sa.Table(
    'users_in_environment',
    Base.metadata,
    sa.Column('user_id', sa.ForeignKey('user.id'), primary_key=True),
    sa.Column('environment_id', sa.ForeignKey('environment.id'), primary_key=True)
)


class User(Base):
    """Информация о пользователе."""
    __tablename__ = 'user'

    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, nullable=False)
    role = sa.Column(BotChoiceType(ROLE), default='other')
    task = relationship('Task', backref='user')  # указатель на контролирующее лицо
    environment = relationship('Environment', secondary=association_table, backref='user')


class Environment(Base):
    """Информация об окружении."""
    __tablename__ = 'environment'

    id = sa.Column(sa.Integer, primary_key=True)
    author = sa.Column(sa.Integer, nullable=False)
    access_code = sa.Column(sa.String(200), nullable=False, unique=True)
    users = relationship('User', secondary=association_table, backref='environment')
