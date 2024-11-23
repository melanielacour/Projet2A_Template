from typing import List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.Service.MovieService import MovieService


class Film(BaseModel):
    id_film: int
    id_tmdb: int
    title: str
    producer: str
    category: str
    date: str


# Instanciation du service (assurez-vous d'avoir un service approprié)
service = MovieService()

# Définition du routeur pour les films avec le préfixe et les tags
movie_router = APIRouter(prefix="/movies", tags=["Movies"])


@movie_router.get("/title/{title}", response_model=List[Film])
async def get_movies_by_title(title: str):
    films = service.get_movie_by_title(title)
    if not films:
        raise HTTPException(status_code=404, detail="Aucun film trouvé")
    return films


@movie_router.get("/{id}", response_model=Film)
async def get_movie_by_id(id: str):
    film = service.get_movie_by_id(id)
    if not film:
        raise HTTPException(status_code=404, detail="Film non trouvé")
    return film


@movie_router.get("/category/{category_name}", response_model=List[Film])
async def get_movies_by_category(category_name: str):
    category_id = service.get_category_id(category_name)
    if category_id is None:
        raise HTTPException(status_code=404, detail="Catégorie non trouvée.")

    films = service.get_movies_by_category(category_id)
    return films


@movie_router.get("/director/{director_name}", response_model=List[Film])
async def get_movies_by_director(director_name: str):
    films = service.get_movies_by_director_name(director_name)
    if not films:
        raise HTTPException(
            status_code=404, detail="Aucun film trouvé pour ce réalisateur."
        )
    return films


@movie_router.get("/synopsis/synposis_by_title}")
async def get_movies_synopsis(title: str):
    try:
        return service.get_synopsis_by_title(title)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
