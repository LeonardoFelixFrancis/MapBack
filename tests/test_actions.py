import io
from unittest.mock import patch

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base
from app.core.auth import get_current_user, require_admin
from app.core.unit_of_work import UnitOfWork, get_uow
from app.main import app
from app.schemas.user import UserResponse


def override_admin() -> UserResponse:
    return UserResponse(id=1, email="admin@example.com", is_admin=True)


def override_user() -> UserResponse:
    return UserResponse(id=2, email="viewer@example.com", is_admin=False)


def test_action_crud() -> None:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    session_factory = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )
    app.dependency_overrides[get_uow] = lambda: UnitOfWork(session_factory)
    app.dependency_overrides[require_admin] = override_admin

    try:
        with TestClient(app) as client:
            created_response = client.post(
                "/api/v1/actions/",
                json={
                    "name": "Trailhead",
                    "description": "North entrance",
                    "latitude": -23.5505,
                    "longitude": -46.6333,
                    "state": "sp",
                },
            )
            assert created_response.status_code == 201
            created_action = created_response.json()
            assert created_action["id"] == 1
            assert created_action["name"] == "Trailhead"
            assert created_action["latitude"] == -23.5505
            assert created_action["longitude"] == -46.6333
            assert created_action["state"] == "SP"
            assert created_action["region"] == "Sudeste"

            action_id = created_action["id"]
            assert client.get("/api/v1/actions/").json() == [created_action]
            assert client.get("/api/v1/actions/?q=TRAIL").json() == [created_action]
            assert client.get("/api/v1/actions/?state=SP").json() == [created_action]
            assert client.get("/api/v1/actions/?region=Sudeste").json() == [created_action]
            assert client.get("/api/v1/actions/?region=Sul").json() == []
            assert client.get("/api/v1/actions/?q=unknown").json() == []
            assert client.get(f"/api/v1/actions/{action_id}").json() == created_action

            updated_response = client.put(
                f"/api/v1/actions/{action_id}",
                json={
                    "name": "Updated trailhead",
                    "description": "South entrance",
                    "latitude": -22.9068,
                    "longitude": -43.1729,
                    "state": "RJ",
                },
            )
            assert updated_response.status_code == 200
            assert updated_response.json()["name"] == "Updated trailhead"
            assert updated_response.json()["latitude"] == -22.9068
            assert updated_response.json()["state"] == "RJ"
            assert updated_response.json()["region"] == "Sudeste"

            assert client.delete(f"/api/v1/actions/{action_id}").status_code == 204
            assert client.get("/api/v1/actions/").json() == []
    finally:
        app.dependency_overrides.pop(get_uow, None)
        app.dependency_overrides.pop(require_admin, None)
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


def test_action_rejects_out_of_range_coordinates() -> None:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    session_factory = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )
    app.dependency_overrides[get_uow] = lambda: UnitOfWork(session_factory)
    app.dependency_overrides[require_admin] = override_admin

    try:
        with TestClient(app) as client:
            response = client.post(
                "/api/v1/actions/",
                json={
                    "name": "Invalid point",
                    "description": "Latitude outside range",
                    "latitude": 91,
                    "longitude": -46,
                    "state": "SP",
                },
            )

        assert response.status_code == 422
    finally:
        app.dependency_overrides.pop(get_uow, None)
        app.dependency_overrides.pop(require_admin, None)
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


def test_action_rejects_coordinates_outside_brazil() -> None:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    session_factory = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )
    app.dependency_overrides[get_uow] = lambda: UnitOfWork(session_factory)
    app.dependency_overrides[require_admin] = override_admin

    try:
        with TestClient(app) as client:
            response = client.post(
                "/api/v1/actions/",
                json={
                    "name": "Outside Brazil",
                    "description": "Coordinates in another country",
                    "latitude": 40.7128,
                    "longitude": -74.006,
                    "state": "SP",
                },
            )

        assert response.status_code == 422
    finally:
        app.dependency_overrides.pop(get_uow, None)
        app.dependency_overrides.pop(require_admin, None)
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


def test_action_type_crud_and_action_link() -> None:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    session_factory = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )
    app.dependency_overrides[get_uow] = lambda: UnitOfWork(session_factory)
    app.dependency_overrides[require_admin] = override_admin

    try:
        with TestClient(app) as client:
            created_type_response = client.post(
                "/api/v1/types/",
                json={"name": "Park", "description": "Public green space"},
            )
            assert created_type_response.status_code == 201
            created_type = created_type_response.json()

            created_action_response = client.post(
                "/api/v1/actions/",
                json={
                    "name": "Central Park",
                    "description": "Main entrance",
                    "latitude": -23.5505,
                    "longitude": -46.6333,
                    "state": "SP",
                    "type_id": created_type["id"],
                },
            )
            assert created_action_response.status_code == 201
            created_action = created_action_response.json()
            assert created_action["type_id"] == created_type["id"]

            updated_type_response = client.put(
                f"/api/v1/types/{created_type['id']}",
                json={"name": "Urban park", "description": "Updated description"},
            )
            assert updated_type_response.status_code == 200
            assert client.get("/api/v1/types/").json() == [
                updated_type_response.json()
            ]

            assert client.delete(f"/api/v1/types/{created_type['id']}").status_code == 204
            assert client.get(f"/api/v1/actions/{created_action['id']}").json()[
                "type_id"
            ] is None
    finally:
        app.dependency_overrides.pop(get_uow, None)
        app.dependency_overrides.pop(require_admin, None)
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


def test_action_mutation_requires_admin() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/actions/",
            json={
                "name": "Restricted",
                "description": "Requires admin access",
                "latitude": 0,
                "longitude": 0,
            },
        )

    assert response.status_code == 401


def test_user_favorites_are_scoped_to_authenticated_user() -> None:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    session_factory = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )
    app.dependency_overrides[get_uow] = lambda: UnitOfWork(session_factory)
    app.dependency_overrides[require_admin] = override_admin
    app.dependency_overrides[get_current_user] = override_user

    try:
        with TestClient(app) as client:
            action_response = client.post(
                "/api/v1/actions/",
                json={
                    "name": "Favorite location",
                    "description": "Can be favorited by viewers",
                    "latitude": -23.5505,
                    "longitude": -46.6333,
                    "state": "SP",
                },
            )
            action_id = action_response.json()["id"]

            favorite_response = client.post(f"/api/v1/favorites/{action_id}")
            assert favorite_response.status_code == 201
            assert favorite_response.json() == {"action_id": action_id}
            assert client.get("/api/v1/favorites/").json() == [
                {"action_id": action_id}
            ]

            assert client.delete(f"/api/v1/favorites/{action_id}").status_code == 204
            assert client.get("/api/v1/favorites/").json() == []
    finally:
        app.dependency_overrides.pop(get_uow, None)
        app.dependency_overrides.pop(require_admin, None)
        app.dependency_overrides.pop(get_current_user, None)
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


def test_user_registration_cannot_assign_administrator_role() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/users/",
            json={
                "email": "viewer@example.com",
                "password": "safe-password",
                "is_admin": True,
            },
        )

    assert response.status_code == 422


def test_detects_brazilian_state_and_region_from_coordinates() -> None:
    reverse_response = io.StringIO(
        '{"address": {"state": "São Paulo"}}'
    )
    with patch(
        "app.api.v1.endpoints.locations.urlopen",
        return_value=reverse_response,
    ):
        with TestClient(app) as client:
            response = client.get(
                "/api/v1/locations/reverse?latitude=-23.5505&longitude=-46.6333"
            )

    assert response.status_code == 200
    assert response.json() == {"state": "SP", "region": "Sudeste"}
