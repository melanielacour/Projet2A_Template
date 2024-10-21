class UserSimple:
    """
    Classe qui représente un utilisateur dans PopcornCritic.

    Attributs:
    ----------
    id_user : int
        L'identifiant de l'utilisateur (unique).
    pseudo : str
        Le pseudo de l'utilisateur.
    is_scout : bool
        Savoir si l'utilisateur est un scout, la valeur prise par défaut est False.

    Méthodes:
    ---------
    __repr__():
        Renvoie un dictionnaire avec l'Id en clé et en valeur un dictionnaire composé du pseudo en clé et du booleen en valeur.

    """
    def __init__(self, id_user: int, pseudo: str, pswd, is_scout: bool= False):
        self.id_user = id_user
        self.pseudo = pseudo
        self.is_scout= is_scout
        self.pswd=pswd
    def __repr__(self):
        # Retourner un dictionnaire avec l'ID comme clé et un autre dictionnaire comme valeur
        return str({self.id_user: {"pseudo": self.pseudo, "is_scout": self.is_scout}})