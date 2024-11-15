import requests
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Récupérer les genres disponibles depuis TMDB
def get_tmdb_genres(api_key):
    url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&language=en-US"
    response = requests.get(url)
    genres = response.json().get('genres', [])
    genre_ids = [genre['id'] for genre in genres]
    genre_names = [genre['name'] for genre in genres]
    return genre_ids, genre_names

# Récupérer les films depuis TMDB (avec gestion de la pagination)
def get_tmdb_movies(api_key, num_movies=100):
    movies = []
    page = 1
    while len(movies) < num_movies:
        url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=en-US&page={page}"
        response = requests.get(url)
        data = response.json()

        # Vérifier si 'results' est présent dans la réponse
        if 'results' not in data:
            print(f"Erreur : La réponse de l'API ne contient pas la clé 'results'. Réponse obtenue : {data}")
            return []

        movies.extend(data['results'])
        page += 1
        if len(data['results']) == 0:  # Si la page est vide, arrêter
            break

    # Limiter la liste à `num_movies` si nécessaire
    movies = movies[:num_movies]
    
    # Afficher les 5 premiers films pour vérification
    print("Voici les 5 premiers films chargés :")
    for movie in movies[:5]:
        print(f"{movie['title']} ({movie['id']})")
    
    print(f"{len(movies)} films ont été chargés avec succès.")
    return movies

# Calcul de la similarité entre les genres
def calculate_similarity(movies, all_genres):
    # Créer une matrice des genres des films
    genre_matrix = []
    for movie in movies:
        genres = movie['genre_ids']
        genre_vector = [1 if genre in genres else 0 for genre in all_genres]
        genre_matrix.append(genre_vector)
    
    # Calcul de la similarité cosinus
    similarity_matrix = cosine_similarity(genre_matrix)
    return similarity_matrix

# Recommander des films basés sur la similarité
def recommend_movies(movies, similarity_matrix, movie_id, top_n=5):
    # Vérifier si movie_id existe dans la liste
    try:
        idx = next(i for i, movie in enumerate(movies) if movie['id'] == movie_id)
    except StopIteration:
        print(f"Le film avec l'ID {movie_id} n'a pas été trouvé.")
        return []

    similarities = similarity_matrix[idx]
    
    # Classer les films en fonction de la similarité
    similar_indices = similarities.argsort()[-top_n-1:-1][::-1]
    recommended_movies = [movies[i] for i in similar_indices]
    
    return recommended_movies

# Exemple d'utilisation
api_key = "ton_api_key"  # Remplace avec ta clé API TMDB
movies = get_tmdb_movies(api_key)

# Récupérer les genres disponibles
if movies:
    genre_ids, genre_names = get_tmdb_genres(api_key)

    # Calcul de la similarité entre les genres
    similarity_matrix = calculate_similarity(movies, genre_ids)

    # Recommander des films basés sur un ID de film spécifique (par exemple, movie_id=1)
    movie_id = 1  # Remplace par l'ID du film pour lequel tu veux des recommandations
    recommended_movies = recommend_movies(movies, similarity_matrix, movie_id)

    # Afficher les films recommandés
    print("Films recommandés :")
    for movie in recommended_movies:
        print(f"{movie['title']} ({movie['id']})")
