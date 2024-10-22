import time
from datetime import datetime

import requests
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
TMDB_ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3YTM1YmQwMDE2Mzk5MDNmNWM4MzBlODhkZDg2ZWQzMCIsIm5iZiI6MTcyOTU4MTc0MS41Nzg2NTEsInN1YiI6IjY2ZTQ0NmI5OTAxM2ZlODcyMjI0MTc1MiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.UvX882tvk0XKaN5mrivSQzXfzzXEOAqSX_4nzSfscFY"
TMDB_API_KEY = "7a35bd001639903f5c830e88dd86ed30"

# Modèle Pydantic pour la classe Film
class Film(BaseModel):
    id_film: int
    id_tmdb: int
    title: str
    producer: str
    category: str
    date: str
    average_rate: float = 0.0
    ratings: list[int] = []

########### tous les films ############ faire aléatoire 200
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


############## film par titre ##################
@app.get("/movies/title/{title}")
async def get_movie_by_title(title: str):
    # Rechercher le film
    search_url = f"https://api.themoviedb.org/3/search/movie?query={title}&language=fr-FR&page=1"
    headers = {
        "Authorization": f"Bearer {TMDB_ACCESS_TOKEN}"
    }
    search_response = requests.get(search_url, headers=headers)

    if search_response.status_code == 200:
        search_results = search_response.json()["results"]
        if search_results:
            film_data = search_results[0]  # on prend le premier film trouvé
            film_id = film_data["id"]  # obtenir l'Id du film

            details_url = f"https://api.themoviedb.org/3/movie/{film_id}?language=fr-FR"
            details_response = requests.get(details_url, headers=headers)

            if details_response.status_code == 200:
                details_data = details_response.json()
                film = Film(
                    id_film=details_data["id"],  # Utiliser l'Id TMDB comme Id du film
                    id_tmdb=details_data["id"],
                    title=details_data["title"],
                    producer=details_data.get("production_companies", [{"name": "Inconnu"}])[0].get("name", "Inconnu"),
                    category=details_data.get("genres", [{"name": "Inconnu"}])[0].get("name", "Inconnu"),
                    date=details_data["release_date"][:4]  # Extraire les 4 premiers caractères ( que l'année)
                )
                return film.__dict__
            else:
                return {"error": f"Erreur lors de la récupération des détails du film. Statut : {details_response.status_code}"}
        else:
            return {"message": "Aucun film trouvé."}
    else:
        return {"error": f"Erreur lors de la recherche des films. Statut : {search_response.status_code}"}



####### films par genre #########
def get_category_id(category_name: str) -> int:
    url = f"https://api.themoviedb.org/3/genre/movie/list?language=fr-FR&api_key={TMDB_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        genres = response.json()["genres"]
        for genre in genres:
            if genre["name"].lower() == category_name.lower():
                return genre["id"]
    return None

@app.get("/movies/category/{category_name}")
async def get_movies_by_category(category_name: str):
    category_id = get_category_id(category_name)
    if category_id is None:
        raise HTTPException(status_code=404, detail="Catégorie non trouvée.")

    url = f"https://api.themoviedb.org/3/discover/movie?with_genres={category_id}&language=fr-FR"
    headers = {
        "Authorization": f"Bearer {TMDB_ACCESS_TOKEN}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        movies_data = response.json()["results"]
        print("Données des films :", movies_data)  # Affichez les données des films
        films = []

        for movie in movies_data:
            film = Film(
                id_film=movie["id"],
                id_tmdb=movie["id"],
                title=movie["title"],
                producer=movie.get("production_companies", [{"name": "Inconnu"}])[0].get("name", "Inconnu"),
                category=movie.get("genres", [{"name": "Inconnu"}])[0].get("name", "Inconnu"),
                date=movie["release_date"][:4]
            )
            films.append(film.__dict__)

        return films
    else:
        raise HTTPException(status_code=response.status_code, detail="Erreur lors de la récupération des films par catégorie.")
