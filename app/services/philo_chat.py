import json
from pathlib import Path

from ..core.entities import Chat, ChatCompleter, Message, Philosopher, User
from ..core.exceptions import BadRequestError, NotFoundError, PermissionDeniedError


class PhiloChat:
    def __init__(self, base_url: str, api_key: str, model_name: str) -> None:
        self.chat_completer = ChatCompleter(base_url, api_key, model_name)
        self.users: dict[str, User] = {}
        self.philosophers: dict[int, Philosopher] = self._load_philosophers()

    def signup(self, username: str, password: str) -> None:
        if self._find_user(username):
            raise BadRequestError(f"Username {username} already taken")

        new_user = User(username, password)
        self.users[username] = new_user

    def login(self, username: str, password: str) -> None:
        user = self._find_user(username)

        if not user:
            raise NotFoundError("Username not found")
        elif user.password != password:
            raise PermissionDeniedError("Wrong password")

    def logout(self, username: str) -> None:
        user = self._find_user(username)
        if not user:
            raise NotFoundError("Username not found")

    def delete_account(self, username: str) -> None:
        if username not in self.users:
            raise NotFoundError(f"User {username} not found")

        del self.users[username]

    def set_name(self, username: str, name: str) -> None:
        user = self._find_user(username)
        if not user:
            raise NotFoundError(f"User {username} not found")

        user.set_name(name)

    def set_age(self, username: str, age: int) -> None:
        user = self._find_user(username)
        if not user:
            raise NotFoundError(f"User {username} not found")

        user.set_age(age)

    def new_chat(self, username: str, name: str, philosopher_id: int) -> None:
        user = self._find_user(username)
        philosopher = self._find_philosopher(philosopher_id)

        if not user:
            raise NotFoundError(f"User {username} not found")
        if not philosopher:
            raise NotFoundError(f"Philosopher with id {philosopher_id} not found")

        user.new_chat(name, philosopher)

    def select_chat(self, username: str, name: str) -> list[Message]:
        user = self._find_user(username)
        if not user:
            raise NotFoundError(f"User {username} not found")

        return user.select_chat(name)

    def get_chat_list(self, username: str) -> list[Chat]:
        user = self._find_user(username)
        if not user:
            raise NotFoundError(f"User {username} not found")

        return user.get_chat_list()

    def exit_chat(self, username: str) -> None:
        user = self._find_user(username)
        if not user:
            raise NotFoundError(f"User {username} not found")

        return user.exit_chat()

    def delete_chat(self, username: str, name: str) -> None:
        user = self._find_user(username)
        if not user:
            raise NotFoundError(f"User {username} not found")

        return user.delete_chat(name)

    def complete_chat(
        self, username: str, chat_name: str, input_text: str
    ) -> tuple[Message, Message]:
        user = self._find_user(username)
        if not user:
            raise NotFoundError(f"User {username} not found")

        return user.complete_chat(chat_name, input_text, self.chat_completer)

    def get_philosophers_list(self) -> list[Philosopher]:
        if not self.philosophers:
            raise NotFoundError("No philosopher found")

        return list(self.philosophers.values())

    def _find_user(self, username: str) -> User | None:
        return self.users.get(username)

    def _find_philosopher(self, philosopher_id: int) -> Philosopher | None:
        return self.philosophers.get(philosopher_id)

    def _load_philosophers(self) -> dict[int, Philosopher]:
        data_dir = Path(__file__).parent.parent / "resources/philosophers.json"

        with open(data_dir, "r", encoding="utf-8") as f:
            raw_philosophers = json.load(f)

        philosophers = {}
        for p in raw_philosophers:
            philosophers[p["id"]] = Philosopher(p["id"], p["name"])
        return philosophers
