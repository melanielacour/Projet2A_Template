import os

from dotenv import load_dotenv

from src.dao.db_connection import DBConnection
from src.dao.follower_dao import FollowerDao
from src.dao.review_dao import ReviewDao
from src.dao.user_repo import UserRepo
from src.Service.JWTService import JwtService
from src.Service.PasswordService import PasswordService

load_dotenv()

class UserService:
    """
    Cette classe gère l'inscription, la connexion, la mise à jour des informations utilisateur, et la gestion des statuts d'éclaireur,
    en assurant la validation des identifiants et la sécurité des mots de passe.
    """

    def __init__(self):
        self.user_repo = UserRepo(DBConnection())
        self.password_service = PasswordService()
        self.jwt_service = JwtService(os.environ["JWT_SECRET"], "HS256")

    def register_user(self, pseudo: str, password: str) -> str:
        """
        Cette méthode permet d'inscrire un nouvel utilisateur dans le système.

        Paramètres:
        -----------
        pseudo : str
            Le pseudo de l'utilisateur.
        password : str
            Le mot de passe de l'utilisateur.

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
        pseudo = pseudo.strip()
        password = password.strip()
        if self.user_repo.get_by_username(pseudo):
            raise ValueError("Cet identifiant est déjà utilisé.")

        # Valider la force du mot de passe
        self.password_service.check_password_strength(password)

        # Hacher le mot de passe avant de l'enregistrer
        hashed_password = self.password_service.hash_password(password)

        # Créer le nouvel utilisateur dans la base de données avec le mot de passe haché
        user_cree = self.user_repo.insert_into_db(username=pseudo, salt= None, hashed_password=hashed_password)

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
        if not self.password_service.validate_pseudo_password(pseudo, password):
            raise ValueError("Mot de passe incorrect.")

        # Générer un token JWT
        jwt_response = self.jwt_service.encode_jwt(user.id)

        # Retourner la réponse avec True et le token
        return {"success": True, "token": jwt_response.access_token}

    def update_pseudo(self, user_id: int, new_pseudo: str) -> str:
        """
        Permet de changer le pseudo d'un utilisateur.

        Paramètres:
        -----------
        user_id : int
            L'identifiant de l'utilisateur.
        new_pseudo : str
            Le nouveau pseudo souhaité.

        Retourne:
        ---------
        str
            Message de confirmation si le pseudo est modifié avec succès.
        """
        existing_user = self.user_repo.get_by_id(user_id)
        if not existing_user:
            raise ValueError("L'utilisateur n'existe pas. Veuillez créer un compte.")
        
        # Vérifier si le nouveau pseudo est déjà pris
        if self.user_repo.get_by_username(new_pseudo):
            raise ValueError("Ce pseudo est déjà utilisé.")
        
        # Mettre à jour le pseudo
        self.user_repo.update_pseudo(user_id, new_pseudo)
        return "Le pseudo a été mis à jour avec succès."
    def update_password(self, user_id: int, current_password: str, new_password: str) -> str:
        """
        Permet de changer le mot de passe d'un utilisateur.

        Paramètres:
        -----------
        user_id : int
            L'identifiant de l'utilisateur.
        current_password : str
            Le mot de passe actuel pour vérification.
        new_password : str
            Le nouveau mot de passe souhaité.

        Retourne:
        ---------
        str
            Message de confirmation si le mot de passe est modifié avec succès.
        """
        # Vérifier le mot de passe actuel
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("L'utilisateur n'existe pas. Veuillez créer un compte.")
        
        if not self.password_service.validate_pseudo_password(user.username, current_password):
            raise ValueError("Mot de passe actuel incorrect.")

        # Vérifier la force du nouveau mot de passe
        self.password_service.check_password_strength(new_password)

        # Mettre à jour le mot de passe avec le nouveau mot de passe haché
        hashed_password = self.password_service.hash_password(new_password)
        self.user_repo.update_password(user_id, hashed_password)
        return "Le mot de passe a été mis à jour avec succès."


    def promote_to_scout(self, user_id: int) -> str:
        """
        Passe le statut de l'utilisateur à éclaireur (true) si celui-ci a au moins 10 commentaires.

        Paramètres:
        -----------
        user_id : int
            Identifiant de l'utilisateur.

        Retourne:
        ---------
        str
            Message confirmant le passage à éclaireur ou indiquant le non-respect des conditions.
        """
        # Vérification du nombre de commentaires de l'utilisateur
        user=self.user_repo.get_by_id(user_id)
        if user.is_scout:
            raise ValueError("Vous êtes déja un éclaireur")
        user_reviews = ReviewDao(DBConnection()).get_all_reviews_by_user_id(user_id)
        if len(user_reviews) >= 10:
            self.user_repo.update_status(user_id, True)
            return "Vous êtes maintenant éclaireur !"
        else:
            return "Vous ne remplissez pas les conditions nécessaires pour devenir éclaireur."

    def demote_scout(self, user_id: int) -> str:
        """
        Révoque le statut éclaireur de l'utilisateur, passant `is_scout` à false.

        Paramètres:
        -----------
        user_id : int
            Identifiant de l'utilisateur.

        Retourne:
        ---------
        str
            Message confirmant la révocation du statut éclaireur.
        """
        user=self.user_repo.get_by_id(user_id)
        if not user.is_scout:
            raise ValueError("Vous n'êtes pas un éclaireur")
        self.user_repo.update_status(user_id, False)
        liste=FollowerDao(DBConnection).get_followers_of_scout(user_id)
        for val in liste:
            res=FollowerDao(DBConnection).unfollow_scout(id_follower=val, id_scout=user_id)
        return "Votre statut éclaireur a été révoqué."

