from datetime import datetime
from enum import Enum


class MessageRole(Enum):
    USER = "user"
    ASSISTANT = "assistant"


class Message:
    def __init__(self, role: MessageRole, author: str, content: str) -> None:
        self.role = role
        self.author = author
        self.content = content
        self.time = datetime.now().strftime("%H:%M")
