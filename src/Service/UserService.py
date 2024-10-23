from src.dao.user_dao import UserDao
from src.Service.PasswordService import PasswordService


class UserService:
    def __init__(self, user_dao: UserDao, password_service: PasswordService):
        """
        Initialise le service avec un UserDAO pour gérer les données des utilisateurs
        et un PasswordService pour valider les mots de passe.

        Paramètres:
        -----------
        user_dao : UserDao
            DAO pour interagir avec les données des utilisateurs dans la base de données.
        password_service : PasswordService
            Service utilisé pour valider les mots de passe.
        """
        self.user_dao = user_dao
        self.password_service = password_service

    def register_user(self, pseudo: str, password: str, is_scout: bool = False) -> bool:
        """
        Inscrit un nouvel utilisateur avec un identifiant unique et un mot de passe sécurisé.
        
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
        bool
            True si l'utilisateur est inscrit avec succès, sinon False.
        
        Lève:
        -----
        ValueError:
            Si l'identifiant est déjà utilisé ou si le mot de passe ne respecte pas les règles.
        """
        # Vérifier si l'utilisateur existe déjà
        if self.user_dao.get_user_by_pseudo(pseudo):
            raise ValueError("Cet identifiant est déjà utilisé.")

        # Valider le mot de passe
        if not self.password_service.validate_password(password):
            raise ValueError("Le mot de passe doit comporter au moins une majuscule, une minuscule et un chiffre.")

        # Créer le nouvel utilisateur dans la base de données
        return self.user_dao.create_user(pseudo=pseudo, is_scout=is_scout, pswd=password)

    def log_in(self, pseudo: str, password: str) -> bool:
        """
        Permet à un utilisateur de se connecter en vérifiant le pseudo et le mot de passe.

        Paramètres:
        -----------
        pseudo : str
            L'identifiant de l'utilisateur.
        password : str
            Le mot de passe de l'utilisateur.

        Retourne:
        ---------
        bool
            True si la connexion est réussie, sinon False.

        Lève:
        -----
        ValueError:
            Si le pseudo ou le mot de passe est incorrect.
        """
        # Récupérer l'utilisateur par son pseudo
        user = self.user_dao.get_user_by_pseudo(pseudo)

        # Vérifier si l'utilisateur existe et si le mot de passe correspond
        if not user:
            raise ValueError("Identifiant incorrect.")
        
        if user.pswd != password:
            raise ValueError("Mot de passe incorrect.")

        return True
