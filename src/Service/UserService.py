import os

from dotenv import load_dotenv

from src.dao.db_connection import DBConnection
from src.dao.user_repo import UserRepo
from src.Service.JWTService import JwtService
from src.Service.PasswordService import PasswordService

load_dotenv()

class UserService:
    def __init__(self):
        self.user_repo = UserRepo(DBConnection())
        self.password_service = PasswordService()
        self.jwt_service = JwtService(os.environ["JWT_SECRET"], "HS256")

    def register_user(self, pseudo: str, password: str, is_scout: bool = False) -> str:
        """
        Cette méthode permet d'inscrire un nouvel utilisateur dans le système.

        Paramètres:
        -----------
        pseudo : str
            Le pseudo de l'utilisateur.
        password : str
            Le mot de passe de l'utilisateur.
        is_scout : bool, optional
            Indique si l'utilisateur est un éclaireur (scout). Par défaut, False.

        Retourne:
        ---------
        str
            Message de confirmation si l'utilisateur est inscrit avec succès.

        Lève:
        -----
        ValueError:
            Si l'identifiant est déjà utilisé ou si le mot de passe ne respecte pas les règles.
        """

        # Vérifier si l'utilisateur existe déjà
        if self.user_repo.get_by_username(pseudo):
            raise ValueError("Cet identifiant est déjà utilisé.")

        # Valider la force du mot de passe
        self.password_service.check_password_strength(password)

        # Hacher le mot de passe avant de l'enregistrer
        hashed_password = self.password_service.hash_password(password)

        # Créer le nouvel utilisateur dans la base de données avec le mot de passe haché
        user_cree = self.user_repo.create_user(username=pseudo, is_scout=is_scout, password=hashed_password)

        if user_cree:
            return "Vous êtes bien inscrit !"
        else:
            raise ValueError("Erreur lors de l'inscription de l'utilisateur.")

    def log_in(self, pseudo: str, password: str) -> dict:
        """
        Cette méthode permet à un utilisateur de se connecter en fournissant un pseudo et un mot de passe.
        Elle vérifie l'existence de l'utilisateur et renvoie un booléen pour indiquer le succès ou l'échec de la connexion.

        Paramètres:
        -----------
        pseudo : str
            Le pseudo de l'utilisateur.
        password : str
            Le mot de passe de l'utilisateur.

        Retourne:
        ---------
        dict
            Un dictionnaire contenant le succès et le token JWT en cas d'authentification réussie.

        Lève:
        -----
        ValueError:
            Si l'identifiant ou le mot de passe est incorrect.
        """

        # On récupère le pseudo de l'utilisateur
        user = self.user_repo.get_by_username(pseudo)

        # Vérifie si l'utilisateur existe
        if not user:
            raise ValueError("Identifiant incorrect.")

        # Vérifier si le mot de passe correspond au pseudo
        if not self.password_service.validate_password(pseudo, password):
            raise ValueError("Mot de passe incorrect.")

        # Générer un token JWT
        jwt_response = self.jwt_service.encode_jwt(user.id)

        # Retourner la réponse avec True et le token
        return {"success": True, "token": jwt_response.access_token}
