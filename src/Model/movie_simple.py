class MovieSimple:
    def __init__(self, id_local: int, id_tmdb: int, title: str):
        self.id_local = id_local
        self.id_tmdb = id_tmdb
        self.title = title

    def __repr__(self):
        return f"Movie(id_local={self.id_local}, id_tmdb={self.id_tmdb}, title='{self.title}')"
