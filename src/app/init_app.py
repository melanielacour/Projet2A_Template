from dotenv import load_dotenv

from src.dao.db_connection import DBConnection
from src.dao.user_repo import UserRepo
from src.dao.review_dao import ReviewDao
from src.Service.JWTService import JwtService
from src.Service.UserService import UserService
from src.Service.review_service import ReviewService
from src.Model.user_movie import UserMovie
from src.Service.user_movie_service import UserMovieService
from src.dao.user_movies_dao import UserMovieDao
from src.dao.follower_dao import FollowerDao
from src.dao.movie_local import MovieRepo
load_dotenv()
db_connection = DBConnection()
user_repo = UserRepo(db_connection)
review_dao = ReviewDao(db_connection)
jwt_service = JwtService()
user_service = UserService()
review_service = ReviewService(ReviewDao(db_connection))
follower_dao = FollowerDao(db_connection)
movie_repo = MovieRepo(db_connection)

def get_user_movie_service():
    db_connection = DBConnection()
    user_movie_dao = UserMovieDao(db_connection)
    return UserMovieService(user_movie_dao)