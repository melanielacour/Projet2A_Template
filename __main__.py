#from src.Interface.API import run_app
from src.Service.MovieService import MovieService
from src.app.API import run_app

if __name__ == "__main__":
    movie_service = MovieService()
    app = run_app()