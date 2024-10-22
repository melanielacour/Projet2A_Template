import json

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MultiLabelBinarizer

from src.Model.Movie import Movie


def json_to_dataframe(movies_json):
    """
    Transforme le fichier JSON en DataFrame avec les colonnes title, producer et date.

    Parametres:
    -----------
    movies_json : fichier json
        fichier contenant des films avec comme clés title, producer et date.

    Returns:
    --------
    movies_df : dataframe
        dataframe pandas obtenu à partir du fichier json.
    """
    # Charger le JSON en tant que liste de dictionnaires
    data = json.loads(movies_json)

    # Transformer en DataFrame
    movies_df = pd.DataFrame(data)

    return movies_df


def classification(movies_json):
    '''
    Effectue une classification pour obtenir un dataframe des similarités entre chaque films.

    Parametres:
    -----------
    movies_json : fichier json
        fichier contenant des films avec comme clés title, producer et date.

    Returns:
    --------
    similarity_df : dataframe
        dataframe des imilarités entre chaque film.

    '''
    # Il est nécessaire de de convertir la base_movies en dictionnaire
    # pour faciliter la classification
    movies_df = json_to_dataframe(movies_json)

    # Ensuite, nous initialisons une variable chargée de l'encodage des
    # variables catégorielles (dans notre cas, title, producer et date).
    # Cette méthode permet de transformer les modalités en format binaire.
    mlb = MultiLabelBinarizer()

    # Encodage des catégories (genres)
    category_encoded = pd.DataFrame(mlb.fit_transform(movies_df['category']),
                                    columns=mlb.classes_,
                                    index=movies_df.index)

    # Encodage des producteurs
    producer_encoded = pd.DataFrame(mlb.fit_transform(movies_df['producer']),
                                    columns=mlb.classes_,
                                    index=movies_df.index)

    # Encodage des dates puisqu'elles sont mises en année, ce qui permet de les regrouper plus facilement
    date_encoded = pd.get_dummies(movies_df['date'])

    # Combiner toutes les colonnes encodées dans un DataFrame final
    movies_encoded = pd.concat([movies_df['title'], category_encoded, producer_encoded, date_encoded], axis=1)

    # Après avoir fait ces manipulations avec MultiLabelBinarizer,
    # nous nous retrouvons avec un pd.DataFrame contenant uniquement des
    # variables numériques. Les variables catégorielles ont été coupé, et les
    # modalités sont devenues des variables. Les valeurs de ces nouvelles
    # variables sont soit 0 si l'individu n'avait pas la modalité, soit dans
    # le cas contraire 1. Il s'agit d'un dérivé de la méthode OneHotEncoder,
    # seulement certaines variables étaient des listes, donc des individus
    # pouvaient avoir plusieurs modalités différentes pour une même variable.

    # Extraire les colonnes encodées sans le titre pour calculer la similarité
    features = movies_encoded.drop(columns=['title'])

    # Calculer la similarité entre tous les films. La similarité
    # entre les séries s'effectueront en calculant le cosinus de l'angle
    # entre les deux vecteurs (donc les deux séries).
    similarity_matrix = cosine_similarity(features)

    # Mettre la similarité dans un DataFrame pour une meilleure lisibilité
    similarity_df = pd.DataFrame(similarity_matrix, index=movies_encoded['title'], columns=movies_encoded['title'])

    return similarity_df


def recommend_movies(movie_title, movies_json, n=10):
    '''
    Renvoie la liste de recommendations des n films avec le plus gros score de similarités.

    Parametres:
    -----------
    movies_json : fichier json
        fichier contenant des films avec comme clés title, producer et date.
    movie_title : str
        titre du film à partir duquel on va chercher une recommandation.
    n : int
        nombre de films similaires que l'ont veut recommander

    Returns:
    --------
    recommandations : list
        liste des n films ayant le plus grand score de similarité.

    '''
    similarity_df = classification(movies_json)

    # Obtenir les similarités pour le film donné
    similarity_scores = similarity_df[movie_title]

    # Trier les films par similarité (du plus similaire au moins similaire)
    similarity_scores_desc = similarity_scores.sort_values(ascending=False)

    # Exclure le film lui-même de la liste
    similarity_scores_desc = similarity_scores_desc.drop(movie_title)

    # Prends les n meilleures recommandations après le tri et l'exclusion du film lui même
    recommendations = similarity_scores_desc.head(n).index.tolist()

    return recommendations

##print("Films recommandés pour 'Movie 1' :", recommendations)

