from src.dao.user_dao import UserDao
from src.Service.PasswordService import PasswordService


class UserService:
    def register_user(self, pseudo: str, password: str, is_scout: bool = False) -> str:
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




    def log_in(self, pseudo: str, password: str) -> bool:

    # Récupérer l'utilisateur par son pseudo
        user = UserDao().get_user_by_pseudo(pseudo)

    # Vérifier si l'utilisateur existe
        if not user:
            raise ValueError("Identifiant incorrect.")

    # Vérifier si le mot de passe correspond
        if not self.password_service.validate_password(password, user.password):  # Utiliser validate_password pour comparer
            raise ValueError("Mot de passe incorrect.")

        return True
