from pydantic import BaseModel


class DetectedLocationResponse(BaseModel):
    state: str
    region: str
