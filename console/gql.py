import strawberry
from fastapi import Depends
from strawberry.fastapi import GraphQLRouter
from strawberry.types import Info

from console.api.deps import get_db
from console.api import schemas
from console.database import models


async def get_context(db=Depends(get_db)):
    return {"db": db}


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello World"


@strawberry.experimental.pydantic.input(model=schemas.Team)
class TeamInput:
    slug: strawberry.auto
    name: strawberry.auto
    purpose: strawberry.auto = None


@strawberry.experimental.pydantic.type(model=schemas.Team)
class TeamOutput:
    slug: strawberry.auto
    name: strawberry.auto
    purpose: strawberry.auto = None


@strawberry.type(description="Mutate teams")
class TeamMutation:
    @strawberry.mutation(description="Create a team")
    def create_team(self, team: TeamInput, info: Info) -> TeamOutput:
        pd_team = team.to_pydantic()
        db = info.context["db"]
        db_team = models.Team(**pd_team.dict())
        db.add(db_team)
        db.commit()
        db.refresh(db_team)
        return TeamOutput.from_pydantic(db_team)


schema = strawberry.Schema(query=Query, mutation=TeamMutation)

graphql_app = GraphQLRouter(schema, context_getter=get_context)
