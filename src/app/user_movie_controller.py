from typing import TYPE_CHECKING, Annotated
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from src.dao.db_connection import DBConnection
from src.Service.user_movie_service import UserMovieService
from pydantic import BaseModel
from src.app.dependencies import get_current_user
from src.app.init_app import get_user_movie_service


usermovie_router = APIRouter(prefix="/movies", tags=["MyMovies"])
# Pydantic Models
class MovieRequest(BaseModel):
    id_film: int
    status: str

class MovieListResponse(BaseModel):
    id_user: int
    id_film: int
    status: str

# Endpoints

@usermovie_router.post("/add")
async def add_movie_to_list(request: MovieRequest, service: UserMovieService = Depends(get_user_movie_service), id_user: int = Depends(get_current_user)):
    """
    Ajouter un film à la liste des films vus ou à voir d'un utilisateur.
    """
    service.add_movie_to_list(id_user=id_user, id_film=request.id_film, status=request.status)
    return {"message": "Film ajouté avec succès"}

@usermovie_router.put("/status/{id_film}")
async def update_movie_status(id_film: int, new_status: str, service: UserMovieService = Depends(get_user_movie_service),id_user: int = Depends(get_current_user)):
    """
    Modifier le statut d'un film existant pour un utilisateur.
    """
    service.update_movie_status(id_user=id_user, id_film=id_film, new_status=new_status)
    return {"message": "Statut du film mis à jour avec succès"}

@usermovie_router.delete("/delete/{id_film}")
async def delete_movie_from_list(id_film: int, status: str, service: UserMovieService = Depends(get_user_movie_service), id_user: int = Depends(get_current_user)):
    """
    Supprimer un film de la liste des films vus ou à voir d'un utilisateur.
    """
    if not service.delete_movie_from_list(id_user=id_user, id_film=id_film, status=status):
        raise HTTPException(status_code=404, detail="Film non trouvé dans la liste")
    return {"message": "Film supprimé de la liste avec succès"}

@usermovie_router.get("/watchlist/{id_user}", response_model=List[MovieListResponse])
async def get_watchlist(service: UserMovieService = Depends(get_user_movie_service),id_user: int = Depends(get_current_user)):
    """
    Récupérer la liste des films vus (watchlist) d'un utilisateur.
    """
    watchlist = service.get_watchlist(id_user=id_user)
    if not watchlist:
        raise HTTPException(status_code=404, detail="Aucun film vu trouvé")
    return watchlist

@usermovie_router.get("/seenlist/{id_user}", response_model=List[MovieListResponse])
async def get_seenlist(service: UserMovieService = Depends(get_user_movie_service),id_user: int = Depends(get_current_user)):
    """
    Récupérer la liste des films à voir d'un utilisateur.
    """
    to_watch_list = service.get_seenlist(id_user=id_user)
    if not to_watch_list:
        raise HTTPException(status_code=404, detail="Aucun film à voir trouvé")
    return to_watch_list

@usermovie_router.get("/all_movies/{id_user}", response_model=List[MovieListResponse])
async def get_all_movies(service: UserMovieService = Depends(get_user_movie_service),id_user: int = Depends(get_current_user)):
    """
    Récupérer la liste de tous les films (vus et à voir) associés à un utilisateur.
    """
    all_movies = service.get_all_movies(id_user=id_user)
    if not all_movies:
        raise HTTPException(status_code=404, detail="Aucun film trouvé")
    return all_movies