import unittest
from unittest.mock import MagicMock, patch
from src.dao.user_movies_dao import UserMovieDao
from src.Model.user_movie import UserMovie


class TestUserMovieDao(unittest.TestCase):
    def setUp(self):
        self.mock_db_connection = MagicMock()
        self.user_movie_dao = UserMovieDao(self.mock_db_connection)


    def test_get_movies_by_user(self):
        mock_cursor = self.mock_db_connection.connection().__enter__().cursor().__enter__()
        mock_cursor.fetchall.return_value = [
            {"id_user": 1, "id_film": 101, "status": "watched"},
            {"id_user": 1, "id_film": 102, "status": "to watch"},
        ]

        result = self.user_movie_dao.get_movies_by_user(1)

        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], UserMovie)
        self.assertEqual(result[0].id_user, 1)
        self.assertEqual(result[0].id_film, 101)
        self.assertEqual(result[0].status, "watched")
        self.assertEqual(result[1].status, "to watch")

        mock_cursor.execute.assert_called_once_with(
            "SELECT id_user, id_film, status  FROM projet_2a.user_movies WHERE id_user = %(id_user)s",
            {"id_user": 1},
        )


if __name__ == "__main__":
    unittest.main()
