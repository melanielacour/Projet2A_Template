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
            titre du film duquel on souhaite voir quelques commentaires
            et notes.
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

            # On ne retient seulement les notes et id_user où un commentaire
            # est écrit
            if comment:
                d = {'id_user': id_user, 'note': note, 'comment': comment}
                L.append(d)

        if n > len(L):
            n = len(L)
        # Création d'un échantillon aléatoire de n dictionnaires de L
        echantillon = random.sample(L, n)

        return f"Notes et commentaires de n utilisateurs : {echantillon}"
