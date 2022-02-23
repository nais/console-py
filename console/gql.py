from typing import Optional

import strawberry
from fastapi import Depends
from strawberry.fastapi import GraphQLRouter
from strawberry.types import Info

from console.api.deps import get_db
from console.database import models


async def get_context(db=Depends(get_db)):
    return {"db": db}


class MappingHelper:
    @classmethod
    def fields(cls):
        return {f.name for f in cls._type_definition.fields}


def convert(instance, cls):
    target_fields = cls.fields()
    source_fields = instance.fields()
    data = {
        k: getattr(instance, k)
        for k in source_fields
        if k in target_fields
        and not (getattr(instance, k) is None and issubclass(cls, models.Common))
    }
    return cls(**data)


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello World"


@strawberry.input
class TeamInput(MappingHelper):
    slug: str
    name: str


@strawberry.type
class TeamOutput(MappingHelper):
    slug: str
    name: str
    purpose: Optional[str] = None


@strawberry.type(description="Mutate teams")
class TeamMutation:
    @strawberry.mutation(description="Create a team")
    def create_team(self, team: TeamInput, info: Info) -> TeamOutput:
        db = info.context["db"]
        db_team = convert(team, models.Team)
        db.add(db_team)
        db.commit()
        db.refresh(db_team)
        return convert(db_team, TeamOutput)


schema = strawberry.Schema(query=Query, mutation=TeamMutation)

graphql_app = GraphQLRouter(schema, context_getter=get_context)
