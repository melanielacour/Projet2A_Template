class MovieSimple:
    """
    Une classe simple pour représenter un film avec un identifiant local,
    un identifiant TMDB (The Movie Database), et un titre.

    Attributs :
    -----------
    - id_local : int
        id film dans la base de données locale.
    - id_tmdb : int
        id film dans la base de données TMDB.
    - title : str
        Le titre du film.

    """
    def __init__(self, id_local: int, id_tmdb: int, title: str):
        self.id_local = id_local
        self.id_tmdb = id_tmdb
        self.title = title

    def __repr__(self):
        res = f"Movie(id_local={self.id_local}, id_tmdb={self.id_tmdb}, "
        res += f"title='{self.title}')"
        return res
