from typing import Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.interfaces.repositories.action import IActionRepository
from app.models.action import Action
from app.schemas.action import ActionCreate, ActionResponse, ActionUpdate


class ActionRepository(IActionRepository):
    def __init__(self, db: Session):
        self.db = db

    def create_action(self, action_data: ActionCreate) -> ActionResponse:
        new_action = Action(**action_data.model_dump())
        self.db.add(new_action)
        self.db.flush()
        self.db.refresh(new_action)
        return ActionResponse.model_validate(new_action)

    def get_action(self, action_id: int) -> Optional[ActionResponse]:
        action = self.db.query(Action).filter(Action.id == action_id).first()
        if action is None:
            return None
        return ActionResponse.model_validate(action)

    def list_actions(
        self,
        query: Optional[str] = None,
        states: Optional[list[str]] = None,
        regions: Optional[list[str]] = None,
    ) -> list[ActionResponse]:
        statement = self.db.query(Action)
        if query and (search_term := query.strip()):
            pattern = f"%{search_term}%"
            statement = statement.filter(
                or_(Action.name.ilike(pattern), Action.description.ilike(pattern))
            )
        if states:
            statement = statement.filter(Action.state.in_(states))
        if regions:
            statement = statement.filter(Action.region.in_(regions))
        actions = statement.order_by(Action.id).all()
        return [ActionResponse.model_validate(action) for action in actions]

    def update_action(
        self, action_id: int, action_data: ActionUpdate
    ) -> Optional[ActionResponse]:
        action = self.db.query(Action).filter(Action.id == action_id).first()
        if action is None:
            return None

        for field, value in action_data.model_dump().items():
            setattr(action, field, value)
        self.db.flush()
        self.db.refresh(action)
        return ActionResponse.model_validate(action)

    def delete_action(self, action_id: int) -> bool:
        action = self.db.query(Action).filter(Action.id == action_id).first()
        if action is None:
            return False

        self.db.delete(action)
        return True
