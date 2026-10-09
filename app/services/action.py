from typing import Optional

from app.interfaces.unit_of_work import IUnitOfWork
from app.schemas.action import ActionCreate, ActionResponse, ActionUpdate


class ActionService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def create_action(self, data: ActionCreate) -> ActionResponse:
        return self.uow.actions.create_action(data)

    def get_action(self, action_id: int) -> Optional[ActionResponse]:
        return self.uow.actions.get_action(action_id)

    def list_actions(
        self,
        query: Optional[str] = None,
        states: Optional[list[str]] = None,
        regions: Optional[list[str]] = None,
    ) -> list[ActionResponse]:
        return self.uow.actions.list_actions(query, states, regions)

    def update_action(
        self, action_id: int, data: ActionUpdate
    ) -> Optional[ActionResponse]:
        return self.uow.actions.update_action(action_id, data)

    def delete_action(self, action_id: int) -> bool:
        return self.uow.actions.delete_action(action_id)
