from pydantic import BaseModel


class ChatCreateReq(BaseModel):
    chat_name: str
    philosopher_id: int


class MessageCreateReq(BaseModel):
    input_text: str
