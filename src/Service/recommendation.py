import requests
from sklearn.metrics.pairwise import cosine_similarity

class RecommendationService:
    def __init__(self, api_key, access_token):
        self.api_key = api_key
        self.access_token = access_token
        self.all_genres = self.get_tmdb_genres()
        self.movies = self.get_tmdb_movies(1000)
        self.similarity_matrix = self.calculate_similarity()

    def get_tmdb_genres(self):
        headers = {"Authorization": f"Bearer {self.access_token}"}
        url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={self.api_key}&language=en-US"
        response = requests.get(url, headers=headers)
        genres = response.json().get('genres', [])
        genre_ids = [genre['id'] for genre in genres]
        return genre_ids

    def get_tmdb_movies(self, num_movies=1000):
        movies = []
        page = 1
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        while len(movies) < num_movies:
            url = f"https://api.themoviedb.org/3/movie/popular?api_key={self.api_key}&language=en-US&page={page}"
            response = requests.get(url, headers=headers)
            data = response.json()

            if 'results' not in data:
                raise ValueError(f"Erreur lors de la récupération des films : {data}")

            movies.extend(data['results'])
            page += 1
            if len(data['results']) == 0:
                break

        return movies[:num_movies]

    def calculate_similarity(self):
        genre_matrix = []
        for movie in self.movies:
            genres = movie['genre_ids']
            genre_vector = [1 if genre in genres else 0 for genre in self.all_genres]
            genre_matrix.append(genre_vector)
        return cosine_similarity(genre_matrix)

    def recommend_movies(self, movie_id, top_n=5):
        try:
            idx = next(i for i, movie in enumerate(self.movies) if movie['id'] == movie_id)
        except StopIteration:
            return []

        similarities = self.similarity_matrix[idx]
        similar_indices = similarities.argsort()[-top_n-1:-1][::-1]
        recommended_movies = [self.movies[i] for i in similar_indices]
        return recommended_movies
