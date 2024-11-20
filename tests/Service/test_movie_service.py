import pytest
from unittest.mock import MagicMock
from src.Service.MovieService import MovieService
from src.Model.Movie import Movie

@pytest.fixture
def movie_service():
    return MovieService()

def test_get_category_id(movie_service):
    assert movie_service.get_category_id("action") == 28
    assert movie_service.get_category_id("comédie") == 35
    assert movie_service.get_category_id("inexistant") is None

def test_get_movie_by_id_success(mocker, movie_service):
    mock_response = {
        "id": 123,
        "title": "Inception",
        "production_companies": [{"name": "Warner Bros"}],
        "genres": [{"name": "Science-Fiction"}],
        "release_date": "2010-07-16"
    }
    mocker.patch("requests.get", return_value=MagicMock(status_code=200, json=lambda: mock_response))

    movie = movie_service.get_movie_by_id("123")
    assert isinstance(movie, Movie)
    assert movie.id_film == 123
    assert movie.title == "Inception"
    assert movie.producer == "Warner Bros"
    assert movie.category == "Science-Fiction"
    assert movie.date == "2010"

def test_get_movie_by_id_failure(mocker, movie_service):
    mocker.patch("requests.get", return_value=MagicMock(status_code=404))

    with pytest.raises(Exception, match="Erreur lors de la récupération des détails : 404"):
        movie_service.get_movie_by_id("999")


import pytest
from unittest.mock import MagicMock

def test_get_movie_by_title_success(mocker, movie_service):
    mock_search_response = {
        "results": [
            {"id": 1, "title": "Inception"},
            {"id": 2, "title": "Interstellar"}
        ]
    }
    mock_details_response_1 = {
        "id": 1,
        "title": "Inception",
        "production_companies": [{"name": "Warner Bros"}],
        "genres": [{"name": "Science-Fiction"}],
        "release_date": "2010-07-16"
    }
    mock_details_response_2 = {
        "id": 2,
        "title": "Interstellar",
        "production_companies": [{"name": "Paramount Pictures"}],
        "genres": [{"name": "Science-Fiction"}],
        "release_date": "2014-11-07"
    }

    # Simuler les appels à `requests.get`
    mocker.patch("requests.get", side_effect=[
        MagicMock(status_code=200, json=lambda: mock_search_response),
        MagicMock(status_code=200, json=lambda: mock_details_response_1),
        MagicMock(status_code=200, json=lambda: mock_details_response_2)
    ])

    # Exécuter la méthode et vérifier les résultats
    movies = movie_service.get_movie_by_title("Inception")
    
    assert len(movies) == 2
    assert movies[0].title == "Inception"
    assert movies[1].title == "Interstellar"

   

def test_get_movie_by_title_no_results(mocker, movie_service):
    mock_search_response = {"results": []}
    mocker.patch("requests.get", return_value=MagicMock(status_code=200, json=lambda: mock_search_response))

    with pytest.raises(Exception, match="Aucun film trouvé."):
        movie_service.get_movie_by_title("Film Inexistant")

def test_get_movies_by_category_success(mocker, movie_service):
    mock_category_response = {
        "results": [{"id": 3, "title": "Avatar"}]
    }
    mock_details_response = {
        "id": 3,
        "title": "Avatar",
        "production_companies": [{"name": "20th Century Fox"}],
        "genres": [{"name": "Science-Fiction"}],
        "release_date": "2009-12-18"
    }
    mocker.patch("requests.get", side_effect=[
        MagicMock(status_code=200, json=lambda: mock_category_response),
        MagicMock(status_code=200, json=lambda: mock_details_response)
    ])

    movies = movie_service.get_movies_by_category(28)
    assert len(movies) == 1
    assert movies[0].title == "Avatar"
    assert movies[0].producer == "20th Century Fox"

def test_get_movies_by_category_failure(mocker, movie_service):
    mocker.patch("requests.get", return_value=MagicMock(status_code=404))

    with pytest.raises(Exception, match="Erreur lors de la récupération des films par catégorie : 404"):
        movie_service.get_movies_by_category(28)

def test_get_movies_by_director_success(mocker, movie_service):
    mock_director_response = {
        "results": [{"id": 4, "title": "The Dark Knight"}]
    }
    mock_details_response = {
        "id": 4,
        "title": "The Dark Knight",
        "production_companies": [{"name": "Warner Bros"}],
        "genres": [{"name": "Action"}],
        "release_date": "2008-07-18"
    }
    mocker.patch("requests.get", side_effect=[
        MagicMock(status_code=200, json=lambda: mock_director_response),
        MagicMock(status_code=200, json=lambda: mock_details_response)
    ])

    movies = movie_service.get_movies_by_director(525)
    assert len(movies) == 1
    assert movies[0].title == "The Dark Knight"

def test_get_movies_by_director_name_success(mocker, movie_service):
    mock_search_response = {"results": [{"id": 525, "name": "Christopher Nolan"}]}
    mock_director_movies_response = {
        "results": [{"id": 4, "title": "The Dark Knight"}]
    }
    mock_details_response = {
        "id": 4,
        "title": "The Dark Knight",
        "production_companies": [{"name": "Warner Bros"}],
        "genres": [{"name": "Action"}],
        "release_date": "2008-07-18"
    }
    mocker.patch("requests.get", side_effect=[
        MagicMock(status_code=200, json=lambda: mock_search_response),
        MagicMock(status_code=200, json=lambda: mock_director_movies_response),
        MagicMock(status_code=200, json=lambda: mock_details_response)
    ])

    movies = movie_service.get_movies_by_director_name("Christopher Nolan")
    assert len(movies) == 1
    assert movies[0].title == "The Dark Knight"

def test_get_movies_by_director_name_no_results(mocker, movie_service):
    mock_search_response = {"results": []}
    mocker.patch("requests.get", return_value=MagicMock(status_code=200, json=lambda: mock_search_response))

    with pytest.raises(Exception, match="Aucun réalisateur trouvé."):
        movie_service.get_movies_by_director_name("Réalisateur Inconnu")
