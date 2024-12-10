import uvicorn
from fastapi import FastAPI

from src.app.MovieController import movie_router
from src.app.UserController import user_router
from src.app.review_controller import review_router
from src.app.user_movie_controller import usermovie_router
from src.app.scout_controller import scout_router
from src.app.movie_local_controller import movielocal_router
from src.app.recommendation_controller import recommendation_router


def run_app():
    app = FastAPI(
        title="Popcorn Critic",
        description="Votre compagnon cinéphile ultime : explorez, critiquez et partagez vos avis sur vos films préférés en un clin d'œil !",
    )

    app.include_router(movie_router)

    app.include_router(movielocal_router)

    app.include_router(user_router)

    app.include_router(review_router)

    app.include_router(usermovie_router)

    app.include_router(scout_router)

    app.include_router(recommendation_router)

    uvicorn.run(app, port=8000, host="localhost")
