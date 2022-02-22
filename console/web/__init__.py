from fastapi import FastAPI

from console.web import teams

app = FastAPI()

app.include_router(teams.router)


@app.get("/hello")
def hello():
    return {"message": "Hello World"}
