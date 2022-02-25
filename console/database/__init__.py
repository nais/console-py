from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from console.core.config import settings

Base = declarative_base()


def init():
    dsn = settings.database_url.replace("postgres:", "postgresql:", 1)
    engine = create_engine(dsn)

    from . import models  # NOQA

    Base.metadata.create_all(bind=engine)

    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


SessionLocal = init()
