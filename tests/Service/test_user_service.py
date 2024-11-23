import unittest
from unittest.mock import patch, MagicMock, Mock
from src.Service.UserService import UserService
from src.dao.user_repo import UserRepo
from src.dao.review_dao import ReviewDao
from src.Service.PasswordService import PasswordService
from src.Service.JWTService import JwtService

class TestUserService(unittest.TestCase):
    def setUp(self):
        self.user_service = UserService()

    @patch("src.dao.user_repo.UserRepo.get_by_username")
    @patch("src.dao.user_repo.UserRepo.insert_into_db")
    @patch("src.Service.PasswordService.PasswordService.hash_password")
    def test_register_user_success(self, mock_hash_password, mock_insert_into_db, mock_get_by_username):
        mock_get_by_username.return_value = None
        mock_hash_password.return_value = "hashed_password"
        mock_insert_into_db.return_value = True

        result = self.user_service.register_user("test_user", "SecurePassword123")
        self.assertEqual(result, "Vous êtes bien inscrit !")

    @patch("src.dao.user_repo.UserRepo.get_by_username")
    def test_register_user_existing_username(self, mock_get_by_username):
        mock_get_by_username.return_value = True

        with self.assertRaises(ValueError) as context:
            self.user_service.register_user("existing_user", "password123")
        self.assertEqual(str(context.exception), "Cet identifiant est déjà utilisé.")

    @patch("src.Service.JWTService.JwtService.encode_jwt")
    def test_log_in_success(self, mock_encode_jwt):
        # Configurer le comportement du mock
        mock_encode_jwt.return_value = {"access_token": "mocked_token"}

        # Appeler la méthode log_in
        response = self.user_service.log_in("valid_pseudo", "valid_password")

        # Vérifier le résultat
        self.assertEqual(response, {"success": True, "token": "mocked_token"})
        mock_encode_jwt.assert_called_once_with(mock.ANY)


    @patch("src.dao.user_repo.UserRepo.get_by_username")
    @patch("src.Service.PasswordService.PasswordService.validate_pseudo_password")
    @patch("src.Service.JWTService.JwtService.encode_jwt")
    def test_log_in_success(self, mock_encode_jwt, mock_validate_pseudo_password, mock_get_by_username):
        mock_user = Mock(id=1, username="test_user")
        mock_get_by_username.return_value = mock_user
        mock_validate_pseudo_password.return_value = True
        mock_encode_jwt.return_value = Mock(access_token="fake_token")

        result = self.user_service.log_in("test_user", "password123")
        self.assertTrue(result["success"])
        self.assertEqual(result["token"], "fake_token")

    @patch("src.dao.user_repo.UserRepo.get_by_username")
    def test_log_in_invalid_username(self, mock_get_by_username):
        mock_get_by_username.return_value = None

        with self.assertRaises(ValueError) as context:
            self.user_service.log_in("nonexistent_user", "password123")
        self.assertEqual(str(context.exception), "Identifiant incorrect.")

    @patch("src.dao.user_repo.UserRepo.get_by_username")
    @patch("src.Service.PasswordService.PasswordService.validate_pseudo_password")
    def test_log_in_invalid_password(self, mock_validate_pseudo_password, mock_get_by_username):
        mock_user = Mock(id=1, username="test_user")
        mock_get_by_username.return_value = mock_user
        mock_validate_pseudo_password.return_value = False

        with self.assertRaises(ValueError) as context:
            self.user_service.log_in("test_user", "wrongpassword")
        self.assertEqual(str(context.exception), "Mot de passe incorrect.")

    @patch("src.dao.user_repo.UserRepo.get_by_id")
    @patch("src.dao.review_dao.ReviewDao.get_all_reviews_by_user_id")
    @patch("src.dao.user_repo.UserRepo.update_status")
    def test_promote_to_scout_success(self, mock_update_status, mock_get_reviews, mock_get_by_id):
        mock_user = Mock(id=1, is_scout=False)
        mock_get_by_id.return_value = mock_user
        mock_get_reviews.return_value = [Mock() for _ in range(10)]  # Mock 10 reviews

        result = self.user_service.promote_to_scout(1)
        self.assertEqual(result, "Vous êtes maintenant éclaireur !")

    @patch("src.dao.user_repo.UserRepo.get_by_id")
    @patch("src.dao.review_dao.ReviewDao.get_all_reviews_by_user_id")
    def test_promote_to_scout_not_enough_reviews(self, mock_get_reviews, mock_get_by_id):
        mock_user = Mock(id=1, is_scout=False)
        mock_get_by_id.return_value = mock_user
        mock_get_reviews.return_value = [Mock() for _ in range(5)]  # Mock 5 reviews

        result = self.user_service.promote_to_scout(1)
        self.assertEqual(result, "Vous ne remplissez pas les conditions nécessaires pour devenir éclaireur.")

    @patch("src.dao.user_repo.UserRepo.get_by_id")
    @patch("src.dao.user_repo.UserRepo.update_status")
    @patch("src.dao.follower_dao.FollowerDao.get_followers_of_scout")
    @patch("src.dao.follower_dao.FollowerDao.unfollow_scout")
    def test_demote_scout_success(self, mock_unfollow, mock_get_followers, mock_update_status, mock_get_by_id):
        mock_user = Mock(id=1, is_scout=True)
        mock_get_by_id.return_value = mock_user
        mock_get_followers.return_value = [2, 3]  # Mock followers' IDs

        result = self.user_service.demote_scout(1)
        self.assertEqual(result, "Votre statut éclaireur a été révoqué.")
        mock_unfollow.assert_called()

if __name__ == "__main__":
    unittest.main()
