import pytest
from unittest.mock import MagicMock
from src.dao.review_dao import ReviewDao
from src.Model.review import Review

@pytest.fixture
def review_dao():
    return ReviewDao()

def test_get_all_review_by_id(mocker, review_dao):
    # Mock de DBConnection
    mock_connection = mocker.patch("src.dao.db_connection.DBConnection")
    mock_cursor = MagicMock()
    mock_connection().connection.cursor.return_value.__enter__.return_value = mock_cursor

    # Simuler le retour de plusieurs lignes de résultat
    mock_cursor.fetchall.return_value = [
        {"id_review": 1, "id_film": 101, "id_user": 202, "comment": "Great movie!", "rating": 5},
        {"id_review": 2, "id_film": 101, "id_user": 203, "comment": "Not bad", "rating": 3},
    ]

    result = review_dao.get_all_review_by_id(101)

    # Vérifier les résultats
    assert len(result) == 2
    assert isinstance(result[0], Review)
    assert result[0].id_review == 1
    assert result[0].note == 5

def test_get_all_review_by_title(mocker, review_dao):
    # Mock de DBConnection
    mock_connection = mocker.patch("src.dao.db_connection.DBConnection")
    mock_cursor = MagicMock()
    mock_connection().connection.cursor.return_value.__enter__.return_value = mock_cursor

    # Simuler le retour de plusieurs lignes de résultat
    mock_cursor.fetchall.return_value = [
        {"id_review": 1, "id_film": 101, "id_user": 202, "comment": "Amazing!", "rating": 4, "title": "Inception"},
    ]

    result = review_dao.get_all_review_by_title("Inception")

    # Vérifier les résultats
    assert len(result) == 1
    assert isinstance(result[0], Review)
    assert result[0].comment == "Amazing!"

def test_get_review_by_id_user_and_id_film(mocker, review_dao):
    # Mock de DBConnection
    mock_connection = mocker.patch("src.dao.db_connection.DBConnection")
    mock_cursor = MagicMock()
    mock_connection().connection.cursor.return_value.__enter__.return_value = mock_cursor

    # Simuler une ligne de résultat
    mock_cursor.fetchone.return_value = {
        "id_review": 1, "id_film": 101, "id_user": 202, "comment": "Good movie", "rating": 4
    }

    result = review_dao.get_review_by_id_user_and_id_film(101, 202)

    # Vérifier les résultats
    assert isinstance(result, Review)
    assert result.id_film == 101
    assert result.id_user == 202
    assert result.note == 4

def test_add_comment(mocker, review_dao):
    # Mock de DBConnection
    mock_connection = mocker.patch("src.dao.db_connection.DBConnection")
    mock_cursor = MagicMock()
    mock_connection().connection.cursor.return_value.__enter__.return_value = mock_cursor

    # Simuler le retour de l'ID de la nouvelle critique
    mock_cursor.fetchone.return_value = {"id_review": 1}

    # Créer une critique de test
    review = Review(id_review=1, id_film=101, id_user=202, comment="Loved it!", note=5)

    result = review_dao.add_comment(review)

    # Vérifier que la critique a été ajoutée correctement
    assert isinstance(result, Review)
    assert result.comment == "Loved it!"
    assert result.note == 5

def test_delete_review_success(mocker, review_dao):
    # Mock de DBConnection
    mock_connection = mocker.patch("src.dao.db_connection.DBConnection")
    mock_cursor = MagicMock()
    mock_connection().connection.cursor.return_value.__enter__.return_value = mock_cursor

    # Simuler le retour de get_review_by_id_user_and_id_film
    mock_get_review = mocker.patch.object(review_dao, "get_review_by_id_user_and_id_film")
    mock_get_review.return_value = Review(id_review=1, id_film=101, id_user=202, comment="Good movie", note=4)

    result = review_dao.delete_review(202, 101)

    # Vérifier que la méthode a bien renvoyé True
    assert result is True
    mock_cursor.execute.assert_called_once_with(
        "DELETE FROM projet_2a.review  WHERE id_user = %(id_user)s AND id_film = %(id_film)s; ",
        {
            "id_user": 202,
            "id_film": 101
        }
    )

def test_delete_review_not_found(mocker, review_dao):
    # Mock de DBConnection
    mock_connection = mocker.patch("src.dao.db_connection.DBConnection")
    mock_cursor = MagicMock()
    mock_connection().connection.cursor.return_value.__enter__.return_value = mock_cursor

    # Simuler l'absence de résultat de la méthode get_review_by_id_user_and_id_film
    mock_get_review = mocker.patch.object(review_dao, "get_review_by_id_user_and_id_film")
    mock_get_review.return_value = None

    result = review_dao.delete_review(202, 101)

    # Vérifier que la méthode a bien renvoyé False
    assert result is False
    mock_cursor.execute.assert_not_called()
