import os
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

# Tests must provide their own signing key because production configuration requires one.
os.environ.setdefault("SECRET_KEY", "test-secret-key-that-is-at-least-32-characters-long")

from app.core.unit_of_work import get_uow
from app.interfaces.unit_of_work import IUnitOfWork
from app.main import app


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