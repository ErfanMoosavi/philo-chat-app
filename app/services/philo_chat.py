import json
from pathlib import Path

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from ..core.exceptions import BadRequestError, NotFoundError, PermissionDeniedError
from ..core.models import Chat, User

# Create hash object
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PhiloChat:
    def __init__(self):
        self.philosophers = self._load_philosophers()

    def signup(self, db: Session, username: str, password: str) -> None:
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            raise BadRequestError(f"Username '{username}' already taken")

        password_hash = pwd_context.hash(password)
        new_user = User(username=username, password_hash=password_hash)

        db.add(new_user)
        db.commit()

    def login(self, db: Session, username: str, password: str) -> None:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise NotFoundError(f"Username '{username}' not found")

        if not pwd_context.verify(password, user.password_hash):
            raise PermissionDeniedError("Password is incorrect")

    def delete_account(self, db: Session, user_id: int) -> None:
        user = self._find_user(db, user_id)
        db.delete(user)
        db.commit()

    def update_profile(
        self, db: Session, user_id: int, name: str | None, age: int | None
    ) -> None:
        user = self._find_user(db, user_id)
        user.update_profile(name, age)
        db.commit()

    def new_chat(
        self, db: Session, user_id: int, chat_name: str, philosopher_id: int
    ) -> None:
        user = self._find_user(db, user_id)
        philosopher = self._find_philosopher(philosopher_id)
        user.new_chat(chat_name, philosopher["name"])
        db.commit()

    def get_chats(self, db: Session, user_id: int) -> list[Chat]:
        user = self._find_user(db, user_id)
        return user.chats

    def delete_chat(self, db: Session, user_id: int, chat_id: int) -> None:
        user = self._find_user(db, user_id)
        user.delete_chat(db, chat_id)
        db.commit()

    def complete_chat(
        self, db: Session, user_id: int, chat_id: int, input_text: str
    ) -> None:
        user = self._find_user(db, user_id)
        user.complete_chat(db, chat_id, input_text)
        db.commit()

    def get_philosophers(self) -> list[dict]:
        return self.philosophers

    def _find_user(self, db: Session, user_id: int) -> User:
        user = db.get(User, user_id)
        if not user:
            raise NotFoundError(f"User with id '{user_id}' not found")
        return user

    def _find_philosopher(self, philosopher_id: int) -> dict:
        for p in self.philosophers:
            if p["id"] == philosopher_id:
                return p
        raise NotFoundError(f"Philosopher with id '{philosopher_id}' not found")

    def _load_philosophers(self) -> list[dict]:
        json_path = Path(__file__).parent.parent / "resources" / "philosophers.json"
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
