import random
from unittest.mock import Mock

import pytest

from src.Model.Review import Review
from src.Service.reviewService import (add_review, delete_comment,
                                     delete_review,modify_review,
                                     modify_comment,modify_note)

@pytest.fixture
def mock_review_dao():
    """
    Fixture pour fournir un mock de la DAO ReviewDAO.
    """
    mock_dao = Mock()
    return mock_dao


def test_add_review_success(mock_review_dao):
    # Aucun commentaire existant, on simule une note et un commentaire valides
    mock_review_dao.get_review_by_id_user_and_id_film.return_value = None
    mock_review_dao.add_review.return_value = True

    # Appel de la méthode add_review avec un id_user, id_film et un commentaire
    result = add_review(mock_review_dao, id_user=1, id_film=1, comment="Très bon film", note=8)

    # Vérifier que l'ajout est réussi et les bonnes méthodes sont appelées
    assert result == True
    mock_review_dao.get_review_by_id_user_and_id_film.assert_called_once_with(1, 1)
    mock_review_dao.add_review.assert_called_once()


def test_add_review_already_exists(mock_review_dao):
    # Un commentaire existant est trouvé
    existing_review = Review(id_review=1, id_user=1, id_film=1, comment="Déjà commenté", note=7)
    mock_review_dao.get_review_by_id_user_and_id_film.return_value = existing_review

    # Tenter d'ajouter un avis alors qu'un avis existe déjà
    result = add_review(mock_review_dao, id_user=1, id_film=1, comment="Un autre avis", note=9)

    # L'ajout doit échouer et retourner False
    assert result == False
    mock_review_dao.get_review_by_id_user_and_id_film.assert_called_once_with(1, 1)
    mock_review_dao.add_review.assert_not_called()


def test_add_review_invalid_note(mock_review_dao):
    # Vérifier qu'une ValueError est levée pour une note invalide
    with pytest.raises(ValueError, match="La note n'est pas comprise entre 1 et 10"):
        add_review(mock_review_dao, id_user=1, id_film=1, comment="Avis", note=11)

    with pytest.raises(ValueError, match="La note n'est pas comprise entre 1 et 10"):
        add_review(mock_review_dao, id_user=1, id_film=1, comment="Avis", note=0)

    # Vérifier que la DAO n'a pas été appelée pour ces cas
    mock_review_dao.get_review_by_id_user_and_id_film.assert_not_called()
    mock_review_dao.add_review.assert_not_called()