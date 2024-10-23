from typing import Optional

import pytest

from src.Model.User import User
from src.Service.PasswordService import PasswordService


class MockUserRepo:
    def get_by_pseudo(self, pseudo: str) -> Optional[User]:
        if pseudo == "janjak":
            return User(
                id_user=4,
                pseudo="janjak",
                password=password_service.hash_password("Jambon1234"),
                seen=[],
                is_scout=False,
                to_watch=[],
                scouts_list=[]
            )
        else:
            return None

password_service = PasswordService()  
user_repo = MockUserRepo()

def test_hash_password():
    password = "soleil1234"
    hashed_password = password_service.hash_password(password)
    assert len(hashed_password.split('$')) == 2  

def test_hash_password_with_salt():
    password = "soleil1234"
    salt = "jambon"
    hashed_password = password_service.hash_password(password, salt)
    assert len(hashed_password.split('$')) == 2 

def test_create_salt():
    salt = password_service.create_salt()
    assert len(salt) == 256

def test_validate_pseudo_password_is_ok():
    janjak = password_service.validate_pseudo_password("janjak", "Jambon1234", user_repo)
    assert janjak.id_user == 4

def test_validate_pseudo_password_unknown_user():
    with pytest.raises(Exception) as exception_info:
        password_service.validate_pseudo_password("Jean-Jacques", "Jambon1234", user_repo)
    assert str(exception_info.value) == "User with pseudo Jean-Jacques not found"

def test_validate_pseudo_password_incorrect_password():
    with pytest.raises(Exception) as exception_info:
        password_service.validate_pseudo_password("janjak", "IncorrectPassword1", user_repo)
    assert str(exception_info.value) == "Incorrect password"

def test_validate_pseudo_password_invalid_format():
    with pytest.raises(ValueError) as exception_info:
        password_service.validate_pseudo_password("janjak", "invalid@password", user_repo) 
    assert str(exception_info.value) == "Password must contain only letters and digits (no special characters)"

def test_validate_pseudo_password_too_short(): 
    with pytest.raises(ValueError) as exception_info:
        password_service.validate_pseudo_password("janjak", "short", user_repo) 
    assert str(exception_info.value) == "Password length must be at least 8 characters"

def test_validate_pseudo_password_no_uppercase():
    with pytest.raises(ValueError) as exception_info:
        password_service.validate_pseudo_password("janjak", "lowercase123", user_repo)  
    assert str(exception_info.value) == "Password must contain at least one uppercase letter"

def test_validate_pseudo_password_no_lowercase():
    with pytest.raises(ValueError) as exception_info:
        password_service.validate_pseudo_password("janjak", "UPPERCASE123", user_repo)  
    assert str(exception_info.value) == "Password must contain at least one lowercase letter"

def test_validate_pseudo_password_no_digit():
    with pytest.raises(ValueError) as exception_info:
        password_service.validate_pseudo_password("janjak", "NoDigitsHere", user_repo)  
    assert str(exception_info.value) == "Password must contain at least one digit"
