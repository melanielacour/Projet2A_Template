from unittest.mock import MagicMock
from typing import Optional, Union, Literal
import pytest
from src.dao.db_connection import DBConnection
from src.Model.User import User
from src.dao.user_repo import UserRepo



class MockDBConnection:
    def __init__(self):
        # Crée les objets MagicMock pour la connexion et le curseur
        self.mock_connection = MagicMock()
        self.mock_cursor = MagicMock()
        
        # Configure le comportement des méthodes __enter__ et cursor
        self.mock_connection.__enter__.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.mock_cursor.__enter__.return_value = self.mock_cursor
        
        # Attributs pour suivre la dernière requête exécutée
        self.last_query = None
        self.last_query_params = None
        self.query_responses = {}

    def connection(self):
        return self.mock_connection

    def set_query_response(self, query: str, response: Optional[dict], rowcount=1):
        """
        Configure la réponse de la requête spécifique et le nombre de lignes affectées.
        """
        # Configure l'effet de la méthode execute
        def execute_mock(query_arg, params=None):
            if query_arg.strip() == query.strip():
                self.mock_cursor.fetchone.return_value = response
                self.mock_cursor.rowcount = rowcount  # Mise à jour de rowcount pour le curseur
            else:
                self.mock_cursor.fetchone.return_value = None
                self.mock_cursor.rowcount = 0  # Aucun changement de ligne si la requête n'est pas celle attendue

        # Associe l'effet simulé à la méthode execute
        self.mock_cursor.execute.side_effect = execute_mock

    def execute(self, query, params=None):
        """
        Simule l'exécution de la requête et retourne le rowcount.
        """
        self.last_query = query.strip()
        self.last_query_params = params
        return self.mock_cursor.rowcount  # Retourne le rowcount du curseur simulé

    def fetchone(self):
        """
        Simule la récupération du premier résultat de la requête.
        """
        return self.mock_cursor.fetchone()
    
    def __enter__(self):
        return self.mock_connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass



from src.dao.user_repo import UserRepo
from src.Model.User import User

def test_get_user_by_id():
    # Initialiser le mock
    mock_db = MockDBConnection()

    # Définir une réponse pour la requête SQL
    mock_db.set_query_response(
        "SELECT * FROM users WHERE id = %(user_id)s",
        {"id": 1, "username": "janjak", "salt": "salt_val",  "password": "hashed_pwd","is_scout": False}
    )

    # Créer une instance de UserRepo avec le mock
    user_repo = UserRepo(mock_db)

    # Appeler la méthode à tester
    user: User = user_repo.get_by_id(1)

    # Vérifications
    assert user is not None
    assert user.id == 1
    assert user.username == "janjak"
    assert user.password == "hashed_pwd"
    assert user.salt == "salt_val"
    assert user.is_scout is False


def test_get_by_username():
    # Initialiser le mock
    mock_db = MockDBConnection()
    
    # Définir une réponse pour la requête SQL
    mock_db.set_query_response(
        "SELECT * FROM users WHERE username = %(username)s",
        {"id": 1, "username": "janjak", "salt": "salt_val", "password": "hashed_pwd", "is_scout": False}
    )
    
    # Créer une instance de UserRepo avec le mock
    user_repo = UserRepo(mock_db)
    
    # Appeler la méthode à tester
    user: Optional[User] = user_repo.get_by_username("janjak")
    
    # Assertions
    assert user is not None, "L'utilisateur devrait être trouvé."
    assert user.id == 1, "L'ID de l'utilisateur est incorrect."
    assert user.username == "janjak", "Le pseudo de l'utilisateur est incorrect."
    assert user.salt == "salt_val", "Le salt de l'utilisateur est incorrect."
    assert user.password == "hashed_pwd", "Le mot de passe de l'utilisateur est incorrect."
    assert user.is_scout is False, "Le statut is_scout de l'utilisateur est incorrect."

    # Tester le cas où aucun utilisateur n'est trouvé
    mock_db.set_query_response("SELECT * FROM users WHERE username = %(username)s", None)
    user_not_found: Optional[User] = user_repo.get_by_username("unknown_user")
    assert user_not_found is None, "L'utilisateur ne devrait pas être trouvé."


