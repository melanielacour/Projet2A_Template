import os
from datetime import datetime
from typing import List

import requests
import uvicorn
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

from src.Service import FilmService, UserService
from src.Service.MovieService import MovieService

load_dotenv()

app = FastAPI()
TMDB_API_KEY = os.getenv("eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3YTM1YmQwMDE2Mzk5MDNmNWM4MzBlODhkZDg2ZWQzMCIsIm5iZiI6MTcyNjgxOTk4Mi42NzA1NDQsInN1YiI6IjY2ZTQ0NmI5OTAxM2ZlODcyMjI0MTc1MiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.mUjUWmMcf2k7lyf4V7sJTn3X8eDGgYSpYDrhKippftg")
TMDB_BASE_URL = "https://api.themoviedb.org/3"


class Movie(BaseModel):
    title: str
    release_date: str
    producer: str
    category: str


### trouver un film par titre
@app.get("/movies/title/{title}", response_model=list[Film])
async def get_movie_by_title(title: str):
    url = f"{TMDB_BASE_URL}/search/movie?api_key={TMDB_API_KEY}&query={title}"
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200 or not data.get("results"):
        raise HTTPException(status_code=404, detail="Movie not found")

    movies = []
    for movie in data["results"]:
        # Création d'une instance de Film
        film = Film(
            id_film=0,  ###???????
            id_tmdb=movie['id'],
            title=movie['title'],
            producer=get_producer(movie['id']),
            category=get_categorys(movie['id']),
            date=datetime.strptime(movie['release_date'], '%Y-%m-%d')
        )
        movies.append(film)

    return movies


# trouver un film par catégorie
@app.get("/movies/category/{category_id}", response_model=list[Movie])
async def get_movies_by_category(category_id: int):
    url = f"{TMDB_BASE_URL}/discover/movie?api_key={TMDB_API_KEY}&with_categorys={category_id}"
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200 or not data.get("results"):
        raise HTTPException(status_code=404, detail="No movies found for this category")

    movies = [
        Movie(
            title=movie['title'],
            date=movie['release_date'],
            producer=get_producer(movie['id']),
            category=get_categorys(movie['id'])
        )
        for movie in data["results"]
    ]
    return movies


@app.get("/movies/producer/{producer_name}", response_model=list[Movie])
async def get_movies_by_producer(producer_name: str):
    url = f"{TMDB_BASE_URL}/discover/movie?api_key={TMDB_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200 or not data.get("results"):
        raise HTTPException(status_code=404, detail="No movies found")

    movies = []
    for movie in data["results"]:
        # Récupérer les crédits du film
        credits_url = f"{TMDB_BASE_URL}/movie/{movie['id']}/credits?api_key={TMDB_API_KEY}"
        credits_response = requests.get(credits_url)
        credits_data = credits_response.json()

        if credits_response.status_code == 200:
            for member in credits_data.get('crew', []):
                if member['job'] == 'Producer' and member['name'] == producer_name:
                    movies.append(
                        Movie(
                            title=movie['title'],
                            release_date=movie['release_date'],
                            director=get_director(movie['id']),
                            category=get_categorys(movie['id'])
                        )
                    )
                    break  # Si un producteur correspondant est trouvé, passe au film suivant

    if not movies:
        raise HTTPException(status_code=404, detail="No movies found for this producer")

    return movies


@app.get("/movies/date/{date}", response_model=list[Movie])
async def get_movies_by_date(date: str):
    url = f"{TMDB_BASE_URL}/discover/movie?api_key={TMDB_API_KEY}&primary_release_year={date}"
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200 or not data.get("results"):
        raise HTTPException(status_code=404, detail="No movies found for this date")

    movies = [
        Movie(
            title=movie['title'],
            release_date=movie['release_date'],
            producer=get_producer(movie['id']),
            category=get_categorys(movie['id'])
        )
        for movie in data["results"]
    ]
    return movies


def get_producer(movie_id: int) -> str:
    url = f"{TMDB_BASE_URL}/movie/{movie_id}/credits?api_key={TMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for crew_member in data.get('crew', []):
            if crew_member['job'] == 'producer':
                return crew_member['name']
    return "Unknown"


def get_categorys(movie_id: int) -> str:
    url = f"{TMDB_BASE_URL}/movie/{movie_id}?api_key={TMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        categorys = [category['name'] for category in data.get('categorys', [])]
        return ", ".join(categorys)
    return "Unknown"


def get_producer_id(producer_name: str) -> int:
    url = f"{TMDB_BASE_URL}/search/person?api_key={TMDB_API_KEY}&query={producer_name}"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200 and data.get("results"):
        return data['results'][0]['id']
    return None


# Lancement de l'application sur le le port 8XXX avec XXX les 3 derniers numéros de votre id
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
