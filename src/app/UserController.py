from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from src.dao.db_connection import DBConnection
from src.Model.APIUser import APIUser
from src.Model.JWTResponse import JWTResponse
from src.Service.PasswordService import PasswordService
from src.app.init_app import jwt_service, user_repo, user_service
from src.app.JWTBearer import JWTBearer
from pydantic import BaseModel
from src.app.dependencies import get_current_user
from src.Model.User import User


# Instanciation des services
db_connection = DBConnection()
user_dao = user_repo
password_service = PasswordService()


# Définir le routeur pour les utilisateurs
user_router = APIRouter(prefix="/users", tags=["Users"])

# Modèle Pydantic pour l'enregistrement des utilisateurs
class UserRegistration(BaseModel):
    pseudo: str
    password: str

@user_router.post("/register")
def register_user(pseudo: str, password: str):
    return user_service.register_user(pseudo, password)

@user_router.post("/login")
def log_in(pseudo: str, password: str):
    return user_service.log_in(pseudo, password)

# Modèles pour la mise à jour du pseudo et du mot de passe
class UpdatePseudoRequest(BaseModel):
    new_pseudo: str

class UpdatePasswordRequest(BaseModel):
    current_password: str
    new_password: str

@user_router.put("/user/update-pseudo")
async def update_pseudo(request: UpdatePseudoRequest, user_id: int = Depends(get_current_user)):
    try:
        message = user_service.update_pseudo(user_id=user_id, new_pseudo=request.new_pseudo)
        return {"message": message}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@user_router.put("/user/update-password")
async def update_password(request: UpdatePasswordRequest, user_id: int = Depends(get_current_user)):
    try:
        message = user_service.update_password(user_id=user_id, current_password=request.current_password, new_password=request.new_password)
        return {"message": message}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@user_router.put("/user/promote-to-scout")
async def promote_to_scout(user_id: int = Depends(get_current_user)):
    try:
        message = user_service.promote_to_scout(user_id=user_id)
        return {"message": message}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@user_router.put("/user/demote-scout")
async def demote_scout(user_id: int = Depends(get_current_user)):
    try:
        message = user_service.demote_scout(user_id=user_id)
        return {"message": message}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@user_router.get("/user/get-user-by-pseudo")
async def get_user_by_user_pseudo(pseudo: str, user_id2:int= Depends(get_current_user)):
    user=user_dao.get_by_username(pseudo)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return pseudo, user.id

@user_router.get("/user/get-user-by-id")
async def get_user_by_user_pseudo(id: int, user_id2:int= Depends(get_current_user)):
    user=user_dao.get_by_id(id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return id, user.username


