import pytest
from src.Service.MovieService import MovieService
from src.Model.Film import Film

@pytest.fixture
def movie_service():
    """Fixture pour initialiser MovieService."""
    return MovieService()


def test_get_movie_by_title_real(movie_service):
    """Test réel pour obtenir un film par son titre."""
    title = "Inception"
    film = movie_service.get_movie_by_title(title)

    assert isinstance(film, Film)
    assert film.title == "Inception"
    assert film.producer  # Le producteur ne doit pas être une chaîne vide
    assert film.category  # La catégorie ne doit pas être une chaîne vide
    assert film.date == "2010"


def test_get_movies_by_category_real(movie_service):
    """Test réel pour obtenir des films par catégorie."""
    category_id = 28  # Action
    films = movie_service.get_movies_by_category(category_id)

    assert len(films) > 0
    assert isinstance(films[0], Film)
    assert films[0].title  # Le titre ne doit pas être une chaîne vide
    assert films[0].producer  # Le producteur ne doit pas être une chaîne vide
    assert films[0].category == "Action"  # Vérifier que la catégorie correspond à "Action"
    assert films[0].date  # La date de sortie ne doit pas être une chaîne vide


def test_get_movies_by_director_name_real(movie_service):
    """Test réel pour obtenir des films par nom de réalisateur."""
    director_name = "Christopher Nolan"
    films = movie_service.get_movies_by_director_name(director_name)

    assert len(films) > 0
    assert isinstance(films[0], Film)
    assert films[0].title  # Le titre ne doit pas être une chaîne vide
    assert films[0].producer  # Le producteur ne doit pas être une chaîne vide
    assert films[0].category  # La catégorie ne doit pas être une chaîne vide
    assert films[0].date  # La date de sortie ne doit pas être une chaîne vide
