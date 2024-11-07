import os
import time
from datetime import datetime
from typing import List
from typing import Optional

from dotenv import load_dotenv

from src.dao.db_connection import DBConnection
from src.dao.user_repo import UserRepo

load_dotenv()

HOST = os.getenv("HOST")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")

import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt.exceptions import ExpiredSignatureError


from src.dao.user_repo import UserRepo
from src.Model.Review import Review
from src.Service.MovieService import MovieService
from src.Service.PasswordService import PasswordService
from src.Service.UserService import UserService


app = FastAPI()
service = MovieService()





# Fonction de dépendance pour valider le token
from src.Service.JWTService import JwtService
jwt_service=JwtService(os.environ["JWT_SECRET"], "HS256")
security = HTTPBearer() 


# Fonction de dépendance pour valider le token
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        # Utilisez directement jwt_service pour valider le token
        user_id = jwt_service.validate_user_jwt(token)
        return user_id  # Renvoie l'ID de l'utilisateur extrait du token
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expiré")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token invalide")
# ########################### Films ######################################

# modèle Pydantic pour les films


class Film(BaseModel):
    id_film: int
    id_tmdb: int
    title: str
    producer: str
    category: str
    date: str
    average_rate: float = 0.0
    ratings: list[int] = []



@app.get("/movies/title/{title}", response_model=List[Film], tags=["Films"])
async def get_movies_by_title(title: str):
    films = service.get_movie_by_title(title)
    if not films:
        raise HTTPException(status_code=404, detail="Aucun film trouvé")
    return films


@app.get("/movies/{id}", response_model=Film, tags=["Films"])
async def get_movie_by_id(id: str):
    film = service.get_movie_by_id(id)
    if not film:
        raise HTTPException(status_code=404, detail="Film non trouvé")
    return film

@app.get("/movies/category/{category_name}", response_model=list[Film], tags=["Films"])
async def get_movies_by_category(category_name: str):
    category_id = service.get_category_id(category_name)
    if category_id is None:
        raise HTTPException(status_code=404, detail="Catégorie non trouvée.")

    films = service.get_movies_by_category(category_id)
    return films


@app.get("/movies/director/{director_name}", response_model=list[Film], tags=["Films"])
async def get_movies_by_director(director_name: str):
    films = service.get_movies_by_director_name(director_name)
    if not films:
        raise HTTPException(status_code=404, detail="Aucun film trouvé pour ce réalisateur.")
    return films

# ########################### User ###########################################

db_connection = DBConnection()
user_dao = UserRepo(db_connection)
password_service = PasswordService()
user_service = UserService()


class UserRegistration(BaseModel):
    pseudo: str
    password: str

@app.post("/register", tags=["User"])
def register_user(pseudo: str, password: str):
    return user_service.register_user(pseudo, password)

@app.post("/login", tags=["User"])
def log_in(pseudo: str, password: str):
    return user_service.log_in(pseudo, password)


# ########################### Reviews ########################################

from src.dao.review_dao import ReviewDao
from src.Service.review_service import ReviewService
from src.Model.Review import Review

review_dao = ReviewDao(db_connection)

# Initialisation de ReviewService
review_service = ReviewService(ReviewDao(DBConnection()))

class ReviewRequest(BaseModel):
    note: Optional[int] = None
    comment: Optional[str] = None

