import os
import sys

from src.Model.movie_simple import MovieSimple  

def test_initialization():
    """Test de l'initialisation de la classe MovieSimple."""
    movie = MovieSimple(id_local=1, id_tmdb=12345, title="Inception")
    assert movie.id_local == 1
    assert movie.id_tmdb == 12345
    assert movie.title == "Inception"

def test_repr():
    """Test de la représentation textuelle (__repr__) de MovieSimple."""
    movie = MovieSimple(id_local=1, id_tmdb=12345, title="Inception")
    expected_repr = "Movie(id_local=1, id_tmdb=12345, title='Inception')"
    assert repr(movie) == expected_repr
