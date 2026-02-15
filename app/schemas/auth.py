from pydantic import BaseModel


class SignupReq(BaseModel):
    username: str
    password: str


class LoginReq(BaseModel):
    username: str
    password: str


class RefreshTokenReq(BaseModel):
    refresh_token: str
