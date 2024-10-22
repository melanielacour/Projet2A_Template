from datetime import datetime

import requests
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
TMDB_ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3YTM1YmQwMDE2Mzk5MDNmNWM4MzBlODhkZDg2ZWQzMCIsIm5iZiI6MTcyOTU4MTc0MS41Nzg2NTEsInN1YiI6IjY2ZTQ0NmI5OTAxM2ZlODcyMjI0MTc1MiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.UvX882tvk0XKaN5mrivSQzXfzzXEOAqSX_4nzSfscFY"


# Modèle Pydantic pour la classe Film
class Film(BaseModel):
    id_film: int
    id_tmdb: int
    title: str
    producer: str
    category: str
    date: datetime
    average_rate: float = 0.0
    ratings: list[int] = []


@app.get("/movies", response_model=list[Film])
async def get_movies():
    url = "https://api.themoviedb.org/3/movie/popular?language=fr-FR&page=1"
    headers = {
        "Authorization": f"Bearer {TMDB_ACCESS_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        results = response.json()["results"]
        films = []
        for movie in results:
            # Assurez-vous de faire correspondre les champs de l'API avec ceux de votre classe Film
            film = Film(
                id_film=0,  # À remplacer par une logique pour obtenir un ID unique si nécessaire
                id_tmdb=movie["id"],
                title=movie["title"],
                producer="N/A",
                category="N/A",
                date=datetime.strptime(movie["release_date"], "%Y-%m-%d"),
                average_rate=0.0,
                ratings=[]
            )
            films.append(film)
        return films
    else:
        return {"error": f"Erreur lors de la récupération des films. Statut : {response.status_code}"}
