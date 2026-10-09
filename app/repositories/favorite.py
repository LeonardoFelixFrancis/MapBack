from sqlalchemy.orm import Session

from app.interfaces.repositories.favorite import IFavoriteRepository
from app.models.favorite import Favorite
from app.schemas.favorite import FavoriteResponse


class FavoriteRepository(IFavoriteRepository):
    def __init__(self, db: Session):
        self.db = db

    def list_favorites(self, user_id: int) -> list[FavoriteResponse]:
        favorites = (
            self.db.query(Favorite)
            .filter(Favorite.user_id == user_id)
            .order_by(Favorite.action_id)
            .all()
        )
        return [FavoriteResponse(action_id=favorite.action_id) for favorite in favorites]

    def add_favorite(self, user_id: int, action_id: int) -> FavoriteResponse:
        favorite = self.db.get(Favorite, (user_id, action_id))
        if favorite is None:
            favorite = Favorite(user_id=user_id, action_id=action_id)
            self.db.add(favorite)
            self.db.flush()
        return FavoriteResponse(action_id=favorite.action_id)

    def remove_favorite(self, user_id: int, action_id: int) -> bool:
        favorite = self.db.get(Favorite, (user_id, action_id))
        if favorite is None:
            return False
        self.db.delete(favorite)
        return True
