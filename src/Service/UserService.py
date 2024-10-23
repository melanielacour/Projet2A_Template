from src.dao.user_dao import UserDao
from src.Service.PasswordService import PasswordService


class UserService:
    def __init__(self, user_dao: UserDao, password_service: PasswordService):
        """
        Cette méthode Initialise le service avec un UserDAO pour gérer les données des utilisateurs
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



    def register_user(self, pseudo: str, password: str, is_scout: bool = False) -> str:
        """
        Cette méthode permet de créer un nouvel utilisateur en vérifiant d'abord si le pseudo est déjà pris et en validant les conditions du mot de passe.        
        
        Paramètres:
        -----------
        pseudo : str
            Le pseudo de l'utilisateur.
        password : str
            Le mot de passe de l'utilisateur.
        is_scout : bool
            Indique si l'utilisateur est un éclaireur (scout), qui prend par défaut False.
    
        Retourne:
        ---------
        str
            Message de confirmation si l'utilisateur est inscrit avec succès.
        """

        # On vérifie si l'utilisateur existe déjà, si c'est déja le cas on retourne une exception de type ValueError avec un message indiquant que pseudo est déjà utilisé.
        if self.user_dao.get_user_by_pseudo(pseudo):
            raise ValueError("Cet identifiant est déjà utilisé.")

        # On verifie si le mot de passe respecte les conditions (longueur, minuscules, majuscules). 
        if not self.password_service.validate_password(password):
            raise ValueError("Le mot de passe doit comporter au moins une majuscule, une minuscule et un chiffre.")

        # On va créer un nouvel utilisateur dans la base de données avec les informations fournis. 
        user_cree = self.user_dao.create_user(pseudo=pseudo, is_scout=is_scout, pswd=password)
        # Cela renverra un message de confirmation à l'utilisateur s' il a reussi son incription. 
        if user_cree:
            return "Vous êtes bien inscrit !"
        else:
            raise ValueError("Erreur lors de l'inscription de l'utilisateur.")



    def log_in(self, pseudo: str, password: str) -> bool:
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
        user = self.user_dao.get_user_by_pseudo(pseudo)

        # On Vérifie si l'utilisateur existe et si le mot de passe fourni est correct.
        if not user:
            raise ValueError("Identifiant incorrect.")
        if not self.password_service.validate_password(password, user.password):  # Utiliser validate_password pour comparer
            raise ValueError("Mot de passe incorrect.")
        # On retourne True si l'authentification est réussie donc si le l'utilisateur est bien inscrit. 
        return True
