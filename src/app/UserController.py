from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel, SecretStr

from src.app.dependencies import get_current_user
from src.app.init_app import jwt_service, user_repo, user_service
from src.app.JWTBearer import JWTBearer
from src.dao.db_connection import DBConnection
from src.Model.APIUser import APIUser
from src.Model.JWTResponse import JWTResponse
from src.Model.User import User
from src.Service.PasswordService import PasswordService

# Instanciation des services
db_connection = DBConnection()
user_dao = user_repo
password_service = PasswordService()


# Définir le routeur pour les utilisateurs
user_router = APIRouter(prefix="/users", tags=["Users"])

# Modèle Pydantic pour l'enregistrement des utilisateurs
class UserRegistration(BaseModel):
    pseudo: str
    password: SecretStr

@user_router.post("/register")
def register_user(pseudo: str, password: SecretStr):
    try:
        message = user_service.register_user(pseudo, password)
        return {"message": message}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@user_router.post("/login")

def log_in(pseudo: str, password: SecretStr):
    try:
        message = user_service.log_in(pseudo, password.get_secret_value())
        return {"message": message}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Modèles pour la mise à jour du pseudo et du mot de passe
class UpdatePseudoRequest(BaseModel):
    new_pseudo: str

class UpdatePasswordRequest(BaseModel):
    current_password: SecretStr
    new_password: SecretStr

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

@user_router.get("/user/view profil")
async def view_profil(user_id: int= Depends(get_current_user)):
    user=user_service.view_profil(user_id)
    res={"id": user.id, "pseudo": user.username, "is_scout": user.is_scout}
    return res

@user_router.delete("/user/delete_user")
async def delete_user(user_id:int= Depends(get_current_user)):
    return user_service.delete_profil(user_id)
