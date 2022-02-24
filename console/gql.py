import uuid
from typing import Optional, Set, Type

import strawberry
from fastapi import Depends
from strawberry.fastapi import GraphQLRouter
from strawberry.types import Info

from console import crud
from console.api.deps import get_db
from console.crud.base import NOTSET
from console.database import models


async def get_context(db=Depends(get_db)):
    return {"db": db}


class MappingHelper:
    @classmethod
    def fields(cls) -> Set[str]:
        return {f.name for f in cls._type_definition.fields}


def convert(db_obj: models.Base, cls: Type[MappingHelper]) -> MappingHelper:
    target_fields = cls.fields()
    source_fields = db_obj.fields()
    fields = target_fields & source_fields
    data = {field: getattr(db_obj, field) for field in fields}
    return cls(**data)


@strawberry.input
class TeamInput(MappingHelper):
    slug: str
    name: str
    purpose: Optional[str] = NOTSET


@strawberry.type
class TeamOutput(MappingHelper):
    slug: str
    name: str
    purpose: Optional[str]


@strawberry.type
class Query:
    @strawberry.field
    def get_team(self, id: uuid.UUID, info: Info) -> TeamOutput:
        db = info.context["db"]
        db_team = crud.team.get(db, id)
        return convert(db_team, TeamOutput)


@strawberry.type(description="Mutate teams")
class TeamMutation:
    @strawberry.mutation(description="Create a team")
    def create_team(self, team: TeamInput, info: Info) -> TeamOutput:
        db = info.context["db"]
        db_team = crud.team.create(db, obj_in=team)
        return convert(db_team, TeamOutput)

    @strawberry.mutation(description="Update a team")
    def update_team(self, id: uuid.UUID, team: TeamInput, info: Info) -> TeamOutput:
        db = info.context["db"]
        db_team = crud.team.get(db, id)
        if db_team is None:
            # TODO: Do error handling
            return None
        db_team = crud.team.update(db, db_obj=db_team, obj_in=team)
        return convert(db_team, TeamOutput)


schema = strawberry.Schema(query=Query, mutation=TeamMutation)
graphql_app = GraphQLRouter(schema, context_getter=get_context)
