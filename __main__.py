from src.Interface.API import run_app
from src.Service.MovieService import MovieService
from src.App.API import run_app

if __name__ == "__main__":
    movie_service = MovieService(None)
    app = run_app(movie_service=movie_service)
    app = run_app()