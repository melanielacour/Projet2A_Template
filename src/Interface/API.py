import time
from datetime import datetime

import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.Service.MovieService import MovieService

app = FastAPI()
service = MovieService()

# modèle Pydantic pour les films


class Film(BaseModel):
    id_film: int
    id_tmdb: int
    title: str
    producer: str
    category: str
    date: str
    average_rate: float = 0.0
    ratings: list[int] = []


@app.get("/movies", response_model=list[Film])
async def get_movies():
    return service.get_random_movies()


@app.get("/movies/title/{title}", response_model=Film)
async def get_movie_by_title(title: str):
    film = service.get_movie_by_title(title)
    if not film:
        raise HTTPException(status_code=404, detail="Film non trouvé")
    return film


@app.get("/movies/category/{category_name}", response_model=list[Film])
async def get_movies_by_category(category_name: str):
    category_id = service.get_category_id(category_name)
    if category_id is None:
        raise HTTPException(status_code=404, detail="Catégorie non trouvée.")

    films = service.get_movies_by_category(category_id)
    return films


@app.get("/movies/director/{director_name}", response_model=list[Film])
async def get_movies_by_director(director_name: str):
    films = service.get_movies_by_director_name(director_name)
    if not films:
        raise HTTPException(status_code=404, detail="Aucun film trouvé pour ce réalisateur.")
    return films
