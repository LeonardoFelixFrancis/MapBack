from pydantic import BaseModel


class ActionTypeBase(BaseModel):
    name: str
    description: str


class ActionTypeCreate(ActionTypeBase):
    pass


class ActionTypeUpdate(ActionTypeBase):
    pass


class ActionTypeResponse(ActionTypeBase):
    id: int

    model_config = {"from_attributes": True}
