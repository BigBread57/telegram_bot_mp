"""Схема БД отвечает за процессы с заметками пользователя."""
import datetime

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from src.data_base.q import Base


class Category(Base):
    """Категория заметки или ее тип."""
    __tablename__ = 'category'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(200), unique=True)
    author_id = sa.Column(sa.Integer, nullable=False)
    access_code = sa.Column(sa.String(200), nullable=True)
    notes = relationship(
        'Note',
        backref='category',
        cascade='all, delete'
    )


class Note(Base):
    """Заметка пользователя."""
    __tablename__ = 'note'

    id = sa.Column(sa.Integer, primary_key=True)
    description = sa.Column(sa.Text, nullable=False)
    keywords = sa.Column(sa.String(200), nullable=True)
    created_at = sa.Column(sa.DateTime, default=datetime.datetime.now())
    category_id = sa.Column(sa.Integer, sa.ForeignKey('category.id'), nullable=False)
