from pydantic import BaseModel


class FavoriteResponse(BaseModel):
    action_id: int
