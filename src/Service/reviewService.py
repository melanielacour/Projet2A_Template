from src.Model.Review import Review
from src.dao.review.dao import ReviewDAO

def add_comment(self,id_user,title,review):
    """
        Ajoute un commentaire à un film via la DAO.

        Paramètres:
        -----------
        id_user : int
            L'identifiant de l'utilisateur.
        title : str
            Le titre du film.
        comment : str
            Le texte du commentaire à ajouter.
        """
    existing_comments = self.review_dao.get_review_by_user_and_title(id_user, title)

    if existing_comments:
        return False 
    result = self.review_dao.add_comment(id_user, title, comment)
    return result

def delete_comment(self,id_user,title):
    """
        Supprime un commentaire à un film via la DAO.

        Paramètres:
        -----------

        id_user : int
            L'identifiant de l'utilisateur
        title : str
            Le titre du film
    """
    existing_comments = self.review_dao.get_review_by_user_and_title(id_user, title)

    if not existing_comments:
        return False 