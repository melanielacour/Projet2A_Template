import random

from src.dao.review_dao import ReviewDao


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
    review_dao = ReviewDao()
    review_list = review_dao.get_all_review_by_title(title)
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

    return echantillon
