# Fonction de dépendance pour valider le token
import os
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException, Depends
from jwt.exceptions import ExpiredSignatureError
from src.Service.JWTService import JwtService
from dotenv import load_dotenv

load_dotenv()
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