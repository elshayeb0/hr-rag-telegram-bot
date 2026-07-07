from collections import defaultdict, deque

from app.config import settings


class ConversationMemory:
    def __init__(self) -> None:
        self._store: dict[str, deque[tuple[str, str]]] = defaultdict(
            lambda: deque(maxlen=settings.max_history_messages)
        )

    def add_user_message(self, user_id: str, message: str) -> None:
        self._store[user_id].append(("user", message))

    def add_assistant_message(self, user_id: str, message: str) -> None:
        self._store[user_id].append(("assistant", message))

    def get_history(self, user_id: str) -> list[tuple[str, str]]:
        return list(self._store[user_id])

    def format_history(self, user_id: str) -> str:
        history = self.get_history(user_id)

        if not history:
            return ""

        return "\n".join(f"{role}: {message}" for role, message in history)

    def clear(self, user_id: str) -> None:
        self._store[user_id].clear()


conversation_memory = ConversationMemory()
