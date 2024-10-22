import os
import sys

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src.Model.Review import Review


def test_review_constructor_ok():
    review_1 = Review(id_review=1, id_film=2, id_user=5, review="Super film")
    assert review_1.id_review == 1
    assert review_1.id_film == 2
    assert review_1.id_user == 5
    assert review_1.review == "Super film"

