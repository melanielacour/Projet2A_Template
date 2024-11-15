from typing import TYPE_CHECKING, Annotated
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from src.dao.db_connection import DBConnection
from pydantic import BaseModel
from src.Service.recommendation import RecommendationService
from src.app.init_app import recommendation_service
from src.app.dependencies import get_current_user

recommendation_router = APIRouter(prefix="/recommandation", tags=["Movie's Recommandation"])

# Initialisation de la classe RecommendationService

# Modèle de réponse pour une recommandation
class MovieRecommendation(BaseModel):
    id: int
    title: str
    overview: Optional[str]
    popularity: float
    release_date: str

@recommendation_router.get("/recommendations", response_model=List[MovieRecommendation])
def get_recommendations(movie_id: int, top_n: int = 5,  id_user: int = Depends(get_current_user)):
    movies= recommendation_service.get_tmdb_movies()
    if not movies:
        raise ValueError("")
    recommended_movies = recommendation_service.recommend_movies(movie_id, top_n)
    
    if not recommended_movies:
        raise HTTPException(status_code=404, detail="Aucune recommandation trouvée pour le film donné.")

    return [
        {
            "id": movie["id"],
            "title": movie["title"],
            "overview": movie.get("overview", "Aucune description disponible"),
            "popularity": movie["popularity"],
            "release_date": movie["release_date"]
        }
        for movie in recommended_movies
    ]