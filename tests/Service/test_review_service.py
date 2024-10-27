import unittest
from unittest.mock import MagicMock
from src.dao.review_dao import ReviewDao
from src.Model.Review import Review
from src.Service.review_service import ReviewService


class TestReviewService(unittest.TestCase):

    def setUp(self):
        # Créez un mock de ReviewDao
        self.review_dao = MagicMock(spec=ReviewDao)
        self.review_service = ReviewService(self.review_dao)

    def test_search_and_rate_movie_new_review(self):
        # Configurer le mock pour retourner None pour une nouvelle critique
        self.review_dao.get_review_by_id_user_and_id_film.return_value = None

        # Appeler la méthode pour ajouter une nouvelle critique
        review = self.review_service.search_and_rate_movie(1, 1, 8, "Good movie")

        # Vérifier que la méthode add_review a été appelée
        self.review_dao.add_review.assert_called_once()
        self.assertIsNotNone(review)

    def test_delete_review(self):
        # Configurer une critique existante
        self.review_dao.get_review_by_id_user_and_id_film.return_value = Review(
            id_review=1, id_film=1, id_user=1, note=8, comment="Good movie"
        )

        # Appeler la méthode pour supprimer la critique
        result = self.review_service.delete_review(1, 1)

        # Vérifier que la méthode delete_review a été appelée
        self.review_dao.delete_review.assert_called_once_with(1, 1)
        self.assertTrue(result)

    def test_get_average_rating(self):
        # Configurer des critiques pour le même film
        reviews = [
            Review(id_review=1, id_film=1, id_user=1, note=8, comment="Good movie"),
            Review(id_review=2, id_film=1, id_user=2, note=9, comment="Great movie"),
        ]
        self.review_dao.get_all_review_by_id.return_value = reviews

        # Calculer la note moyenne
        average_rating = self.review_service.get_average_rating(1)

        # Vérifier le calcul de la note moyenne
        self.assertEqual(average_rating, 8.5)

    def test_get_average_rating_no_reviews(self):
        # Configurer une absence de critiques
        self.review_dao.get_all_review_by_id.return_value = []

        # Calculer la note moyenne
        average_rating = self.review_service.get_average_rating(1)

        # Vérifier que la note moyenne est 0
        self.assertEqual(average_rating, 0)


if __name__ == "__main__":
    unittest.main()
