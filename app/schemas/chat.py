from pydantic import BaseModel, Field


class ChatCreateReq(BaseModel):
    chat_name: str = Field(..., max_length=20)
    philosopher_id: int = Field(..., le=4, ge=0)


class ChatNameUpdateReq(BaseModel):
    new_chat_name: str = Field(..., max_length=20)


class MessageCreateReq(BaseModel):
    input_text: str = Field(..., min_length=1, max_length=1000)
