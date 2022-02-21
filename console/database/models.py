import datetime
import uuid

from sqlalchemy import Column, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_mixin, declared_attr

from . import Base


@declarative_mixin
class Common:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + "s"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now)
    deleted_at = Column(DateTime)


class Team(Common, Base):
    slug = Column(Text, unique=True, nullable=False)
    name = Column(Text, unique=True, nullable=False)
    purpose = Column(Text)
