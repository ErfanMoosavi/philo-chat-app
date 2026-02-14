from pydantic import BaseModel


class UserUpdateReq(BaseModel):
    name: str | None = None
    age: int | None = None
