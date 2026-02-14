from pydantic import BaseModel


class SignupReq(BaseModel):
    username: str
    password: str


class LoginReq(BaseException):
    username: str
    password: str
