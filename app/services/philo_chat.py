from passlib.context import CryptContext
from sqlalchemy.orm import Session

from ..core.entities import Chat, Philosopher, User
from ..core.exceptions import BadRequestError, NotFoundError, PermissionDeniedError

# Create hash object
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PhiloChat:
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

    def set_first_name(self, db: Session, user_id: int, name: str) -> None:
        user = self._find_user(db, user_id)
        user.set_first_name(name)
        db.commit()

    def set_age(self, db: Session, user_id: int, age: int) -> None:
        user = self._find_user(db, user_id)
        user.set_age(age)
        db.commit()

    def new_chat(
        self, db: Session, user_id: int, chat_name: str, philosopher_id: int
    ) -> None:
        user = self._find_user(db, user_id)
        philosopher = self._find_philosopher(db, philosopher_id)
        user.new_chat(chat_name, philosopher)
        db.commit()

    def rename_chat(
        self, db: Session, user_id: int, old_chat_name: str, new_chat_name: str
    ) -> None:
        user = self._find_user(db, user_id)
        user.rename_chat(old_chat_name, new_chat_name)
        db.commit()

    def get_chats(self, db: Session, user_id: int) -> list[Chat]:
        user = self._find_user(db, user_id)
        return user.chats

    def delete_chat(self, db: Session, user_id: int, chat_name: str) -> None:
        user = self._find_user(db, user_id)
        user.delete_chat(chat_name)
        db.commit()

    def complete_chat(
        self, db: Session, user_id: int, chat_name: str, input_text: str
    ) -> None:
        user = self._find_user(db, user_id)
        user.complete_chat(chat_name, input_text)
        db.commit()

    def get_philosophers(self, db: Session) -> list[Philosopher]:
        philosophers = db.query(Philosopher).all()
        if not philosophers:
            return []

        return philosophers

    def _find_user(self, db: Session, user_id: int) -> User:
        user = db.get(User, user_id)
        if not user:
            raise NotFoundError(f"User with id '{user_id}' not found")
        return user

    def _find_philosopher(self, db: Session, philosopher_id: int) -> Philosopher:
        philosopher = db.get(Philosopher, philosopher_id)
        if not philosopher:
            raise NotFoundError(f"Philosopher with id '{philosopher_id}' not found")
        return philosopher
