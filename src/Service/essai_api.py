import requests


class Film:
    def __init__(self, id_film, id_tmdb, title, producer, category, date, average_rate, ratings):
        self.id_film = id_film
        self.id_tmdb = id_tmdb
        self.title = title
        self.producer = producer
        self.category = category
        self.date = date
        self.average_rate = average_rate
        self.ratings = ratings




def get_film_by_title(title: str):
    url = f"http://127.0.0.1:8000/movies/title/{title}"
    response = requests.get(url)

    if response.status_code == 200:
        raw_film = response.json()

        film = Film(
            id_film=raw_film['id_film'],
            id_tmdb=raw_film['id_tmdb'],
            title=raw_film['title'],
            producer=raw_film['producer'],
            category=raw_film['category'],
            date=raw_film['date'],
            average_rate=raw_film['average_rate'],
            ratings=raw_film['ratings']
        )
        return film
    else:
        print(f"Erreur lors de la récupération du film : {response.status_code}")
        return None


# Exécution de la fonction pour le titre "Inception"

film = get_film_by_title("Inception")
print(f"Titre : {film.title}, Producteur : {film.producer}, Date : {film.date}, ID TMDB : {film.id_tmdb}, Moyenne des notes : {film.average_rate}")
