import pytest

from src.Model.user import User
from src.Model.UserFollowService import UserFollowService


class TestUserFollowService:

    def test_become_scout(self):
        """Test pour devenir éclaireur."""
        # Given
        service = UserFollowService()
        user1 = User(id_user=1, pseudo="Python")
        service.users[user1.id_user] = user1

        # When
        service.become_scout(1)

        # Then
        assert user1.is_scout is True
        assert 1 in service.scouts

    def test_add_scout(self):
        """Test pour ajouter un suivi d'éclaireur."""
        # le but : que user1 devienne éclaireur
        # Given
        service = UserFollowService()
        user1 = User(id_user=1, pseudo="Python")
        user2 = User(id_user=2, pseudo="Poule")
        service.users[user1.id_user] = user1
        service.users[user2.id_user] = user2
        service.become_scout(1)

        # When
        service.add_scout(2, 1)

        # Then
        assert ... # A FINIR