from app.interfaces.unit_of_work import IUnitOfWork
from app.schemas.action_type import (
    ActionTypeCreate,
    ActionTypeResponse,
    ActionTypeUpdate,
)


class ActionTypeService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def create_type(self, data: ActionTypeCreate) -> ActionTypeResponse:
        return self.uow.action_types.create_type(data)

    def get_type(self, type_id: int) -> ActionTypeResponse | None:
        return self.uow.action_types.get_type(type_id)

    def list_types(self) -> list[ActionTypeResponse]:
        return self.uow.action_types.list_types()

    def update_type(
        self, type_id: int, data: ActionTypeUpdate
    ) -> ActionTypeResponse | None:
        return self.uow.action_types.update_type(type_id, data)

    def delete_type(self, type_id: int) -> bool:
        return self.uow.action_types.delete_type(type_id)
