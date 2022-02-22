import datetime
import uuid

from sqlalchemy import Column, DateTime, Text, Table, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_mixin, declared_attr, relationship

from . import Base


@declarative_mixin
class Common:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + "s"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.datetime.now)

    @declared_attr
    def created_by_id(cls):
        return Column(UUID, ForeignKey("users.id"))

    @declared_attr
    def created_by(cls):
        return relationship("User")

    updated_at = Column(DateTime, onupdate=datetime.datetime.now)

    @declared_attr
    def updated_by_id(cls):
        return Column(UUID, ForeignKey("users.id"))

    @declared_attr
    def updated_by(cls):
        return relationship("User")

    deleted_at = Column(DateTime)

    @declared_attr
    def deleted_by_id(cls):
        return Column(UUID, ForeignKey("users.id"))

    @declared_attr
    def deleted_by(cls):
        return relationship("User")


user_team = Table(
    'association', Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('team_id', ForeignKey('teams.id'), primary_key=True)
)


class Team(Common, Base):
    slug = Column(Text, unique=True, nullable=False)
    name = Column(Text, unique=True, nullable=False)
    purpose = Column(Text)
    users = relationship("User", secondary=user_team, back_populates="teams")


class User(Common, Base):
    email = Column(Text, unique=True)
    name = Column(Text, nullable=False)
    teams = relationship("Team", secondary=user_team, back_populates="users")
