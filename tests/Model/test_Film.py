import pytest
from pydantic_core import ValidationError

from src.Model.Film import Film


class TestFilm:

    def test_film_constructor_ok(self):
        film = Film(id_film=1, id_tmdb=12345, title="Inception", producer="Christopher Nolan", category="Science Fiction", date="2010-07-16")
        assert film.id_film == 1
        assert film.id_tmdb == 12345
        assert film.title == "Inception"
        assert film.producer == "Christopher Nolan"
        assert film.category == "Science Fiction"
        assert film.date == "2010-07-16"
        assert film.average_rate == 0.0
        assert film.ratings == []

    def test_add_rating_valid(self):
        """Test l'ajout d'une note valide."""
        film = Film(id_film=1, id_tmdb=12345, title="Inception", producer="Christopher Nolan", category="Science Fiction", date="2010-07-16")
        film.add_rating(8)
        assert film.ratings == [8]
        assert film.average_rate == 8.0
        film.add_rating(10)
        assert film.ratings == [8, 10]
        assert film.average_rate == 9.0
        film.add_rating(6)
        assert film.ratings == [8, 10, 6]
        assert film.average_rate == 8.0

    def test_calculation_mean_no_ratings(self):
        """Test le calcul de la moyenne sans notes."""
        film = Film(id_film=1, id_tmdb=12345, title="Inception", producer="Christopher Nolan", category="Science Fiction", date="2010-07-16")
        assert film.calculation_mean() is None

    def test_add_rating_invalid(self):
        """Test l'ajout d'une note invalide."""
        film = Film(id_film=1, id_tmdb=12345, title="Inception", producer="Christopher Nolan", category="Science Fiction", date="2010-07-16")

        with pytest.raises(ValueError) as excinfo:
            film.add_rating(0)
        assert "la note doit etre comprise entre 1 et 10" in str(excinfo.value)

        with pytest.raises(ValueError) as excinfo:
            film.add_rating(11)
        assert "la note doit etre comprise entre 1 et 10" in str(excinfo.value)

    def test_calculation_mean_with_ratings(self):
        """Test le calcul de la moyenne avec des notes."""
        film = Film(id_film=1, id_tmdb=12345, title="Inception", producer="Christopher Nolan", category="Science Fiction", date="2010-07-16")
        
        film.add_rating(5)
        film.add_rating(7)
        film.add_rating(9)
        assert film.calculation_mean() == 7.0



def test_movie_constructor_ok():
    the_shining = Film(id_film=12, id_tmdb=100, title="The Shining", producer="Stanley Kubrick", category="Horror", date="1980-05-23")
    assert the_shining.id_film == 12
    assert the_shining.title == "The Shining"

def test_film_constructor_throws_on_incorrect_input(): 
    with pytest.raises(ValueError, match="id_film must be an integer, unable to parse string as an integer"):
        Film(id_film="Twelve", id_tmdb=100, title="Dracula", producer="Bram Stoker", category="Horror", date="1897-05-26")