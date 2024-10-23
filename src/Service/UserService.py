import random

from src.dao.review_dao import ReviewDao
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

    def register_user(self, pseudo: str, password: str, is_scout: bool = False) -> str:
        """
        Inscrit un nouvel utilisateur avec un identifiant unique et un mot de
        passe sécurisé.

        Paramètres:
        -----------
        pseudo : str
            Le pseudo de l'utilisateur.
        password : str
            Le mot de passe de l'utilisateur.
        is_scout : bool, optional
            Indique si l'utilisateur est un éclaireur (scout).
            Par défaut, False.

        Retourne:
        ---------
        str
            Message de confirmation si l'utilisateur est inscrit avec succès.

        Lève:
        -----
        ValueError:
            Si l'identifiant est déjà utilisé ou si le mot de passe ne
            respecte pas les règles.
        """
        # Vérifier si l'utilisateur existe déjà
        if self.user_dao.get_user_by_pseudo(pseudo):
            raise ValueError("Cet identifiant est déjà utilisé.")  # Lever l'exception correctement

        # Valider le mot de passe
        if not self.password_service.validate_password(password):
            raise ValueError("Le mot de passe doit comporter au moins une majuscule, une minuscule et un chiffre.")

        # Créer le nouvel utilisateur dans la base de données
        user_cree = self.user_dao.create_user(pseudo=pseudo, is_scout=is_scout, pswd=password)

        if user_cree:
            return "Vous êtes bien inscrit !"
        else:
            raise ValueError("Erreur lors de l'inscription de l'utilisateur.")



    def log_in(self, pseudo: str, password: str) -> bool:

        # Récupérer l'utilisateur par son pseudo
        user = self.user_dao.get_user_by_pseudo(pseudo)

        # Vérifier si l'utilisateur existe
        if not user:
            raise ValueError("Identifiant incorrect.")

        # Vérifier si le mot de passe correspond, utiliser validate_password pour comparer
        if not self.password_service.validate_password(password, user.password):
            raise ValueError("Mot de passe incorrect.")

        return True


def average_rate(title):
    """
    Calcule la note moyenne d'un film en le recherchant par son titre.

    Parametres:
    -----------
    title : str
        titre du film duquel on veut la note moyenne.

    Returns:
    --------
    moy : float
        moyenne du film.
    """
    review_list = ReviewDao.get_all_review_by_title(title)
    L = []

    for row in review_list:
        note = row.note

        if note:
            L.append({'note': note})

    n = len(L)

    # Si L est vide on relève une erreur
    if n == 0:
        return f"Aucune note disponible pour le film '{title}'."

    # Calcul de la somme des notes
    somme = sum(d['note'] for d in L)

    # Calcul de la moyenne
    moy = somme / n

    # On limite le calcule de la moyenne à deux chiffres après la virgule
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
    review_list = ReviewDao.get_all_review_by_title(title)
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
