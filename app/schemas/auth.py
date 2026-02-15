from pydantic import BaseModel, Field


class SignupReq(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    password: str = Field(..., min_length=8, max_length=64)


class LoginReq(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    password: str = Field(..., min_length=8, max_length=64)


class RefreshTokenReq(BaseModel):
    refresh_token: str
