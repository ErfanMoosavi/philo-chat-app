from ..utils import load_prompt
from .message import Message, MessageRole
from .philosopher import Philosopher


class Chat:
    def __init__(self, name: str, philosopher: Philosopher) -> None:
        self.name = name
        self.philosopher = philosopher
        self.messages: list[Message] = []

    def rename(self, new_name: str) -> None:
        self.name = new_name

    def complete_chat(
        self, input_text: str, username: str, name: str, age: int, chat_completer
    ) -> tuple[Message, Message]:
        if self._is_first_message():
            prompt = load_prompt(input_text, self.philosopher.name, name, age)
            prompt_msg = Message(MessageRole.USER, username, prompt)
            self._add_message(prompt_msg)

        user_msg = Message(MessageRole.USER, username, input_text)
        response = chat_completer.complete_chat(self.messages)
        ai_msg = Message(MessageRole.ASSISTANT, self.philosopher.name, response)

        self._add_message(ai_msg)
        self._add_message(user_msg)

        return ai_msg, user_msg

    def get_history(self) -> list[Message]:
        # Don't include the prompt
        return self.messages[1:]

    def _add_message(self, new_msg: Message) -> None:
        self.messages.append(new_msg)

    def _is_first_message(self) -> bool:
        return not self.messages
