from typing import Protocol

from app.schemas.favorite import FavoriteResponse


class IFavoriteRepository(Protocol):
    def list_favorites(self, user_id: int) -> list[FavoriteResponse]:
        ...

    def add_favorite(self, user_id: int, action_id: int) -> FavoriteResponse:
        ...

    def remove_favorite(self, user_id: int, action_id: int) -> bool:
        ...
