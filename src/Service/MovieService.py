import os
import random
from datetime import datetime

import requests

from src.Model.Film import Film

TMDB_ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3YTM1YmQwMDE2Mzk5MDNmNWM4MzBlODhkZDg2ZWQzMCIsIm5iZiI6MTcyOTU4MTc0MS41Nzg2NTEsInN1YiI6IjY2ZTQ0NmI5OTAxM2ZlODcyMjI0MTc1MiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.UvX882tvk0XKaN5mrivSQzXfzzXEOAqSX_4nzSfscFY"
TMDB_API_KEY = "7a35bd001639903f5c830e88dd86ed30"

class MovieService:
    def get_category_id(self, category_name: str):
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

    def get_movie_by_id(self, id: str) -> Film:
        headers = {"Authorization": f"Bearer {TMDB_ACCESS_TOKEN}"}
        details_url = f"https://api.themoviedb.org/3/movie/{id}?language=fr-FR"
        details_response = requests.get(details_url, headers=headers)

        if details_response.status_code == 200:
            details_data = details_response.json()
            return Film(
                id_film=details_data["id"],
                id_tmdb=details_data["id"],
                title=details_data["title"],
                producer=details_data.get("production_companies", [{"name": "Inconnu"}])[0].get("name", "Inconnu"),
                category=details_data.get("genres", [{"name": "Inconnu"}])[0].get("name", "Inconnu"),
                date=details_data["release_date"][:4] if "release_date" in details_data else "Inconnue"
            )
        else:
            raise Exception(f"Erreur lors de la récupération des détails : {details_response.status_code}")

    def get_movie_by_title(self, title: str) -> list[Film]:
        headers = {"Authorization": f"Bearer {TMDB_ACCESS_TOKEN}"}
        search_url = f"https://api.themoviedb.org/3/search/movie?query={title}&language=fr-FR&page=1"
        search_response = requests.get(search_url, headers=headers)

        if search_response.status_code == 200:
            search_results = search_response.json()["results"]

            films = []
            for film_data in search_results[:5]:
                film_id = film_data["id"]

                details_url = f"https://api.themoviedb.org/3/movie/{film_id}?language=fr-FR"
                details_response = requests.get(details_url, headers=headers)

                if details_response.status_code == 200:
                    details_data = details_response.json()
                    films.append(Film(
                        id_film=details_data["id"],
                        id_tmdb=details_data["id"],
                        title=details_data["title"],
                        producer=details_data.get("production_companies", [{"name": "Inconnu"}])[0].get("name", "Inconnu"),
                        category=details_data.get("genres", [{"name": "Inconnu"}])[0].get("name", "Inconnu"),
                        date=details_data["release_date"][:4] if "release_date" in details_data else "Inconnue"
                    ))

            if films:
                return films
            else:
                raise Exception("Aucun film trouvé.")
        else:
            raise Exception(f"Erreur lors de la recherche : {search_response.status_code}")

    def get_movies_by_category(self, category_id: int):
        headers = {"Authorization": f"Bearer {TMDB_ACCESS_TOKEN}"}
        url = f"https://api.themoviedb.org/3/discover/movie?with_genres={category_id}&language=fr-FR"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            movies_data = response.json()["results"]
            films = []

            for movie in movies_data:
                details_url = f"https://api.themoviedb.org/3/movie/{movie['id']}?language=fr-FR"
                details_response = requests.get(details_url, headers=headers)

                if details_response.status_code == 200:
                    details_data = details_response.json()
                    film = Film(
                        id_film=details_data["id"],
                        id_tmdb=details_data["id"],
                        title=details_data["title"],
                        producer=details_data.get("production_companies", [{"name": "Inconnu"}])[0]["name"],
                        category=details_data.get("genres", [{"name": "Inconnu"}])[0]["name"],
                        date=details_data["release_date"][:4] if "release_date" in details_data else "Inconnue"
                    )
                    films.append(film)
            return films
        else:
            raise Exception(f"Erreur lors de la récupération des films par catégorie : {response.status_code}")

    def get_movies_by_director(self, director_id: int):
        headers = {"Authorization": f"Bearer {TMDB_ACCESS_TOKEN}"}
        url = f"https://api.themoviedb.org/3/discover/movie?with_crew={director_id}&language=fr-FR"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            movies_data = response.json().get("results", [])
            films = []

            for movie in movies_data:
                details_url = f"https://api.themoviedb.org/3/movie/{movie['id']}?language=fr-FR"
                details_response = requests.get(details_url, headers=headers)

                if details_response.status_code == 200:
                    details_data = details_response.json()
                    film = Film(
                        id_film=details_data["id"],
                        id_tmdb=details_data["id"],
                        title=details_data["title"],
                        producer=details_data.get("production_companies", [{"name": "Inconnu"}])[0]["name"],
                        category=details_data.get("genres", [{"name": "Inconnu"}])[0]["name"],
                        date=details_data["release_date"][:4] if "release_date" in details_data else "Inconnue"
                    )
                    films.append(film)
            return films
        else:
            raise Exception(f"Erreur lors de la récupération des films par réalisateur : {response.status_code} - {response.text}")

    def get_movies_by_director_name(self, director_name: str):
        headers = {"Authorization": f"Bearer {TMDB_ACCESS_TOKEN}"}
        search_url = f"https://api.themoviedb.org/3/search/person?query={director_name}&language=fr-FR"
        search_response = requests.get(search_url, headers=headers)

        if search_response.status_code == 200:
            search_results = search_response.json()["results"]
            if search_results:
                director_id = search_results[0]["id"]
                return self.get_movies_by_director(director_id)
            else:
                raise Exception("Aucun réalisateur trouvé.")
        else:
            raise Exception(f"Erreur lors de la recherche du réalisateur : {search_response.status_code}")
