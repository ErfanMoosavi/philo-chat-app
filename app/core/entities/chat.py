from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from ...config import settings
from ..utils import load_prompt, run_completion
from .message import Message, MessageRole

Base = declarative_base()


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users"))
    messages = relationship("Message")
    philosopher = relationship("Philosopher")

    name = Column(String)

    def rename_chat(self, new_name: str) -> None:
        self.name = new_name

    def complete_chat(
        self, input_text: str, username: str, name: str, age: int
    ) -> None:
        if self._is_first_message():
            prompt = load_prompt(input_text, self.philosopher.name, name, age)
            prompt_msg = Message(MessageRole.USER, username, prompt)
            self._add_message(prompt_msg)

        user_msg = Message(MessageRole.USER, username, input_text)
        response = run_completion(
            settings.base_url, settings.api_key, settings.llm_model, self.messages
        )
        ai_msg = Message(MessageRole.ASSISTANT, self.philosopher.name, response)

        self._add_message(user_msg)
        self._add_message(ai_msg)

    def get_history(self) -> list[Message]:
        return self.messages[1:]

    def _add_message(self, new_msg: Message) -> None:
        self.messages.append(new_msg)

    def _is_first_message(self) -> bool:
        return not self.messages
