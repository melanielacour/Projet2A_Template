class UserMovie:
    def __init__(self, id_user, id_film, status):
        self.id_user = id_user
        self.id_film = id_film
        self.status = status

    def __repr__(self):
        return f"UserMovie(id_user={self.id_user}, id_film={self.id_film}, status='{self.status}')"
