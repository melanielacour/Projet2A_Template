from unittest import mock
from unittest.mock import MagicMock

import pytest

from src.dao.review_dao import ReviewDao
from src.Model.Review import Review


@pytest.fixture
def review_dao():
    return ReviewDao()

@pytest.fixture
def mock_db():
    mock_connection= MagicMock()
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    return mock_connection, mock_cursor

def test_get_all_review_by_id(review_dao, mock_db):
    mock_connection, mock_cursor = mock_db
    review_dao.db_connection = mock_connection
    mock_cursor.fetchall.return_value = [
        {"id_review": 1, "id_film": 1, "id_user": 1, "review": "Film incroyable"},
        {"id_review": 2, "id_film": 1, "id_user": 2, "review": "Nul"}
    ]

    reviews = review_dao.get_all_review_by_id(1)

    assert len(reviews) == 2
    assert reviews[0].review == "Film incroyable"
    assert reviews[1].review == "Nul"