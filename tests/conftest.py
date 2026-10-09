import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from app.main import app
from app.interfaces.unit_of_work import IUnitOfWork
from app.core.unit_of_work import get_uow

@pytest.fixture
def mock_uow():
    uow = MagicMock(spec=IUnitOfWork)
    return uow

@pytest.fixture
def client(mock_uow):
    app.dependency_overrides[get_uow] = lambda: mock_uow

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()