def test_insert_into_db():
    # Initialiser le mock
    mock_db = MockDBConnection()
    
    # Définir une réponse pour la requête d'insertion
    mock_db.set_query_response(
        """
        INSERT INTO users (id, username, salt, password)
        VALUES (DEFAULT, %(username)s, %(salt)s, %(password)s)
        RETURNING *;
        """,
        {"id": 1, "username": "new_user", "salt": "new_salt", "password": "hashed_password", "is_scout": False}
    )
    
    # Créer une instance de UserRepo avec le mock
    user_repo = UserRepo(mock_db)
    
    # Appeler la méthode à tester
    new_user: User = user_repo.insert_into_db("new_user", "new_salt", "hashed_password")
    
    # Assertions
    assert new_user is not None, "Un utilisateur devrait être créé."
    assert new_user.id == 1, "L'ID de l'utilisateur est incorrect."
    assert new_user.username == "new_user", "Le pseudo de l'utilisateur est incorrect."
    assert new_user.salt == "new_salt", "Le salt de l'utilisateur est incorrect."
    assert new_user.password == "hashed_password", "Le mot de passe haché est incorrect."
    assert new_user.is_scout is False, "Le statut is_scout de l'utilisateur est incorrect."

def test_update_pseudo():
    # Initialiser le mock
    mock_db = MockDBConnection()

    # Définir une réponse pour la requête d'update avec rowcount=1 (une ligne affectée)
    mock_db.set_query_response(
        "UPDATE users SET username = %(new_pseudo)s WHERE id = %(user_id)s",
        response=True,  # Ceci n'est pas utilisé dans ce cas, donc True suffit
        rowcount=1  # Simule qu'une ligne a été affectée
    )

    # Créer une instance de UserRepo avec le mock
    user_repo = UserRepo(mock_db)

    # Appeler la méthode à tester
    success = user_repo.update_pseudo(1, "updated_username")

    # Assertions
    assert success is True, "La mise à jour du pseudo devrait réussir."

def test_update_password():
    # Initialiser le mock
    mock_db = MockDBConnection()

    # Définir une réponse pour la requête d'update avec rowcount=1 (une ligne affectée)
    mock_db.set_query_response(
        "UPDATE users SET hashed_password = %(hashed_password)s WHERE id = %(user_id)s",
        response=True,  # Cette réponse n'est pas utilisée ici, donc True suffit
        rowcount=1  # Simule qu'une ligne a été affectée
    )

    # Créer une instance de UserRepo avec le mock
    user_repo = UserRepo(mock_db)

    # Appeler la méthode à tester
    success = user_repo.update_password(1, "new_hashed_password")

    # Assertions
    assert success is True, "La mise à jour du mot de passe devrait réussir."

def test_update_status():
    # Initialiser le mock
    mock_db = MockDBConnection()

    # Définir une réponse pour la requête d'update avec rowcount=1 (une ligne affectée)
    mock_db.set_query_response(
        "UPDATE users SET is_scout = %(is_scout)s WHERE id = %(user_id)s",
        response=True,  # Cette réponse n'est pas utilisée ici, donc True suffit
        rowcount=1  # Simule qu'une ligne a été affectée
    )

    # Créer une instance de UserRepo avec le mock
    user_repo = UserRepo(mock_db)

    # Appeler la méthode à tester
    success = user_repo.update_status(1, True)

    # Assertions
    assert success is True, "La mise à jour du statut d'éclaireur devrait réussir."

def test_delete_by_id():
    # Initialiser le mock
    mock_db = MockDBConnection()

    # Définir une réponse pour la requête de suppression avec rowcount=1 (une ligne affectée)
    mock_db.set_query_response(
        "DELETE FROM users WHERE id = %(user_id)s",
        response=True,  # Cette réponse n'est pas utilisée ici, donc True suffit
        rowcount=1  # Simule qu'une ligne a été affectée
    )

    # Créer une instance de UserRepo avec le mock
    user_repo = UserRepo(mock_db)

    # Appeler la méthode à tester
    success = user_repo.delete_by_id(1)

    # Assertions
    assert success is True, "La suppression de l'utilisateur devrait réussir."


#Fixture pour la connexion mockée
@pytest.fixture
def db_connection():
    # Instanciation du mock de la connexion à la base de données
    return MockDBConnection()

# Fixture pour l'instanciation de UserRepo
@pytest.fixture
def user_repo(db_connection):
    return UserRepo(db_connection)


# Test pour `get_by_id` quand l'utilisateur n'est pas trouvé
def test_get_by_id_user_not_found(user_repo, db_connection):
    # Simuler une réponse de la requête pour aucun utilisateur trouvé
    db_connection.set_query_response("SELECT * FROM users WHERE id = %(user_id)s", None)
    
    # Appeler la méthode à tester
    result = user_repo.get_by_id(9999)
    
    # Vérifier que le résultat est None
    assert result is None

