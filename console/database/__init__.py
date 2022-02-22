from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from console.settings import Settings

SessionLocal = None

Base = declarative_base()


def init(settings: Settings):
    dsn = settings.pg_dsn.replace("postgres:", "postgresql:", 1)
    engine = create_engine(dsn)

    from . import models # NOQA
    Base.metadata.create_all(bind=engine)

    global SessionLocal
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
