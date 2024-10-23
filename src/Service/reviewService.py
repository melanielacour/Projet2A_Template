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
    # Vérifie que la note soit bien comprise entre 1 et 10 (barème SensCritique)
    if not 1<=note<=10:
        raise ValueError("La note n'est pas comprise entre 1 et 10")

    # Regarde dans la base de données si un commentaire existe déjà
    review=Review(id_review=None, id_film=id_film,id_user=id_user, comment=comment,note=note)
    existing_comments = self.review_dao.get_review_by_id_user_and_id_film(id_user, id_film)

    # Si un commentaire existe lève une erreur sinon ajoute un avis grâce à la DAO
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
    # Regarde dans la base de données si un commentaire existe déjà
    review=Review(id_review=None, id_film=id_film,id_user=id_user, comment=comment,note=note)
    existing_comments = self.review_dao.get_review_by_id_user_and_id_film(id_user, id_film)
    
    # Si aucun commentaire existe lève une erreur, sinon supprime le commentaire grâce à la DAO
    if not existing_comments:
        return False
    result = self.review_dao.delete_review(review)
    return result
    review=Review(id_review=None, id_film=id_film,id_user=id_user, comment=None,note=note)
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
    # Regarde dans la base de données si un avis existe déjà
    review=Review(id_review=None, id_film=id_film,id_user=id_user, comment=comment,note=note)
    existing_comments = self.review_dao.get_review_by_id_user_and_id_film(id_user, id_film)

    # Si aucun avis existe lève une erreur, sinon supprime l'avis grâce à la DAO
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
    # Vérifie que la nouvelle note soit bien comprise entre 1 et 10 (barème SensCritique)
    if not 1<=note_modif<=10:
        raise ValueError("La note n'est pas comprise entre 1 et 10")
    
    # Regarde dans la base de données si un avis existe déjà
    review=Review(id_review=None, id_film=id_film,id_user=id_user, comment=comment_modif,note=note)
    existing_comments = self.review_dao.get_review_by_id_user_and_id_film(id_user, id_film)

    # Si aucun avis existe lève une erreur, sinon modifie l'avis grâce à la DAO (suppression puis ajout)
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

    # Regarde dans la base de données si un commentaire existe déjà
    review=Review(id_review=None, id_film=id_film,id_user=id_user, comment=comment_modif,note=note)
    existing_comments = self.review_dao.get_review_by_id_user_and_id_film(id_user, id_film)

    # Si aucun commentaire existe lève une erreur, sinon supprime le commentaire grâce à la DAO
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
    # Vérifie que la note soit bien comprise entre 1 et 10 (barème SensCritique)
    if not 1<=note<=10:
        raise ValueError("La note n'est pas comprise entre 1 et 10")
    
    # Regarde dans la base de données si une note existe déjà
    review=Review(id_review=None, id_film=id_film,id_user=id_user, comment=comment,note=note_modif)
    existing_comments = self.review_dao.get_review_by_id_user_and_id_film(id_user, id_film)

    # Si aucun avis existe lève une erreur, sinon modifie l'avis grâce à la DAO (suppression puis ajout)
    if not existing_comments:
        return False
    result = self.review_dao.delete_review(review)
    return result
    result = self.review_dao.add_review(review)
    return result

# get_all_review_by_id à faire
