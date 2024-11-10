import uvicorn
from fastapi import FastAPI

from src.app.MovieController import movie_router
from src.app.UserController import user_router


def run_app():
    app = FastAPI(title="Popcorn Critic", description="Le réseau social pour les cinéphiles")

    app.include_router(user_router)

    app.include_router(movie_router)

    uvicorn.run(app, port=8000, host="localhost")
