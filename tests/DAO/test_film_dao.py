import pytest
from unittest.mock import MagicMock
from src.Model.film_simple import FilmSimple
from src.dao.movie_dao import MovieDAO

def test_get_local_movie_by_id(mocker):
    # Crée une instance de MovieDAO
    movie_dao = MovieDAO()

    # Mocker DBConnection pour éviter les interactions avec la vraie base de données
    mock_connection = mocker.patch("src.dao.db_connection.DBConnection")
    mock_cursor = MagicMock()
    mock_connection().connection.cursor.return_value.__enter__.return_value = mock_cursor

    # Simuler une ligne de résultat de la base de données
    mock_cursor.fetchone.return_value = {
        "id": 1,
        "id_tmdb": 27205,
        "title": "Inception"
    }

    # Appel de la méthode
    result = movie_dao.get_local_movie_by_id(1)

    # Vérifier le résultat
    assert isinstance(result, FilmSimple)


def test_get_local_movie_by_idtmdb(mocker):
    movie_dao = MovieDAO()

    # Mock de DBConnection
    mock_connection = mocker.patch("src.dao.db_connection.DBConnection")
    mock_cursor = MagicMock()
    mock_connection().connection.cursor.return_value.__enter__.return_value = mock_cursor

    # Simuler une ligne de résultat
    mock_cursor.fetchone.return_value = {
        "id": 1,
        "id_tmdb": 272025,
        "title": "Inception"
    }

    # Appel de la méthode
    result = movie_dao.get_local_movie_by_idtmdb(272025)
    # Vérifier le résultat
    assert isinstance(result, FilmSimple)


def test_add_local_movie(mocker):
    movie_dao = MovieDAO()

    # Mock DBConnection
    mock_connection = mocker.patch("src.dao.db_connection.DBConnection")
    mock_cursor = MagicMock()
    mock_connection().connection.cursor.return_value.__enter__.return_value = mock_cursor

    # Mock de la méthode get_local_movie_by_idtmdb pour simuler qu'aucun film n'existe
    mocker.patch.object(MovieDAO, 'get_local_movie_by_idtmdb', return_value=None)

    # Simuler le retour après l'insertion du film
    mock_cursor.fetchone.return_value = {
        "id": 3,
        "id_tmdb": 67890,
        "title": "New Movie"
    }

    # Appel de la méthode pour ajouter un film
    result = movie_dao.add_local_movie(title="New Movie", id_tmdb=67890)


    assert result == True

