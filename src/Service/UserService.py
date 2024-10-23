import random

from src.dao.review_dao import ReviewDao
from src.dao.user_dao import UserDao
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

<<<<<<< HEAD
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
        # Vérifier si le mot de passe correspond
        if not self.password_service.validate_password(password, user.password):  # Utiliser validate_password pour comparer
            raise ValueError("Mot de passe incorrect.")
        # On retourne True si l'authentification est réussie donc si le l'utilisateur est bien inscrit.
        return True


def average_rate(title):
    """
    Calcule la note moyenne d'un film en le recherchant par son titre.

    Paramètres:
    -----------
    title : str
        titre du film duquel on veut la note moyenne.

    Returns:
    --------
    str
        Message contenant la note moyenne ou indiquant qu'il n'y a pas d'avis.
    """
    review_dao = ReviewDao()  # Créer une instance de ReviewDao
    review_list = review_dao.get_all_review_by_title(title)  # Appeler sur l'instance

    if not review_list:
        return f"Aucune note disponible pour le film '{title}'."

    total = sum(review.note for review in review_list)
    moy = total / len(review_list)
    return f"La note moyenne de '{title}' est de {moy:.2f}."



def get_review_by_title(title, n=10):
    """
    Récupère aléatoirement les commentaires et notes de n user pour un
    film donné.

    Parametres:
    -----------
    title : str
        titre du film duquel on souhaite voir quelques commentaires et notes.
    n : int
        nombre total de commentaires ou notes que l'on souhaite voir.

    Returns:
    --------
    echantillon_complet : list[dict]
        liste de n dictionnaires avec comme clés id_user, comment et note.
    """
    review_dao = ReviewDao() 
    review_list = review_dao.get_all_review_by_title(title)
    L = []

    for row in review_list:
        id_user = row.id_user
        note = row.note
        comment = row.comment

        # On ne retient seulement les notes et id_user où un commentaire est
        # écrit
        if comment:
            d = {'id_user': id_user, 'note': note, 'comment': comment}
            L.append(d)

    if n > len(L):
        n = len(L)
    # Création d'un échantillon aléatoire de n dictionnaires de L
    echantillon = random.sample(L, n)

    return f"Voici les notes et commentaires de n utilisateurs : {echantillon}"
