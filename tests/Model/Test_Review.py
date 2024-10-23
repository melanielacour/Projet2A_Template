import os
import sys
from unittest.mock import MagicMock, patch

import pytest

from src.Model.Review import Review
from src.Service.review_essai import average_rate, get_review_by_title

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))


def test_review_constructor_ok():
    review_1 = Review(id_review=1, id_film=2, id_user=5, comment="Super film", note=7)
    assert review_1.id_review == 1
    assert review_1.id_film == 2
    assert review_1.id_user == 5
    assert review_1.comment == "Super film"
    assert review_1.note == 7




# Test de la fonction average_rate avec des données mockées
@patch('src.dao.review_dao.ReviewDao.get_all_review_by_title')
def test_average_rate(mock_get_all_review_by_title):
    # Simuler une liste de reviews pour un film
    mock_get_all_review_by_title.return_value = [
        MagicMock(note=8.5),
        MagicMock(note=6.8),
        MagicMock(note=7.0)
    ]

    # Appeler la fonction
    result = average_rate("Film A")

    # Vérification du résultat
    assert result == "La note moyenne de 'Film A' est de 7.43.", f"Résultat inattendu : {result}"


# Test de la fonction average_rate avec aucune note disponible
@patch('src.dao.review_dao.ReviewDao.get_all_review_by_title')
def test_average_rate_no_reviews(mock_get_all_review_by_title):
    # Simuler aucun review pour un film
    mock_get_all_review_by_title.return_value = []

    # Appeler la fonction
    result = average_rate("Film Inexistant")

    # Vérification du message d'erreur
    assert result == "Aucune note disponible pour le film 'Film Inexistant'.", f"Résultat inattendu : {result}"

# Test de la fonction get_review_by_title avec des données mockées
@patch('src.dao.review_dao.ReviewDao.get_all_review_by_title')
def test_get_review_by_title(mock_get_all_review_by_title):
    # Simuler une liste de reviews avec des commentaires pour un film
    mock_get_all_review_by_title.return_value = [
        MagicMock(id_user=1, note=8.0, comment="Très bon film"),
        MagicMock(id_user=2, note=7.5, comment="Bon film"),
        MagicMock(id_user=3, note=6.0, comment="Pas mal"),
        MagicMock(id_user=4, note=5.5, comment="Peut mieux faire")
    ]

    # Appeler la fonction pour un échantillon de 3 commentaires
    result = get_review_by_title("Film A", n=3)

    # Vérification que le résultat contient exactement 3 éléments
    assert len(result) == 3, f"Le nombre d'échantillons devrait être 3 mais c'est : {len(result)}"

    # Vérification du contenu de chaque élément
    for r in result:
        assert 'id_user' in r
        assert 'note' in r
        assert 'comment' in r


# Test de la fonction get_review_by_title avec moins de n commentaires disponibles
@patch('src.dao.review_dao.ReviewDao.get_all_review_by_title')
def test_get_review_by_title_less_than_n(mock_get_all_review_by_title):
    # Simuler une liste avec seulement 2 reviews
    mock_get_all_review_by_title.return_value = [
        MagicMock(id_user=1, note=8.0, comment="Très bon film"),
        MagicMock(id_user=2, note=7.5, comment="Bon film")
    ]

    # Appeler la fonction en demandant 5 commentaires (mais seulement 2 disponibles)
    result = get_review_by_title("Film B", n=5)

    # Vérification que le résultat contient les 2 commentaires disponibles
    assert len(result) == 2, f"Le nombre d'échantillons devrait être 2 mais c'est : {len(result)}"

    # Vérification du contenu de chaque élément
    for r in result:
        assert 'id_user' in r
        assert 'note' in r
        assert 'comment' in r


# Test de la fonction get_review_by_title avec aucun commentaire
@patch('src.dao.review_dao.ReviewDao.get_all_review_by_title')
def test_get_review_by_title_no_reviews(mock_get_all_review_by_title):
    # Simuler aucun commentaire pour un film
    mock_get_all_review_by_title.return_value = []

    # Appeler la fonction
    result = get_review_by_title("Film C", n=5)

    # Vérification que la liste retournée est vide
    assert len(result) == 0, f"Le résultat devrait être vide, mais contient : {len(result)}"