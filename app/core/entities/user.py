from passlib.context import CryptContext

from ..exceptions import BadRequestError, NotFoundError
from .chat import Chat
from .message import Message
from .philosopher import Philosopher

NAME_NOT_PROVIDED = "name_not_provided"
AGE_NOT_PROVIDED = -1

# Create hash object
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User:
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password_hash = pwd_context.hash(password)
        self.name = NAME_NOT_PROVIDED
        self.age = AGE_NOT_PROVIDED
        self.chats: dict[str, Chat] = {}

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password_hash)

    def set_name(self, name: str) -> None:
        self.name = name

    def set_age(self, age: int) -> None:
        self.age = age

    def new_chat(self, chat_name: str, philosopher: Philosopher) -> None:
        if self._find_chat(chat_name):
            raise BadRequestError(f"Chat '{chat_name}' already exists")

        new_chat = Chat(chat_name, philosopher)
        self.chats[chat_name] = new_chat

    def rename_chat(self, old_chat_name: str, new_chat_name: str) -> None:
        if self._find_chat(new_chat_name):
            raise BadRequestError(f"Chat '{new_chat_name}' already exists")

        chat = self._find_chat(old_chat_name)
        if not chat:
            raise NotFoundError(f"Chat '{old_chat_name}' not found")

        chat.rename_chat(new_chat_name)

    def get_chat_list(self) -> list[Chat]:
        if not self.chats:
            raise NotFoundError("No chats found")

        return list(self.chats.values())

    def delete_chat(self, chat_name: str) -> None:
        chat = self._find_chat(chat_name)
        if not chat:
            raise NotFoundError(f"Chat '{chat_name}' not found")

        del self.chats[chat_name]

    def complete_chat(
        self, chat_name: str, input_text: str, chat_completer
    ) -> tuple[Message, Message]:
        chat = self._find_chat(chat_name)
        if not chat:
            raise NotFoundError(f"Chat '{chat_name}' not found")

        return chat.complete_chat(
            input_text, self.username, self.name, self.age, chat_completer
        )

    def _find_chat(self, name: str) -> Chat | None:
        return self.chats.get(name)
