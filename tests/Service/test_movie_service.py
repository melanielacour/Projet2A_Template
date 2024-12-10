import unittest
from unittest.mock import patch, MagicMock
from src.Service.MovieService import MovieService
from src.Model.Movie import Movie

class TestMovieService(unittest.TestCase):
    
    @patch('src.Service.MovieService.requests.get')
    def test_get_category_id(self, mock_get):
        # Test de la méthode get_category_id
        service = MovieService()
        
        # Cas où la catégorie est trouvée
        category_id = service.get_category_id("action")
        self.assertEqual(category_id, 28)
        
        # Cas où la catégorie est inconnue
        category_id = service.get_category_id("nonexistent")
        self.assertIsNone(category_id)
    
    @patch('src.Service.MovieService.requests.get')
    def test_get_movie_by_id(self, mock_get):
        # Test de la méthode get_movie_by_id
        
        # Mock de la réponse de l'API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": 123,
            "title": "Test Movie",
            "production_companies": [{"name": "Test Company"}],
            "genres": [{"name": "Action"}],
            "release_date": "2023-12-01"
        }
        mock_get.return_value = mock_response
        
        service = MovieService()
        movie = service.get_movie_by_id(123)
        
        self.assertEqual(movie.id_film, 123)
        self.assertEqual(movie.title, "Test Movie")
        self.assertEqual(movie.producer, "Test Company")
        self.assertEqual(movie.category, "Action")
        self.assertEqual(movie.date, "2023")
    
    @patch('src.Service.MovieService.requests.get')
    def test_get_movie_by_title(self, mock_get):
        # Mock de la réponse de recherche
        mock_search_response = MagicMock()
        mock_search_response.status_code = 200
        mock_search_response.json.return_value = {"results": [
            {"id": 123, "title": "Test Movie", "adult": False}
        ]}

        # Mock de la réponse de détails du film
        mock_details_response = MagicMock()
        mock_details_response.status_code = 200
        mock_details_response.json.return_value = {
            "id": 123,
            "title": "Test Movie",
            "production_companies": [{"name": "Test Company"}],
            "genres": [{"name": "Action"}],
            "release_date": "2023-12-01",
            "adult": False
        }

        # Définir le comportement pour chaque appel
        mock_get.side_effect = [mock_search_response, mock_details_response]
    
        service = MovieService()
        films = service.get_movie_by_title("Test Movie")

        # Vérification que la méthode retourne bien une liste de films avec l'instance de Movie attendue
        assert len(films) == 1
        assert isinstance(films[0], Movie)
        assert films[0].id_film == 123
        assert films[0].title == "Test Movie"
        assert films[0].producer == "Test Company"
        assert films[0].category == "Action"
        assert films[0].date == "2023"
        
    @patch('src.Service.MovieService.requests.get')
    def test_get_movies_by_category(self, mock_get):
        # Mock de la réponse de recherche des films par catégorie
        mock_search_response = MagicMock()
        mock_search_response.status_code = 200
        mock_search_response.json.return_value = {
            "results": [
                {"id": 123, "title": "Test Movie", "adult": False}
            ]
        }

        # Mock de la réponse de détails du film
        mock_details_response = MagicMock()
        mock_details_response.status_code = 200
        mock_details_response.json.return_value = {
            "id": 123,
            "title": "Test Movie",
            "production_companies": [{"name": "Test Company"}],
            "genres": [{"name": "Action"}],
            "release_date": "2023-12-01"
        }

        # Définir le comportement pour chaque appel
        mock_get.side_effect = [mock_search_response, mock_details_response]
    
        service = MovieService()
        films = service.get_movies_by_category("Action")

        # Vérification que la méthode retourne bien une liste de films avec l'instance de Movie attendue
        assert len(films) == 1
        assert isinstance(films[0], Movie)
        assert films[0].id_film == 123
        assert films[0].title == "Test Movie"
        assert films[0].producer == "Test Company"
        assert films[0].category == "Action"
        assert films[0].date == "2023"
    
    @patch('src.Service.MovieService.requests.get')
    def test_get_movies_by_director(self, mock_get):
        # Mock de la réponse de recherche des films par réalisateur
        mock_search_response = MagicMock()
        mock_search_response.status_code = 200
        mock_search_response.json.return_value = {
            "results": [
                {"id": 123, "title": "Test Movie", "adult": False}
            ]
        }

        # Mock de la réponse de détails du film
        mock_details_response = MagicMock()
        mock_details_response.status_code = 200
        mock_details_response.json.return_value = {
            "id": 123,
            "title": "Test Movie",
            "production_companies": [{"name": "Test Company"}],
            "genres": [{"name": "Action"}],
            "release_date": "2023-12-01"
        }

        # Simuler les deux appels
        mock_get.side_effect = [mock_search_response, mock_details_response]
    
        service = MovieService()
        films = service.get_movies_by_director(456)  # Director ID
    
        # Vérifier que le nombre de films est bien 1
        self.assertEqual(len(films), 1)
    
        # Vérifier que le film retourné est correct
        film = films[0]
        self.assertEqual(film.id_film, 123)
        self.assertEqual(film.title, "Test Movie")
        self.assertEqual(film.producer, "Test Company")
        self.assertEqual(film.category, "Action")
        self.assertEqual(film.date, "2023")
    
    @patch('src.Service.MovieService.requests.get')
    def test_get_movies_by_director_name(self, mock_get):
        # Mock de la réponse de recherche de réalisateur
        mock_search_response = MagicMock()
        mock_search_response.status_code = 200
        mock_search_response.json.return_value = {
            "results": [
                {"id": 456, "name": "Test Director"}
            ]
        }
        # Mock de la réponse de films par réalisateur
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [
                {"id": 123, "title": "Test Movie", "adult": False}
            ]
        }
        # Mock de la réponse de détails du film
        mock_details_response = MagicMock()
        mock_details_response.status_code = 200
        mock_details_response.json.return_value = {
            "id": 123,
            "title": "Test Movie",
            "production_companies": [{"name": "Test Company"}],
            "genres": [{"name": "Action"}],
            "release_date": "2023-12-01"
        }

        # Mettre tous les mocks dans side_effect
        mock_get.side_effect = [mock_search_response, mock_response, mock_details_response]
    
        service = MovieService()
        films = service.get_movies_by_director_name("Test Director")
    
        # Vérification des résultats
        self.assertEqual(len(films), 1)
        self.assertEqual(films[0].id_film, 123)
        self.assertEqual(films[0].title, "Test Movie")
        self.assertEqual(films[0].producer, "Test Company")
        self.assertEqual(films[0].category, "Action")
        self.assertEqual(films[0].date, "2023")
if __name__ == '__main__':
    unittest.main()
