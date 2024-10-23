import random
import time
from datetime import datetime

import requests
from fastapi import FastAPI, HTTPException
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


# 200 films aléatoire
@app.get("/movies", response_model=list[Film])
async def get_movies():
    headers = {
        "Authorization": f"Bearer {TMDB_ACCESS_TOKEN}"
    }
    films = []
    total_films_needed = 200
    films_per_page = 20
    total_pages = total_films_needed // films_per_page + 1

    for page in range(1, total_pages + 1):
        url = f"https://api.themoviedb.org/3/movie/popular?language=fr-FR&page={page}"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            results = response.json()["results"]
            for movie in results:
                film = Film(
                    id_film=0,
                    id_tmdb=movie["id"],
                    title=movie["title"],
                    producer="N/A",
                    category="N/A",
                    date=datetime.strptime(movie["release_date"], "%Y-%m-%d"),
                    average_rate=0.0,
                    ratings=[]
                )
                films.append(film)
        else:
            return {"error": f"Erreur lors de la récupération des films. Statut : {response.status_code}"}

    # sélectionner aléatoirement 200 films
    selected_films = random.sample(films, min(total_films_needed, len(films)))

    return selected_films

# film par titre
@app.get("/movies/title/{title}")
async def get_movie_by_title(title: str):
    search_url = f"https://api.themoviedb.org/3/search/movie?query={title}&language=fr-FR&page=1"
    headers = {
        "Authorization": f"Bearer {TMDB_ACCESS_TOKEN}"
    }
    search_response = requests.get(search_url, headers=headers)

    if search_response.status_code == 200:
        search_results = search_response.json()["results"]
        if search_results:
            film_data = search_results[0]  # on prend le premier film trouvé
            film_id = film_data["id"]  # obtenir l'id du film

            details_url = f"https://api.themoviedb.org/3/movie/{film_id}?language=fr-FR"
            details_response = requests.get(details_url, headers=headers)

            if details_response.status_code == 200:
                details_data = details_response.json()
                film = Film(
                    id_film=details_data["id"],  # utiliser l'id TMDB comme id du film
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


# ###### films par genre #########
# Fonction pour obtenir l'ID de la catégorie à partir de son nom
def get_category_id(category_name: str):
    categories = {
        "action": 28,
        "aventure": 12,
        "animation": 16,
        "comédie": 35,
        "crime": 80,
        "documentaire": 99,
        "drame": 18,
        "familial": 10751,
        "fantastique": 14,
        "horreur": 27,
        "musique": 10402,
        "mystère": 9648,
        "romance": 10749,
        "science-fiction": 878,
        "téléfilm": 10770,
        "thriller": 53,
        "guerre": 10752,
        "western": 37
    }
    return categories.get(category_name.lower())


@app.get("/movies/category/{category_name}")
async def get_movies_by_category(category_name: str):
    # Obtenir l'id de la catégorie en fonction du nom
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
        print("Données des films :", movies_data)
        films = []

        for movie in movies_data:
            film_id = movie["id"]

            # Faire une requête en plus pour obtenir les détails complets de chaque film
            details_url = f"https://api.themoviedb.org/3/movie/{film_id}?language=fr-FR"
            details_response = requests.get(details_url, headers=headers)

            if details_response.status_code == 200:
                details_data = details_response.json()

                # Vérification des producers
                if "production_companies" in details_data and details_data["production_companies"]:
                    producer = details_data["production_companies"][0]["name"]
                else:
                    producer = "Inconnu"

                # Vérification des categories
                if "genres" in details_data and details_data["genres"]:
                    category = details_data["genres"][0]["name"]
                else:
                    category = "Inconnu"

                # Vérification de la date de sortie
                date = details_data["release_date"][:4] if "release_date" in details_data and details_data["release_date"] else "Inconnue"

                # Créer l'objet Film
                film = Film(
                    id_film=details_data["id"],
                    id_tmdb=details_data["id"],
                    title=details_data["title"],
                    producer=producer,
                    category=category,
                    date=date
                )
                films.append(film.__dict__)
            else:
                print(f"Erreur lors de la récupération des détails du film {film_id}")

        return films
    else:
        raise HTTPException(status_code=response.status_code, detail="Erreur lors de la récupération des films par catégorie.")




# films par réalisateur
@app.get("/movies/director/{director_name}")
async def get_movies_by_director(director_name: str):
    # Récupérer l'Id du réalisateur
    director_id_url = f"https://api.themoviedb.org/3/search/person?query={director_name}&language=fr-FR"
    headers = {
        "Authorization": f"Bearer {TMDB_ACCESS_TOKEN}"
    }
    director_response = requests.get(director_id_url, headers=headers)

    if director_response.status_code == 200:
        director_data = director_response.json()["results"]
        if not director_data:
            raise HTTPException(status_code=404, detail="Réalisateur non trouvé.")

        director_id = director_data[0]["id"]  # Prendre le premier résultat

        # Utiliser l'Id pour récupérer les films
        url = f"https://api.themoviedb.org/3/discover/movie?with_crew={director_id}&language=fr-FR"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            movies_data = response.json()["results"]
            films = []

            for movie in movies_data:
                film_id = movie["id"]

                # Requête en plus pour obtenir les détails complets de chaque film
                details_url = f"https://api.themoviedb.org/3/movie/{film_id}?language=fr-FR"
                details_response = requests.get(details_url, headers=headers)

                if details_response.status_code == 200:
                    details_data = details_response.json()

                    # Vérification des producteurs
                    if "production_companies" in details_data and details_data["production_companies"]:
                        producer = details_data["production_companies"][0]["name"]
                    else:
                        producer = "Inconnu"

                    # Vérification des catégories
                    if "genres" in details_data and details_data["genres"]:
                        category = details_data["genres"][0]["name"]
                    else:
                        category = "Inconnu"

                    # Vérification de la date de sortie
                    date = details_data["release_date"][:4] if "release_date" in details_data and details_data["release_date"] else "Inconnue"

                    # Créer l'objet Film
                    film = Film(
                        id_film=details_data["id"],
                        id_tmdb=details_data["id"],
                        title=details_data["title"],
                        producer=producer,
                        category=category,
                        date=date,
                        average_rate=0.0,  # Remplace par la logique appropriée si nécessaire
                        ratings=[]  # Remplace par la logique appropriée si nécessaire
                    )
                    films.append(film.__dict__)
                else:
                    print(f"Erreur lors de la récupération des détails du film {film_id}")

            return films
        else:
            raise HTTPException(status_code=response.status_code, detail="Erreur lors de la récupération des films.")
    else:
        raise HTTPException(status_code=director_response.status_code, detail="Erreur lors de la recherche du réalisateur.")
