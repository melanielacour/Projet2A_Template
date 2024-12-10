from typing import TYPE_CHECKING, Annotated
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from src.dao.db_connection import DBConnection
from pydantic import BaseModel
from src.app.dependencies import get_current_user
from src.app.init_app import follower_dao
from src.dao.follower_dao import FollowerDao

scout_router = APIRouter(prefix="/scout", tags=["My Scouts/followers"])


# Endpoint pour suivre un éclaireur
@scout_router.post("/scouts/{id_scout}/follow", summary="Suivre un éclaireur")
async def follow_scout(id_scout: int, id_follower: int = Depends(get_current_user)):
    try:
        return follower_dao.follow_scout(id_follower=id_follower, id_scout=id_scout)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Endpoint pour ne plus suivre un éclaireur
@scout_router.delete(
    "/scouts/{id_scout}/unfollow", summary="Ne plus suivre un éclaireur"
)
async def unfollow_scout(
    id_scout: int,
    id_follower: int = Depends(get_current_user),
    db: DBConnection = Depends(),
):
    try:
        return follower_dao.unfollow_scout(id_follower=id_follower, id_scout=id_scout)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Endpoint pour obtenir la liste des éclaireurs suivis par un utilisateur
@scout_router.get("/users/{id_follower}/scouts", summary="Liste des éclaireurs suivis")
async def get_scouts_followed_by_user(
    id_follower: int = Depends(get_current_user), db: DBConnection = Depends()
):
    scouts = follower_dao.get_scouts_followed_by_user(id_follower=id_follower)
    return {"scouts": scouts}


# Endpoint pour obtenir la liste des utilisateurs qui suivent un éclaireur
@scout_router.get(
    "/scouts/{id_scout}/followers", summary="Liste des followers d'un éclaireur"
)
async def get_followers_of_scout(
    id_scout: int = Depends(get_current_user), db: DBConnection = Depends()
):
    followers = follower_dao.get_followers_of_scout(id_scout=id_scout)
    return {"followers": followers}


# Endpoint pour obtenir la watchlist des éclaireurs suivis par un utilisateur
@scout_router.get(
    "/users/{id_follower}/scouts/watchlist", summary="Watchlist des éclaireurs suivis"
)
async def get_watchlist_of_scouts(
    id_scout: int,
    did_follower: int = Depends(get_current_user),
    db: DBConnection = Depends(),
):
    watchlist = follower_dao.get_watchlist_of_scouts(
        id_follower=id_follower, id_scout=id_scout
    )
    return {"watchlist": watchlist}
