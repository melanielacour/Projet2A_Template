import pytest
from src.Model.Review import Review, ValidationError


def test_valid_review_creation():
    """Test de création d'une critique valide."""
    review = Review(id_film=1, id_user=42, id_review=101, comment="Amazing movie!", note=9)
    assert review.id_film == 1
    assert review.id_user == 42
    assert review.id_review == 101
    assert review.comment == "Amazing movie!"
    assert review.note == 9


def test_invalid_id_film_type():
    """Test de levée d'une exception si id_film n'est pas un entier."""
    with pytest.raises(ValidationError, match="id_film must be an integer"):
        Review(id_film="1", id_user=42, id_review=101, comment="Good!", note=8)


def test_invalid_id_user_type():
    """Test de levée d'une exception si id_user n'est pas un entier."""
    with pytest.raises(ValidationError, match="id_user must be an integer"):
        Review(id_film=1, id_user="42", id_review=101, comment="Good!", note=8)


def test_invalid_id_review_type():
    """Test de levée d'une exception si id_review n'est pas un entier."""
    with pytest.raises(ValidationError, match="id_review must be an integer"):
        Review(id_film=1, id_user=42, id_review="101", comment="Good!", note=8)


def test_invalid_comment_type():
    """Test de levée d'une exception si comment n'est pas une chaîne."""
    with pytest.raises(ValidationError, match="comment must be a string"):
        Review(id_film=1, id_user=42, id_review=101, comment=123, note=8)


def test_invalid_note_type():
    """Test de levée d'une exception si note n'est pas un entier."""
    with pytest.raises(ValidationError, match="note must be an integer between 0 and 10"):
        Review(id_film=1, id_user=42, id_review=101, comment="Good!", note="8")


def test_invalid_note_range():
    """Test de levée d'une exception si note n'est pas dans la plage [0, 10]."""
    with pytest.raises(ValidationError, match="note must be an integer between 0 and 10"):
        Review(id_film=1, id_user=42, id_review=101, comment="Good!", note=11)


def test_repr_method():
    """Test de la méthode __repr__."""
    review = Review(id_film=1, id_user=42, id_review=101, comment="Nice!", note=8)
    expected_repr = "<Review(id_film=1, id_user=42, id_review=101, comment='Nice!', note=8)>"
    assert repr(review) == expected_repr
