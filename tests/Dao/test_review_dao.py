import pytest
from unittest.mock import MagicMock, patch
from src.dao.review_dao import ReviewDao
from src.Model.Review import Review


@pytest.fixture
def db_connection_mock():
    """Fixture pour mocker la connexion à la base de données."""
    db_conn = MagicMock()
    db_conn.connection.return_value.__enter__.return_value.cursor.return_value = MagicMock()
    return db_conn


@pytest.fixture
def review_dao(db_connection_mock):
    """Fixture pour initialiser ReviewDao avec une connexion mockée."""
    return ReviewDao(db_connection=db_connection_mock)


def test_get_all_review_by_id(review_dao, db_connection_mock):
    """Test de la méthode get_all_review_by_id."""
    # Mock des données retournées par la base de données
    db_connection_mock.connection().__enter__().cursor().__enter__().fetchall.return_value = [
        {"id_review": 1, "id_film": 10, "id_user": 5, "comment": "Great movie!", "rating": 9},
        {"id_review": 2, "id_film": 10, "id_user": 6, "comment": "Not bad", "rating": 7},
    ]

    reviews = review_dao.get_all_review_by_id(10)

    # Vérification des résultats
    assert len(reviews) == 2
    assert reviews[0].id_review == 1
    assert reviews[0].comment == "Great movie!"
    assert reviews[0].note == 9


def test_add_review(review_dao, db_connection_mock):
    """Test de la méthode add_review."""
    # Mock pour simuler qu'il n'existe pas encore de critique
    review_dao.get_review_by_id_user_and_id_film = MagicMock(return_value=None)

    # Mock des résultats de l'insertion
    db_connection_mock.connection().__enter__().cursor().__enter__().fetchone.return_value = {"id_review": 3}

    new_review = Review(id_review=None, id_film=10, id_user=5, comment="Amazing!", note=8)
    added_review = review_dao.add_review(new_review)

    # Vérification de la critique ajoutée
    assert added_review.id_review == 3
    assert added_review.comment == "Amazing!"
    assert added_review.note == 8


def test_delete_review(review_dao, db_connection_mock):
    """Test de la méthode delete_review."""
    # Mock pour simuler l'existence d'une critique
    review_dao.get_review_by_id_user_and_id_film = MagicMock(
        return_value=Review(id_review=1, id_film=10, id_user=5, comment="Great!", note=9)
    )

    result = review_dao.delete_review(5, 10)

    # Vérification de la suppression
    assert result is True
    review_dao.get_review_by_id_user_and_id_film.assert_called_once_with(10, 5)
    db_connection_mock.connection().__enter__().cursor().__enter__().execute.assert_called_once()


def test_update_review(review_dao, db_connection_mock):
    """Test de la méthode update_review."""
    review_to_update = Review(id_review=1, id_film=10, id_user=5, comment="Updated comment", note=8)

    updated_review = review_dao.update_review(review_to_update)

    # Vérification de la mise à jour
    assert updated_review.comment == "Updated comment"
    assert updated_review.note == 8
    db_connection_mock.connection().__enter__().cursor().__enter__().execute.assert_called_once()


def test_get_all_reviews_by_user_id(review_dao, db_connection_mock):
    """Test de la méthode get_all_reviews_by_user_id."""
    # Mock des données retournées par la base de données
    db_connection_mock.connection().__enter__().cursor().__enter__().fetchall.return_value = [
        {"id_review": 1, "id_film": 10, "id_user": 5, "comment": "Great movie!", "rating": 9},
        {"id_review": 2, "id_film": 20, "id_user": 5, "comment": "Amazing story", "rating": 10},
    ]

    reviews = review_dao.get_all_reviews_by_user_id(5)

    # Vérification des résultats
    assert len(reviews) == 2
    assert reviews[0].id_review == 1
    assert reviews[0].id_film == 10
    assert reviews[1].comment == "Amazing story"
    assert reviews[1].note == 10