# Test d'insertion avec des valeurs invalides
def test_insert_into_db_invalid_data(user_repo, db_connection):
    # Simuler une réponse de la requête (pas nécessaire pour l'insertion dans ce cas)
    db_connection.set_query_response("INSERT INTO users", None)
    
    # Test avec un nom d'utilisateur vide
    with pytest.raises(ValueError):
        user_repo.insert_into_db("", "some_salt", "some_hashed_password")
    
    # Test avec un mot de passe vide
    with pytest.raises(ValueError):
        user_repo.insert_into_db("testuser", "some_salt", "")
    
    # Test avec un sel vide
    with pytest.raises(ValueError):
        user_repo.insert_into_db("testuser", "", "some_hashed_password")








# 2. Test de récupération avec un pseudo inexistant
def test_get_by_username_not_found(user_repo, db_connection):
    db_connection.set_query_response("SELECT * FROM users WHERE username = %(username)s", None)
    
    # Appeler la méthode à tester
    result = user_repo.get_by_username("nonexistentuser")
    
    # Vérifier que le résultat est None
    assert result is None


def test_insert_into_db_invalid_data():
    # Setup de la base de données mock
    mock_db_connection = MockDBConnection()
    user_repo = UserRepo(db_connection=mock_db_connection)

    # Simuler une réponse de la requête (pas nécessaire pour l'insertion dans ce cas)
    mock_db_connection.set_query_response("INSERT INTO users", None)

    # Test avec un nom d'utilisateur vide
    try:
        user_repo.insert_into_db("", "some_salt", "some_hashed_password")
    except ValueError as e:
        assert str(e) == "Username cannot be empty"

    # Test avec un mot de passe vide
    try:
        user_repo.insert_into_db("testuser", "some_salt", "")
    except ValueError as e:
        assert str(e) == "Password cannot be empty"
    
    # Test avec un sel vide
    try:
        user_repo.insert_into_db("testuser", "", "some_hashed_password")
    except ValueError as e:
        assert str(e) == "Salt cannot be empty"

# 4. Test de mise à jour avec un pseudo déjà existant
def test_update_pseudo_with_existing_username():
    # Setup de la base de données mock
    mock_db_connection = MockDBConnection()
    user_repo = UserRepo(db_connection=mock_db_connection)

    # Simuler que le pseudo existe déjà
    mock_db_connection.set_query_response("UPDATE users SET username = %(username)s WHERE id = %(user_id)s", None)
    mock_db_connection.mock_cursor.rowcount = 0  # Aucun changement de ligne, pseudo déjà existant

    # Appeler la méthode à tester
    result = user_repo.update_pseudo(1, "existingusername")

    # Vérifier que le résultat est False, car le pseudo existe déjà
    assert not result

# 5. Test de mise à jour avec un mot de passe invalide
def test_update_password_invalid_data():
    # Setup de la base de données mock
    mock_db_connection = MockDBConnection()
    user_repo = UserRepo(db_connection=mock_db_connection)

    # Simuler l'échec de la mise à jour du mot de passe avec des données invalides (mot de passe vide)
    mock_db_connection.set_query_response("UPDATE users SET password = %(password)s WHERE id = %(user_id)s", None)
    mock_db_connection.mock_cursor.rowcount = 0  # Aucun changement de ligne, mise à jour échouée

    # Appeler la méthode à tester avec un mot de passe vide
    result = user_repo.update_password(1, "")

    # Vérifier que le résultat est False, car le mot de passe est invalide
    assert not result

# 6. Test de mise à jour avec une valeur invalide pour `is_scout`
# Fonction de test
def test_update_status_invalid_value():
    # Setup de la base de données mock
    mock_db_connection = MockDBConnection()
    user_repo = UserRepo(db_connection=mock_db_connection)

    # Simuler l'échec de mise à jour du statut avec une valeur invalide
    mock_db_connection.set_query_response("UPDATE users SET is_scout = %(status)s WHERE id = %(user_id)s", None)
    mock_db_connection.mock_cursor.rowcount = 0  # Aucun changement de ligne, mise à jour échouée

    # Appeler la méthode à tester avec une valeur non booléenne (par exemple, "invalid_value")
    result = user_repo.update_status(1, "invalid_value")

    # Vérifier que le résultat est False, car la valeur est invalide
    assert not result

# 7. Test de suppression d'un utilisateur inexistant
# Fonction de test
def test_delete_by_id_user_not_found():
    # Setup de la base de données mock
    mock_db_connection = MockDBConnection()
    user_repo = UserRepo(db_connection=mock_db_connection)

    # Simuler l'échec de suppression de l'utilisateur (aucune ligne affectée)
    mock_db_connection.set_query_response("DELETE FROM users WHERE id = %(user_id)s", False)
    mock_db_connection.mock_cursor.rowcount = 0  # Simuler que l'utilisateur n'existe pas

    # Appeler la méthode à tester
    result = user_repo.delete_by_id(9999)

    # Vérifier que le résultat est False, car l'utilisateur n'existe pas
    assert result is False
