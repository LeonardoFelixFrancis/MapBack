from fastapi import APIRouter

from app.api.v1.endpoints import (
    action_types,
    actions,
    auth,
    favorites,
    locations,
    users,
)

router = APIRouter(prefix="/api/v1")

router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(actions.router, prefix="/actions", tags=["actions"])
router.include_router(action_types.router, prefix="/types", tags=["types"])
router.include_router(favorites.router, prefix="/favorites", tags=["favorites"])
router.include_router(locations.router, prefix="/locations", tags=["locations"])