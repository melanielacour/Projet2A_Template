import os
import time
from datetime import datetime
from typing import List

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

from src.dao.user_repo import UserRepo
# from src.Model.Review import Review
from src.Service.MovieService import MovieService
from src.Service.PasswordService import PasswordService
from src.Service.UserService import UserService

app = FastAPI()
service = MovieService()

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


@app.get("/movies/title/{title}", response_model=Film, tags=["Films"])
async def get_movie_by_title(title: str):
    film = service.get_movie_by_title(title)
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
    is_scout: bool = False

@app.post("/register", tags=["User"])
def register_user(pseudo: str, password: str, is_scout: bool = False):
    return user_service.register_user(pseudo, password, is_scout)

@app.post("/login", tags=["User"])
def log_in(pseudo: str, password: str):
    return user_service.log_in(pseudo, password)


# ########################### Reviews ########################################

from src.dao.review_dao import ReviewDao
from src.Model.Review import Review

review_dao = ReviewDao(db_connection)

class Review(BaseModel):
    id_review: int
    id_film: int
    id_user: int
    comment: str

@app.get("/reviews/{title}", response_model=List[Review], tags=["Review"])
def get_reviews_by_title(title: str):
    """
    Récupère toutes les critiques pour un film donné par son titre.
    """
    reviews = review_dao.get_all_review_by_title(title)
    if not reviews:
        raise HTTPException(status_code=404, detail="Aucune critique trouvée pour ce film.")
    return reviews
