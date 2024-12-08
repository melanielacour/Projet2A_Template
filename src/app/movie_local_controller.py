from pydantic import BaseModel
from src.app.init_app import movie_repo
from fastapi import APIRouter, HTTPException

movielocal_router = APIRouter(
    prefix="/movielocal", tags=["Popcorn Critic's movies"]
    )


# Déclaration du modèle de réponse pour un film
class MovieSimple(BaseModel):
    id_local: int
    id_tmdb: int
    title: str


# Création d'une instance de MovieRepo


@movielocal_router.get(
    "/movies/tmdb_id/{id_tmdb}",
    response_model=MovieSimple,
    summary="Get movies available on Popcorn Critic",
)
async def get_movie_by_tmdb_id(id_tmdb: int):
    movie = movie_repo.get_movie_by_tmdb_id(id_tmdb)
    if not movie:
        raise HTTPException(status_code=404, detail="Film non trouvé")
    return movie
