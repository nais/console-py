from fastapi import FastAPI

from console.api import teams

app = FastAPI()

app.include_router(teams.router)


@app.get("/hello")
def hello():
    return {"message": "Hello World"}
