from src.Model.Review import Review
from src.dao.review_dao import ReviewDAO

def add_review(self,id_user,id_film,comment=None,note=None):
    """
        Ajoute un commentaire à un film via la DAO.

        Paramètres:
        -----------
        id_user : int
            L'identifiant de l'utilisateur.
        id_film
            L'identifiant du film.
        comment : str
            Le texte du commentaire à ajouter.

        Retourne:
        ---------

        bool
        """
    review=Review(id_review=1, id_film=id_film,id_user=id_user, comment=comment,note=note)
    existing_comments = self.review_dao.get_review_by_id_user_and_id_film(id_user, id_film)

    if existing_comments:
        return False 
    elif note:
        result = self.review_dao.add_comment(review)
        return result

def delete_review(self,id_user,id_film):
    """
        Supprime un commentaire à un film via la DAO.

        Paramètres:
        -----------

        id_user : int
            L'identifiant de l'utilisateur.
        id_film : str
            L'identifiant du film.
        
        Retourne:
        ---------

        bool
    """
    existing_comments = self.review_dao.get_review_by_id_user_and_id_film(id_user, id_film)

    if not existing_comments:
        return False
    result = self.review_dao.delete_comment(review)
    return result

def modify_review(self,id_user,id_film, comment_modif, note_modif):
    """
        Modifie un commentaire existant.
        
        Paramètres:
        -----------

        id_user : int
            L'identifiant de l'utilisateur.
        title : str
            Le titre du film.
        comment_modif: str
            Le nouveau
        
        Retourne:
        ---------

        bool
    """
    review=Review(id_review=1, id_film=id_film,id_user=id_user, comment=comment_modif,note=note)
    existing_comments = self.review_dao.get_review_by_id_user_and_id_film(id_user, id_film)

    if not existing_comments:
        return False
    elif not note:
        return False
    result = self.review_dao.delete_comment(review)
    return result
    result = self.review_dao.add_comment(review)
    return result
def delet_comment(u)

