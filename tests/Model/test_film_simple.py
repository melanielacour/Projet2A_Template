import os
import sys

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src.Model.film_simple import FilmSimple


def test_film_simple_constructor_ok():
    film_1 = FilmSimple(id_film=1, id_tmdb=5, title="Split")
    assert film_1.id_film == 1
    assert film_1.id_tmdb == 5
    assert film_1.title == "Split"
