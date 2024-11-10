from dotenv import load_dotenv

from src.dao.db_connection import DBConnection
from src.dao.user_repo import UserRepo
from src.Service.JWTService import JwtService
from src.Service.UserService import UserService

load_dotenv()
db_connection = DBConnection()
user_repo = UserRepo(db_connection)
jwt_service = JwtService()
user_service = UserService()
