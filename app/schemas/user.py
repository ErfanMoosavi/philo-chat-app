from pydantic import BaseModel, Field


class UserUpdateReq(BaseModel):
    name: str | None = Field(default=None, min_length=3, max_length=20)
    age: int | None = Field(default=None, le=120, ge=0)
