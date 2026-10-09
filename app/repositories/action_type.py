from sqlalchemy import update
from sqlalchemy.orm import Session

from app.interfaces.repositories.action_type import IActionTypeRepository
from app.models.action import Action
from app.models.action_type import ActionType
from app.schemas.action_type import (
    ActionTypeCreate,
    ActionTypeResponse,
    ActionTypeUpdate,
)


class ActionTypeRepository(IActionTypeRepository):
    def __init__(self, db: Session):
        self.db = db

    def create_type(self, type_data: ActionTypeCreate) -> ActionTypeResponse:
        new_type = ActionType(**type_data.model_dump())
        self.db.add(new_type)
        self.db.flush()
        self.db.refresh(new_type)
        return ActionTypeResponse.model_validate(new_type)

    def get_type(self, type_id: int) -> ActionTypeResponse | None:
        action_type = self.db.get(ActionType, type_id)
        if action_type is None:
            return None
        return ActionTypeResponse.model_validate(action_type)

    def list_types(self) -> list[ActionTypeResponse]:
        action_types = self.db.query(ActionType).order_by(ActionType.name).all()
        return [ActionTypeResponse.model_validate(action_type) for action_type in action_types]

    def update_type(
        self, type_id: int, type_data: ActionTypeUpdate
    ) -> ActionTypeResponse | None:
        action_type = self.db.get(ActionType, type_id)
        if action_type is None:
            return None

        for field, value in type_data.model_dump().items():
            setattr(action_type, field, value)
        self.db.flush()
        self.db.refresh(action_type)
        return ActionTypeResponse.model_validate(action_type)

    def delete_type(self, type_id: int) -> bool:
        action_type = self.db.get(ActionType, type_id)
        if action_type is None:
            return False

        self.db.execute(
            update(Action).where(Action.type_id == type_id).values(type_id=None)
        )
        self.db.delete(action_type)
        return True