@app.post("/reviews/id_local/{id_local}", tags=["Reviews"])
async def post_review_by_id_local(id_local: int, review: ReviewRequest, id_user: int = Depends(get_current_user)):
    try:
        return review_service.search_and_rate_movie_existing_movie(
            id_film=id_local, 
            id_user=id_user, 
            note=review.note, 
            comment=review.comment
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/reviews/id_tmdb/{id_tmdb}",tags=["Reviews"])
async def post_review_by_id_tmdb(id_tmdb: int, title: str, review: ReviewRequest, id_user: int = Depends(get_current_user)):
    try:
        return review_service.search_and_rate_movie_by_idtmdb(
            id_tmdb=id_tmdb, 
            title=title, 
            id_user=id_user, 
            note=review.note, 
            comment=review.comment
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/reviews/update_note", tags=["Reviews"])
async def update_note( id_film: int, note: int, id_user: int = Depends(get_current_user)):
    try:
        return review_service.update_note(id_user=id_user, id_film=id_film, note=note)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/reviews/update_comment", tags=["Reviews"])
async def update_comment(id_film: int, comment: str,id_user: int = Depends(get_current_user)):
    try:
        return review_service.update_comment(id_user=id_user, id_film=id_film, comment=comment)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/reviews/delete_note",tags=["Reviews"])
async def delete_note(id_film: int, id_user: int= Depends(get_current_user)):
    try:
        return review_service.delete_note(id_film=id_film, id_user=id_user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/reviews/delete_comment",tags=["Reviews"])
async def delete_comment(id_film: int, id_user: int = Depends(get_current_user)):
    try:
        return review_service.delete_comment(id_film=id_film, id_user=id_user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/reviews/average_rating/{id_film}", tags=["Reviews"])
async def get_average_rating(id_film: int):
    return {"average_rating": review_service.get_average_rating(id_film)}
# ########################### MovieRepo ########################################

from src.dao.movie_local import MovieRepo
from src.Model.movie_simple import MovieSimple

# Déclaration du modèle de réponse pour un film
class MovieSimple(BaseModel):
    id_local: int
    id_tmdb: int
    title: str

# Création d'une instance de MovieRepo
movie_repo = MovieRepo(DBConnection())

@app.get("/movies/tmdb_id/{id_tmdb}", response_model=MovieSimple, tags=["Movies"])
async def get_movie_by_tmdb_id(id_tmdb: int):
    movie = movie_repo.get_movie_by_tmdb_id(id_tmdb)
    if not movie:
        raise HTTPException(status_code=404, detail="Film non trouvé")
    return movie

# ########################### UserMovie ########################################
from src.Model.user_movie import UserMovie
from src.Service.user_movie_service import UserMovieService
from src.dao.user_movies_dao import UserMovieDao
# Dependency pour obtenir l'instance de UserMovieService
def get_user_movie_service():
    db_connection = DBConnection()
    user_movie_dao = UserMovieDao(db_connection)
    return UserMovieService(user_movie_dao)

# Pydantic Models
class MovieRequest(BaseModel):
    id_film: int
    status: str

class MovieListResponse(BaseModel):
    id_user: int
    id_film: int
    status: str

# Endpoints

@app.post("/movies/add", tags=["User's Movies"])
async def add_movie_to_list(request: MovieRequest, service: UserMovieService = Depends(get_user_movie_service), id_user: int = Depends(get_current_user)):
    """
    Ajouter un film à la liste des films vus ou à voir d'un utilisateur.
    """
    service.add_movie_to_list(id_user=id_user, id_film=request.id_film, status=request.status)
    return {"message": "Film ajouté avec succès"}

@app.put("/movies/status/{id_film}", tags=["User's Movies"])
async def update_movie_status(id_film: int, new_status: str, service: UserMovieService = Depends(get_user_movie_service),id_user: int = Depends(get_current_user)):
    """
    Modifier le statut d'un film existant pour un utilisateur.
    """
    service.update_movie_status(id_user=id_user, id_film=id_film, new_status=new_status)
    return {"message": "Statut du film mis à jour avec succès"}

@app.delete("/movies/delete/{id_film}", tags=["User's Movies"])
async def delete_movie_from_list(id_film: int, status: str, service: UserMovieService = Depends(get_user_movie_service), id_user: int = Depends(get_current_user)):
    """
    Supprimer un film de la liste des films vus ou à voir d'un utilisateur.
    """
    if not service.delete_movie_from_list(id_user=id_user, id_film=id_film, status=status):
        raise HTTPException(status_code=404, detail="Film non trouvé dans la liste")
    return {"message": "Film supprimé de la liste avec succès"}

@app.get("/movies/watchlist/{id_user}", response_model=List[MovieListResponse], tags=["User's Movies"])
async def get_watchlist(service: UserMovieService = Depends(get_user_movie_service),id_user: int = Depends(get_current_user)):
    """
    Récupérer la liste des films vus (watchlist) d'un utilisateur.
    """
    watchlist = service.get_watchlist(id_user=id_user)
    if not watchlist:
        raise HTTPException(status_code=404, detail="Aucun film vu trouvé")
    return watchlist

@app.get("/movies/seenlist/{id_user}", response_model=List[MovieListResponse], tags=["User's Movies"])
async def get_seenlist(service: UserMovieService = Depends(get_user_movie_service),id_user: int = Depends(get_current_user)):
    """
    Récupérer la liste des films à voir d'un utilisateur.
    """
    to_watch_list = service.get_seenlist(id_user=id_user)
    if not to_watch_list:
        raise HTTPException(status_code=404, detail="Aucun film à voir trouvé")
    return to_watch_list

@app.get("/movies/all_movies/{id_user}", response_model=List[MovieListResponse], tags=["User's Movies"])
async def get_all_movies(service: UserMovieService = Depends(get_user_movie_service),id_user: int = Depends(get_current_user)):
    """
    Récupérer la liste de tous les films (vus et à voir) associés à un utilisateur.
    """
    all_movies = service.get_all_movies(id_user=id_user)
    if not all_movies:
        raise HTTPException(status_code=404, detail="Aucun film trouvé")
    return all_movies