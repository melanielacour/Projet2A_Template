class UserSimple:
    def __init__(self, id_user: int, pseudo: str,is_scout:bool=False):
        self.id_user = id_user
        self.pseudo = pseudo
        self.is_scout= is_scout

    def __repr__(self):
        # Retourner un dictionnaire avec l'ID comme clé et un autre dictionnaire comme valeur
        return str({self.id_user: {"pseudo": self.pseudo, "is_scout": self.is_scout}})
