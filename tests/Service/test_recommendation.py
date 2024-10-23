import json
import unittest

import pandas as pd

from src.Service.recommendation import (classification, json_to_dataframe,
                                        recommend_movies)


class TestMovieFunctions(unittest.TestCase):

    def setUp(self):
        # Création d'un exemple de JSON de films
        self.movies_json = json.dumps([
            {"title": "Movie 1", "producer": "Producer A", "date": "2022", "category": ["Action", "Adventure"]},
            {"title": "Movie 2", "producer": "Producer B", "date": "2021", "category": ["Comedy"]},
            {"title": "Movie 3", "producer": "Producer A", "date": "2022", "category": ["Action", "Comedy"]},
            {"title": "Movie 4", "producer": "Producer C", "date": "2020", "category": ["Drama"]}
        ])

    def test_json_to_dataframe(self):
        """Test la conversion du JSON en DataFrame."""
        df = json_to_dataframe(self.movies_json)
        
        # Vérifie que le DataFrame a le bon nombre de lignes et de colonnes
        self.assertEqual(df.shape, (4, 4))  # 4 films, 4 colonnes (title, producer, date, category)
        
        # Vérifie le contenu du DataFrame
        self.assertIn("Movie 1", df['title'].values)
        self.assertIn("Producer A", df['producer'].values)

    def test_classification(self):
        """Test la classification des films pour obtenir la matrice de similarité."""
        similarity_df = classification(self.movies_json)
        
        # Vérifie que le DataFrame de similarité est correct
        self.assertEqual(similarity_df.shape, (4, 4))  # 4 films, 4 colonnes (tous les films)
        
        # Vérifie que les titres des films sont les index
        self.assertListEqual(list(similarity_df.index), ["Movie 1", "Movie 2", "Movie 3", "Movie 4"])

        # Vérifie que les valeurs ne sont pas toutes nulles
        self.assertFalse(similarity_df.isnull().values.any())

    def test_recommend_movies(self):
        """Test la fonction de recommandation de films."""
        recommendations = recommend_movies("Movie 1", self.movies_json, n=2)
        
        # Vérifie que le nombre de recommandations est correct
        self.assertEqual(len(recommendations), 2)
        
        # Vérifie que les recommandations ne contiennent pas le film d'origine
        self.assertNotIn("Movie 1", recommendations)
        
        # Vérifie que les recommandations sont bien dans la liste des titres de films
        titles = ["Movie 2", "Movie 3", "Movie 4"]
        for rec in recommendations:
            self.assertIn(rec, titles)

    def test_recommend_movies_no_similarities(self):
        """Test la fonction de recommandation quand il n'y a pas de similarités."""
        recommendations = recommend_movies("Movie 4", self.movies_json, n=2)
        
        # Vérifie que le nombre de recommandations est 2, mais peuvent être similaires ou non
        self.assertEqual(len(recommendations), 2)
        self.assertNotIn("Movie 4", recommendations)

if __name__ == "__main__":
    unittest.main()
