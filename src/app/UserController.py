from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from src.Model.APIUser import APIUser
from src.Model.JWTResponse import JWTResponse
from src.Service.PasswordService import (check_password_strength,
                                         validate_username_password)

from .init_app import jwt_service, user_repo, user_service
from .JWTBearer import JWTBearer

if TYPE_CHECKING:
    from src.Model.User import User

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(username: str, password: str) -> APIUser:
    """
    Fait la validation du nom d'utilisateur et du mot de passe
    """
    try:
        check_password_strength(password=password)
    except Exception:
        raise HTTPException(status_code=400, detail="Mot de passe trop faible") from Exception
    try:
        user: User = user_service.create_user(username=username, password=password)
    except Exception as error:
        raise HTTPException(status_code=409, detail="Nom d'utilisateur déjà existant") from error

    return APIUser(id=user.id, username=user.username)


@user_router.post("/jwt", status_code=status.HTTP_201_CREATED)
def login(username: str, password: str) -> JWTResponse:
    """
    Authentifie le nom d'utilisateur, le mot de passe et le jeton
    """
    try:
        user = validate_username_password(username=username, password=password, user_repo=user_repo)
    except Exception as error:
        raise HTTPException(status_code=403, detail="Combinaison du mot de passe et du nom d'utilisateur incorrecte") from error

    return jwt_service.encode_jwt(user.id)


@user_router.get("/me", dependencies=[Depends(JWTBearer())])
def get_user_own_profile(credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())]) -> APIUser:
    """
    Obtiens le profil authentifié
    """
    return get_user_from_credentials(credentials)


def get_user_from_credentials(credentials: HTTPAuthorizationCredentials) -> APIUser:
    token = credentials.credentials
    user_id = int(jwt_service.validate_user_jwt(token))
    user: User | None = user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    return APIUser(id=user.id, username=user.username)
