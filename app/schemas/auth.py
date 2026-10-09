from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class RefreshRequest(BaseModel):
    refresh_token: str
