from pydantic import BaseModel, Field, field_validator


class ChatCreateReq(BaseModel):
    chat_name: str = Field(..., max_length=20)
    philosopher_id: int = Field(..., le=4, ge=0)


class MessageCreateReq(BaseModel):
    input_text: str = Field(..., min_length=1, max_length=1000)

    @field_validator("input_text", mode="before")
    @classmethod
    def strip_input(cls, value: str) -> str:
        if isinstance(value, str):
            return value.strip()
        return value
