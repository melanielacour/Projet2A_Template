import pytest
from src.Model.Movie import Movie, ValidationError  # Remplacez `your_module` par le nom de votre fichier contenant `Movie`.

def test_movie_initialization():
    """Test de l'initialisation réussie de la classe Movie avec des valeurs valides."""
    movie = Movie(id_film=1, id_tmdb=100, title="Inception", producer="Christopher Nolan", category="Sci-Fi", date="2010-07-16")
    assert movie.id_film == 1
    assert movie.id_tmdb == 100
    assert movie.title == "Inception"
    assert movie.producer == "Christopher Nolan"
    assert movie.category == "Sci-Fi"
    assert movie.date == "2010-07-16"

def test_movie_id_film_invalid_type():
    """Test de l'erreur de validation si id_film n'est pas un entier."""
    with pytest.raises(ValueError, match="id_film must be an integer"):
        Movie(id_film="abc", id_tmdb=100, title="Inception", producer="Christopher Nolan", category="Sci-Fi", date="2010-07-16")

def test_movie_id_tmdb_invalid_type():
    """Test de l'erreur de validation si id_tmdb n'est pas un entier."""
    with pytest.raises(ValueError, match="id_tmdb must be an integer"):
        Movie(id_film=1, id_tmdb="xyz", title="Inception", producer="Christopher Nolan", category="Sci-Fi", date="2010-07-16")
