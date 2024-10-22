import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity
from base_series import BaseSeries


def convert_to_dataframe(base_series):
    """Convertion d'une base de séries de classe BaseSeries en pd.DataFrame.

    Parameters:
    -----------
    base_series: BaseSeries
        Base de données contenant les séries

    Return:
    -------
    pd.DataFrame
        Dataframe contenant les séries.

    Examples:
    ---------
    >>> base_series = BaseSeries()
    >>> base_series.load_from_path("dat_test.csv")
    Base de données chargée avec succès depuis dat_test.csv.
    >>> base_series = convert_to_dataframe(base_series)
    >>> print(type(base_series))
    <class 'pandas.core.frame.DataFrame'>
    """
    data = {
        "name": [],
        "number_of_seasons": [],
        "number_of_episodes": [],
        "genres": [],
        "languages": [],
        "networks": [],
        "adult": [],
        "status": []
    }

    for serie in base_series.series.values():
        data["name"].append(serie.name)
        data["number_of_seasons"].append(serie.number_of_seasons)
        data["number_of_episodes"].append(serie.number_of_episodes)
        data["genres"].append(serie.genres)
        data["languages"].append(serie.spoken_languages)
        data["networks"].append(serie.networks)
        data["adult"].append(serie.adult)
        data["status"].append(serie.status)
    return pd.DataFrame(data)


def classification(base_series, nom_serie, n=10):
    """Proposer les n séries les plus similaires à celle précisée.

    Parameters:
    -----------
    base_series: BaseSeries
        Base de données contenant les séries.
    nom_serie: str
        Nom de la série intéressée
    n: int
        Nombre de séries à recommander

    Return:
    -------
    list
        Liste des n séries recommandées

    Examples:
    ---------
    >>> base_series = BaseSeries()
    >>> base_series.load_from_path("dat_test.csv")
    Base de données chargée avec succès depuis dat_test.csv.
    >>> nom_serie = "The Simpsons"
    >>> n = 1
    >>> classifier = classification(base_series, nom_serie, n)
    Les 1 séries recommandées sont :
    - Law & Order: Special Victims Unit
    >>> classifier
    ['Law & Order: Special Victims Unit']
    """
    if not isinstance(base_series, BaseSeries):
        raise TypeError("La base de données doit être une instance de "
                        "BaseSeries.")

    if not isinstance(nom_serie, str):
        raise TypeError("Le nom de la série intéressée doit être une "
                        "instance de str.")

    if not isinstance(n, int):
        raise TypeError("Le nombre de séries à recommander doit être une "
                        "instance de int.")

    # Il est nécessaire de de convertir la base_series en dictionnaire
    # pour faciliter la classification
    base_series_dict = convert_to_dataframe(base_series)

    # Ensuite, nous initialisons une variable chargée de l'encodage des
    # variables catégorielles (dans notre cas, genres, languages, networks
    # et status). Cette méthode permet de transformer les modalités en format
    # binaire.
    mlb = MultiLabelBinarizer()
    genres_encoded = pd.DataFrame(mlb.fit_transform(base_series_dict["genres"]),
                                 columns=mlb.classes_, index=base_series_dict.index)
    languages_encoded = pd.DataFrame(mlb.fit_transform(
                                    base_series_dict["languages"]),
                                    columns=mlb.classes_,
                                    index=base_series_dict.index)
    networks_encoded = pd.DataFrame(mlb.fit_transform(base_series_dict["networks"]),
                                   columns=mlb.classes_,
                                   index=base_series_dict.index)
    status_encoded = pd.DataFrame(mlb.fit_transform(base_series_dict["status"]),
                                 columns=mlb.classes_,
                                 index=base_series_dict.index)

    data_encoded = pd.concat([base_series_dict[["name", "number_of_seasons",
                                           "number_of_episodes", "adult"]],
                             genres_encoded, languages_encoded,
                             networks_encoded, status_encoded], axis=1)

    # Après avoir fait ces manipulations avec MultiLabelBinarizer,
    # nous nous retrouvons avec un pd.DataFrame contenant uniquement des
    # variables numériques. Les variables catégorielles ont été coupé, et les
    # modalités sont devenues des variables. Les valeurs de ces nouvelles
    # variables sont soit 0 si l'individu n'avait pas la modalité, soit dans
    # le cas contraire 1. Il s'agit d'un dérivé de la méthode OneHotEncoder,
    # seulement certaines variables étaient des listes, donc des individus
    # pouvaient avoir plusieurs modalités différentes pour une même variable.

    serie_specified = data_encoded[data_encoded["name"] == nom_serie]

    # Enfin, nous mesurons la similarité entre la série spécifiée et
    # chacune des séries de la base. La mesure de similarité s'effectue
    # à l'aide de la fonction cosine_similarity.
    # Voici une explication simple de son fonctionnement :
    # Imaginiez que l'on représente les séries sous forme de vecteur dans
    # un espace vectoriel où chaque variable est une dimension. La similarité
    # entre les séries s'effectueront en calculant le cosinus de l'angle
    # entre les deux vecteurs (donc les deux séries).
    similarities = cosine_similarity(serie_specified.drop(columns=["name"]),
                                    data_encoded.drop(columns=["name"]))

    similarities = similarities.flatten()
    similarities[data_encoded["name"] == nom_serie] = -1

    # Pour finir, nous extrayons les n séries avec les mesures les plus fortes
    # donc les séries les plus similaires.
    closer_indexes = similarities.argsort()[-n:][::-1]

    most_similar_series = data_encoded.iloc[closer_indexes]["name"]
    print(f"Les {n} séries recommandées sont :")
    liste = []
    for serie in most_similar_series:
        liste.append(serie)
        print("- " + serie)
    return liste


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
