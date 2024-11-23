import unittest
from unittest.mock import MagicMock
from src.Service.user_movie_service import UserMovieService
from src.Model.user_movie import UserMovie

import unittest
from unittest.mock import MagicMock
from src.Service.user_movie_service import UserMovieService
from src.Model.user_movie import UserMovie

class TestUserMovieService(unittest.TestCase):
    def setUp(self):
        # Mock du DAO
        self.user_movie_dao = MagicMock()
        self.user_movie_service = UserMovieService(self.user_movie_dao)

    def test_get_watchlist(self):
        # Configurer le mock pour simuler des résultats
        self.user_movie_dao.get_movies_by_user.return_value = [
            UserMovie(1, 101, "to watch"),
            UserMovie(1, 102, "to watch"),
        ]
    
        # Appeler la méthode à tester
        watchlist = self.user_movie_service.get_watchlist(1)
    
        # Vérifier que la méthode DAO a été appelée avec les bons arguments
        self.user_movie_dao.get_movies_by_user.assert_called_once_with(1, status="to watch")

        # Vérifier le nombre d'éléments dans la watchlist
        self.assertEqual(len(watchlist), 2)

        # Vérifier les attributs des objets renvoyés
        self.assertEqual(watchlist[0].id_film, 101)
        self.assertEqual(watchlist[0].status, "to watch")
        self.assertIsInstance(watchlist[0], UserMovie)
        self.assertEqual(watchlist[1].id_film, 102)
        self.assertEqual(watchlist[1].status, "to watch")



    def test_get_seenlist(self):
        # Configurer le mock
        self.user_movie_dao.get_movies_by_user.return_value = [
            UserMovie(1, 201, "watched"),
            UserMovie(1, 202, "watched")
        ]

        # Appeler la méthode
        seenlist = self.user_movie_service.get_seenlist(1)

        # Vérifier le résultat
        self.user_movie_dao.get_movies_by_user.assert_called_once_with(1, status="watched")
        self.assertEqual(len(seenlist), 2)
        self.assertEqual(seenlist[0].id_film, 201)

    def test_add_movie_to_watchlist(self):
        # Appeler la méthode
        self.user_movie_service.add_movie_to_watchlist(1, 101)

        # Vérifier l'appel
        self.user_movie_dao.add_movie.assert_called_once_with(1, 101, status="to watch")

    def test_add_movie_to_seenlist(self):
        # Appeler la méthode
        self.user_movie_service.add_movie_to_seenlist(1, 201)

        # Vérifier l'appel
        self.user_movie_dao.add_movie.assert_called_once_with(1, 201, status="watched")

    def test_delete_movie_from_list(self):
        # Appeler la méthode
        result = self.user_movie_service.delete_movie_from_list(1, 101, "to watch")

        # Vérifier l'appel
        self.user_movie_dao.delete_movie.assert_called_once_with(1, 101, "to watch")

    def test_update_movie_status(self):
        # Appeler la méthode pour mettre à jour le statut
        self.user_movie_service.update_movie_status(1, 101, "watched")

        # Vérifier l'appel de la méthode DAO avec les bons arguments
        self.user_movie_dao.add_movie.assert_called_once_with(1, 101, "watched")

    def test_update_movie_status_invalid(self):
        # Vérifier que l'exception est levée pour un statut invalide
        with self.assertRaises(ValueError):
            self.user_movie_service.update_movie_status(1, 101, "invalid_status")

if __name__ == "__main__":
    unittest.main()
