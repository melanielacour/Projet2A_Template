import os

from src.dao.user_dao import UserDao
from src.Service.JWTService import JwtService
from src.Service.PasswordService import PasswordService


class UserService:
    def register_user(self, pseudo: str, password: str, is_scout: bool = False) -> str:
        """
        Cette méthode Initialise le service avec un UserDAO pour gérer les données des utilisateurs
        et un PasswordService pour valider les mots de passe.

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
        if UserDao().get_user_by_pseudo(pseudo):
            raise ValueError("Cet identifiant est déjà utilisé.")

        # Valider la force du mot de passe
        pswd_ser = PasswordService()

        # Cette méthode lève une exception si le mot de passe est invalide
        pswd_ser.check_password_strength(password)

        # Hacher le mot de passe avant de l'enregistrer
        hashed_password = pswd_ser.hash_password(password)

        # Créer le nouvel utilisateur dans la base de données avec le mot de passe haché
        user_cree = UserDao().create_user(pseudo=pseudo, is_scout=is_scout, pswd=hashed_password)


        if user_cree:
            return "Vous êtes bien inscrit !"
        else:
            raise ValueError("Erreur lors de l'inscription de l'utilisateur.")




    def log_in(self, pseudo: str, password: str) -> dict:

    # Récupérer l'utilisateur par son pseudo
        user = UserDao().get_user_by_pseudo(pseudo)
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
        bool
            True si l'authentification est réussit, sinon on lève une exception.
        """

        # On récupère le pseudo de l'utilisateur
        user = UserDao().get_user_by_pseudo(pseudo)

        # On Vérifie si l'utilisateur existe et si le mot de passe fourni est correct.
        if not user:
            raise ValueError("Identifiant incorrect.")
        # Vérifier si le mot de passe correspond au pseudo
        if not PasswordService().validate_pseudo_password(pseudo, password):  # Utiliser validate_password pour comparer
            raise ValueError("Mot de passe incorrect.")
<<<<<<< HEAD
        # On retourne True si l'authentification est réussie donc si le l'utilisateur est bien inscrit.
        return True
<<<<<<< HEAD
=======

>>>>>>> 455843ac32d54422f97696732b59958562669d89
=======

        # générer un token JWT
        jwt_response = JwtService(os.environ["JWT_SECRET"], "HS256").encode_jwt(user.id_user)

        # Retourner la réponse avec True et le token
        return {"success": True, "token": jwt_response.access_token}
>>>>>>> ee77daef1f0eba5d0dad5d81977816770759b696
