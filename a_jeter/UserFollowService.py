class UserFollowService:
    """ Classe qui gère les éclaireurs et leur statut particulier. """
    def __init__(self):
        self.users = {}  # peut-être mettre directement la database ?
        self.scouts = {}  # créer une db scout ?

    def become_scout(self, id_user: int) -> None:
        """
        Transforme un utilisateur en éclaireur.
        
        Parametres:
        -----------
        id_user : int
            ID de l'utilisateur qui souhaite devenir eclaireur

        Returns:
        --------
            None
        """
        if id_user in self.users:
            self.users[id_user].is_scout = True
            self.scouts[id_user] = []

    def add_scout(self, id_user_follower: int, id_scout: int) -> None:
        """
        Pour qu'un utilisateur suive un éclaireur.
        
        Parametres:
        -----------
        id_user_follower : int
            ID de l'utilisateur qui souhaite suivre un scout
        id_scout : int
            ID du scout que sera suivi par l'utilisateur

        Returns:
        --------
            None
        
        """
        if id_user_follower in self.users and id_scout in self.scouts:
            self.scouts[id_user_follower].append(id_scout)

    def get_scouts(self, id_user: int) -> list:
        """
        Retourne la liste des éclaireurs suivis par l'utilisateur.
        
        Parametres:
        -----------
        id_user : int
            ID de l'utilisateur duquel on retourne la liste de scout

        Returns:
        --------
        [self.users[id_scout] for id_scout in self.scouts.get(id_user, [])] : list
            list de scouts de l'utilisateur
        """
        return [self.users[id_scout] for id_scout in
                self.scouts.get(id_user, [])]
