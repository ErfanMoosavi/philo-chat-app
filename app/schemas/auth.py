from pydantic import BaseModel, Field


class SignupReq(BaseModel):
    username: str = Field(..., min_length=3, max_length=20, pattern=r"^[a-zA-Z0-9_]+$")
    password: str = Field(
        ..., min_length=8, max_length=64, pattern=r"r'^[A-Za-z0-9!@#$%^&*()_+]+$'"
    )


class LoginReq(BaseModel):
    username: str = Field(..., min_length=3, max_length=20, pattern=r"^[a-zA-Z0-9_]+$")
    password: str = Field(
        ..., min_length=8, max_length=64, pattern=r"r'^[A-Za-z0-9!@#$%^&*()_+]+$'"
    )


class RefreshTokenReq(BaseModel):
    refresh_token: str
