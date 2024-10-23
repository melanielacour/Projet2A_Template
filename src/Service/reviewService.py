from src.Model.Review import Review
from src.dao.review_dao import ReviewDAO

def add_review(self,id_user,id_film,comment=None,note):
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
        note : int
            La note à ajouter

        Retourne:
        ---------

        bool
        """
    review=Review(id_review=None, id_film=id_film,id_user=id_user, comment=comment,note=note)
    existing_comments = self.review_dao.get_review_by_id_user_and_id_film(id_user, id_film)

    if existing_comments:
        return False 
    elif note:
        result = self.review_dao.add_review(review)
        return result

def delete_comment(self,id_user,id_film):
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
    review=Review(id_review=None, id_film=id_film,id_user=id_user, comment=comment,note=note)
    existing_comments = self.review_dao.get_review_by_id_user_and_id_film(id_user, id_film)

    if not existing_comments:
        return False
    result = self.review_dao.delete_comment(review)
    return result

def delete_review(self,id_user,id_film):
    """
    Supprime tout l'avis (note et commentaire)

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
    review=Review(id_review=None, id_film=id_film,id_user=id_user, comment=comment,note=note)
    existing_comments = self.review_dao.get_review_by_id_user_and_id_film(id_user, id_film)
    if not existing_comments:
        return False
    result = self.review_dao.delete_review(review)
    return result

def modify_review(self,id_user,id_film, comment_modif, note_modif):
    """
        Modifie entièrement l'avis (commentaire + note) existant.
        
        Paramètres:
        -----------

        id_user : int
            L'identifiant de l'utilisateur.
        title : str
            Le titre du film.
        comment_modif: str
            Le nouveau commentaire.
        note_modif:int
            La nouvelle note
        
        Retourne:
        ---------

        bool
    """
    review=Review(id_review=None, id_film=id_film,id_user=id_user, comment=comment_modif,note=note)
    existing_comments = self.review_dao.get_review_by_id_user_and_id_film(id_user, id_film)

    if not existing_comments:
        return False
    result = self.review_dao.delete_review(review)
    return result
    result = self.review_dao.add_review(review)
    return result

def modify_comment(self,id_user,id_film, comment_modif):
    """
        Modifie le commentaire existant.
        
        Paramètres:
        -----------

        id_user : int
            L'identifiant de l'utilisateur.
        title : str
            Le titre du film.
        comment_modif: str
            Le nouveau commentaire.
        
        Retourne:
        ---------

        bool
    """
    review=Review(id_review=None, id_film=id_film,id_user=id_user, comment=comment_modif,note=note)
    existing_comments = self.review_dao.get_review_by_id_user_and_id_film(id_user, id_film)

    if not existing_comments:
        return False
    result = self.review_dao.delete_review(review)
    return result
    result = self.review_dao.add_review(review)
    return result

def modify_note(self,id_user,id_film, comment_note):
    """
        Modifie le commentaire existant.
        
        Paramètres:
        -----------

        id_user : int
            L'identifiant de l'utilisateur.
        title : str
            Le titre du film.
        note_modif:int
            La nouvelle note.
        
        Retourne:
        ---------

        bool
    """
    review=Review(id_review=None, id_film=id_film,id_user=id_user, comment=comment,note=note_modif)
    existing_comments = self.review_dao.get_review_by_id_user_and_id_film(id_user, id_film)

    if not existing_comments:
        return False
    result = self.review_dao.delete_review(review)
    return result
    result = self.review_dao.add_review(review)
    return result
