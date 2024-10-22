from typing import Optional

import pytest

from src.dao.db_connection import DBConnection
from src.Model.User import User
from src.Service.PasswordService import (create_salt, hash_password,
                                         validate_pseudo_password)


def test_hash_password():
    password = "soleil1234"
    hashed_password = hash_password(password)
    assert len(hashed_password.split('$')) == 2  

def test_hash_password_with_salt():
    password = "soleil1234"
    salt = "jambon"
    hashed_password = hash_password(password, salt)
    assert len(hashed_password.split('$')) == 2 


def test_create_salt():
    salt = create_salt()
    assert len(salt) == 256

class MockUserRepo:
    def get_by_pseudo(self, pseudo: str) -> Optional[User]:
        if pseudo == "janjak":
            return User(
                id_user=4,
                pseudo="janjak",
                password="jambon" + "56d25b0190eb6fcdab76f20550aa3e85a37ee48d520ac70385ae3615deb7d53a",  # Concaténation du sel et du mot de passe haché
                is_scout=False,
                seen=[],
                to_watch=[],
                scouts_list=[]
            )
        else:
            return None

user_repo = MockUserRepo()

def test_validate_pseudo_password_is_ok():
    janjak = validate_pseudo_password("janjak", "soleil1234", user_repo)
    assert janjak.id_user == 4

def test_validate_pseudo_password_unknown_user():
    with pytest.raises(Exception) as exception_info:
        validate_pseudo_password("Jean-Jacques", "soleil1234", user_repo)
    assert str(exception_info.value) == "User with pseudo Jean-Jacques not found" 

def test_validate_pseudo_password_incorrect_password():
    with pytest.raises(Exception) as exception_info:
        validate_pseudo_password("janjak", "wrongpassword", user_repo)
    assert str(exception_info.value) == "Incorrect password"