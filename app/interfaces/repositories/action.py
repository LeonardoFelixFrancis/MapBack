from typing import Optional, Protocol

from app.schemas.action import ActionCreate, ActionResponse, ActionUpdate


class IActionRepository(Protocol):
    def create_action(self, action_data: ActionCreate) -> ActionResponse:
        ...

    def get_action(self, action_id: int) -> Optional[ActionResponse]:
        ...

    def list_actions(
        self,
        query: Optional[str] = None,
        states: Optional[list[str]] = None,
        regions: Optional[list[str]] = None,
    ) -> list[ActionResponse]:
        ...

    def update_action(
        self, action_id: int, action_data: ActionUpdate
    ) -> Optional[ActionResponse]:
        ...

    def delete_action(self, action_id: int) -> bool:
        ...
