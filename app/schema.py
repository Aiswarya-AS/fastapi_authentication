from typing import TypeVar, Optional, Generic
from pydantic import BaseModel, Field
T = TypeVar("T")

class UserSchema(BaseModel):
    username:Optional[str] = None
    password:Optional[str] = None

    class config:
        orm_mode = True

class RequestUser(BaseModel):
    parameter:UserSchema  = Field(...)


class Response(BaseModel, Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]