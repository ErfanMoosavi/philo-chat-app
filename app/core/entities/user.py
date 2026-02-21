from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from ..entities import Chat, Philosopher
from ..exceptions import NotFoundError

Base = declarative_base()
NAME_NOT_PROVIDED = "name_not_provided"
AGE_NOT_PROVIDED = -1


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    chats = relationship("Chat")

    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    first_name = Column(String, default=NAME_NOT_PROVIDED)
    age = Column(Integer, default=AGE_NOT_PROVIDED)

    def set_first_name(self, first_name: str) -> None:
        self.first_name = first_name

    def set_age(self, age: int) -> None:
        self.age = age

    def new_chat(self, chat_name: str, philosopher: Philosopher) -> None:
        new_chat = Chat(user_id=self.id, name=chat_name, philosopher=philosopher)
        self.chats.append(new_chat)

    def rename_chat(self, old_chat_name: str, new_chat_name: str) -> None:
        old_chat = self._find_chat(old_chat_name)
        if not old_chat:
            raise NotFoundError(f"Chat '{old_chat_name}' not found")

        old_chat.rename_chat(new_chat_name)

    def get_chats(self) -> list[Chat]:
        return self.chats

    def delete_chat(self, chat_name: str) -> None:
        chat = self._find_chat(chat_name)
        if not chat:
            raise NotFoundError(f"Chat '{chat_name}' not found")

        self.chats.remove(chat)

    def complete_chat(self, chat_name: str, input_text: str) -> None:
        chat = self._find_chat(chat_name)
        if not chat:
            raise NotFoundError(f"Chat '{chat_name}' not found")

        chat.complete_chat(input_text, self.username, self.first_name, self.age)

    # def _find_chat(self, db: Session, chat_id: str) -> Chat | None:
    #     chat = db.get(User, chat_id)
    #     if not chat:
    #         raise NotFoundError(f"User with id '{chat_id}' not found")
    #     return chat
