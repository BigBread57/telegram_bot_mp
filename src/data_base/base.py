import typing

from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.util.compat import contextmanager

from src.settings.common import DATABASES


engine = create_engine(URL.create(**DATABASES))
metadata = MetaData(bind=engine)
Session = sessionmaker()
current_session = scoped_session(Session)


@as_declarative(metadata=metadata)
class Base:
    pass


@contextmanager
def session(**kwargs) -> typing.ContextManager[Session]:
    """Provide a transactional scope."""
    new_session = Session(**kwargs)
    try:
        yield new_session
        new_session.commit()
    except Exception:
        new_session.rollback()
        raise
    finally:
        new_session.close()
