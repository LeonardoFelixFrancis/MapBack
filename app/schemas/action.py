from pydantic import BaseModel, Field, model_validator

from app.core.brazil import (
    BRAZILIAN_STATES,
    normalize_brazilian_state,
    validate_brazilian_coordinates,
)


class ActionBase(BaseModel):
    name: str
    description: str
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    type_id: int | None = None


class ActionCreate(ActionBase):
    state: str = Field(min_length=2, max_length=2)
    region: str = ""

    @model_validator(mode="after")
    def validate_brazil_location(self) -> "ActionCreate":
        self.state = normalize_brazilian_state(self.state)
        validate_brazilian_coordinates(self.latitude, self.longitude)
        self.region = BRAZILIAN_STATES[self.state]
        return self


class ActionUpdate(ActionCreate):
    pass


class ActionResponse(ActionBase):
    id: int
    state: str | None
    region: str | None

    model_config = {"from_attributes": True}
