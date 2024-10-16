import pytest

from src.Model.Review import Review


class TestReview:

    def test_add_review(self):
        # Given
        review = Review(id_film=1, id_user=101)

        # When
        review.add_review("Excellent film d'action.")

        # Then
        assert Review.reviews[(
            review.id_user, review.id_film)] == "Excellent film d'action."

    def test_delete_review(self):
        # Given
        review = Review(id_film=1, id_user=101)

        # When
        review.add_review("Pas terrible.")
        review.delete_review()

        # Then
        assert (review.id_user, review.id_film) not in Review.reviews
