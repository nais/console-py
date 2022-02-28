import os

import functools
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from console.core.config import settings

Base = declarative_base()


@functools.cache
def init():
    engine = create_engine(settings.database_url)

    run_migrations()

    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    session_maker = init()
    return session_maker()


def run_migrations():
    up = os.path.dirname
    project_root = up(up(up(os.path.realpath(__file__))))
    alembic_cfg = Config(os.path.join(project_root, "alembic.ini"))
    alembic_cfg.set_main_option(
        "script_location", os.path.join(project_root, "alembic")
    )
    command.upgrade(alembic_cfg, "head")
