from app.interfaces.unit_of_work import IUnitOfWork
from app.schemas.favorite import FavoriteResponse


class FavoriteService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def list_favorites(self, user_id: int) -> list[FavoriteResponse]:
        return self.uow.favorites.list_favorites(user_id)

    def add_favorite(
        self, user_id: int, action_id: int
    ) -> FavoriteResponse | None:
        if self.uow.actions.get_action(action_id) is None:
            return None
        return self.uow.favorites.add_favorite(user_id, action_id)

    def remove_favorite(self, user_id: int, action_id: int) -> bool:
        return self.uow.favorites.remove_favorite(user_id, action_id)
