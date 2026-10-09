from typing import Protocol

from app.schemas.action_type import (
    ActionTypeCreate,
    ActionTypeResponse,
    ActionTypeUpdate,
)


class IActionTypeRepository(Protocol):
    def create_type(self, type_data: ActionTypeCreate) -> ActionTypeResponse:
        ...

    def get_type(self, type_id: int) -> ActionTypeResponse | None:
        ...

    def list_types(self) -> list[ActionTypeResponse]:
        ...

    def update_type(
        self, type_id: int, type_data: ActionTypeUpdate
    ) -> ActionTypeResponse | None:
        ...

    def delete_type(self, type_id: int) -> bool:
        ...
