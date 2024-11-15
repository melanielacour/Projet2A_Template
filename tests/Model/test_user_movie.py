import pytest
from src.Model.user_movie import UserMovie  # Remplacez `your_module` par le nom de votre fichier contenant `UserMovie`.

def test_usermovie_initialization():
    """Test de l'initialisation réussie de la classe UserMovie avec des valeurs valides."""
    user_movie = UserMovie(id_user=1, id_film=101, status="watched")
    assert user_movie.id_user == 1
    assert user_movie.id_film == 101
    assert user_movie.status == "watched"

def test_usermovie_id_user_invalid_type():
    """Test de l'erreur de type si id_user n'est pas un entier."""
    with pytest.raises(TypeError):
        UserMovie(id_user="abc", id_film=101, status="watched")

def test_usermovie_id_film_invalid_type():
    """Test de l'erreur de type si id_film n'est pas un entier."""
    with pytest.raises(TypeError):
        UserMovie(id_user=1, id_film="xyz", status="watched")

def test_usermovie_status_invalid_value():
    """Test de l'erreur de type si status n'est pas une chaîne de caractères."""
    with pytest.raises(ValueError):
        UserMovie(id_user=1, id_film=101, status=123)

def test_usermovie_repr():
    """Test de la méthode __repr__ pour vérifier la sortie attendue."""
    user_movie = UserMovie(id_user=1, id_film=101, status="watched")
    assert repr(user_movie) == "UserMovie(id_user=1, id_film=101, status='watched')"
