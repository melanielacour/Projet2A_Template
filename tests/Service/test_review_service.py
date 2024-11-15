import pytest
from unittest.mock import MagicMock
from src.Service.review_service import ReviewService
from src.Model.Review import Review

@pytest.fixture
def review_service():
    # Création d'un mock pour le DAO de reviews
    review_dao_mock = MagicMock()
    return ReviewService(review_dao_mock)

def test_search_and_rate_movie_existing_movie(review_service):
    # Mock de la méthode MovieRepo.get_movie_by_id_film
    movie_mock = MagicMock()
    movie_mock.id_local = 1
    review_service.review_dao.get_review_by_id_user_and_id_film.return_value = None  # Aucune critique existante
    
    # Mock pour la méthode add_review de ReviewDao
    review_service.review_dao.add_review.return_value = Review(id_film=1, id_user=1, id_review=1, note=8, comment="Nice movie")

    # Simulation d'une recherche et notation de film
    review = review_service.search_and_rate_movie_existing_movie(id_film=1, id_user=1, note=8, comment="Nice movie")
    
    # Vérification que la méthode add_review a bien été appelée
    review_service.review_dao.add_review.assert_called_once()
    
    # Vérification des valeurs retournées
    assert review.note == 8
    assert review.comment == "Nice movie"
